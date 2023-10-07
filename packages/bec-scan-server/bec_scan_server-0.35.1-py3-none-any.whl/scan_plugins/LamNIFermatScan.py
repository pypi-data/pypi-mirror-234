"""
SCAN PLUGINS

All new scans should be derived from ScanBase. ScanBase provides various methods that can be customized and overriden
but they are executed in a specific order:

- self.initialize                        # initialize the class if needed
- self.read_scan_motors                  # used to retrieve the start position (and the relative position shift if needed)
- self.prepare_positions                 # prepare the positions for the scan. The preparation is split into multiple sub fuctions:
    - self._calculate_positions          # calculate the positions
    - self._set_positions_offset         # apply the previously retrieved scan position shift (if needed)
    - self._check_limits                 # tests to ensure the limits won't be reached
- self.open_scan                         # send an open_scan message including the scan name, the number of points and the scan motor names
- self.stage                             # stage all devices for the upcoming acquisiton
- self.run_baseline_readings             # read all devices to get a baseline for the upcoming scan
- self.scan_core                         # run a loop over all position
    - self._at_each_point(ind, pos)      # called at each position with the current index and the target positions as arguments
- self.finalize                          # clean up the scan, e.g. move back to the start position; wait everything to finish
- self.unstage                           # unstage all devices that have been staged before
- self.cleanup                           # send a close scan message and perform additional cleanups if needed
"""

import time

import numpy as np
from bec_lib.core import BECMessage, MessageEndpoints, bec_logger

from scan_server.errors import ScanAbortion
from scan_server.scans import RequestBase, ScanArgType, ScanBase

MOVEMENT_SCALE_X = np.sin(np.radians(15)) * np.cos(np.radians(30))
MOVEMENT_SCALE_Y = np.cos(np.radians(15))

logger = bec_logger.logger


def lamni_to_stage_coordinates(x: float, y: float) -> tuple:
    """convert from lamni coordinates to stage coordinates"""
    y_stage = y / MOVEMENT_SCALE_Y
    x_stage = 2 * (x - y_stage * MOVEMENT_SCALE_X)
    return (x_stage, y_stage)


def lamni_from_stage_coordinates(x_stage: float, y_stage: float) -> tuple:
    """convert to lamni coordinates from stage coordinates"""
    x = x_stage * 0.5 + y_stage * MOVEMENT_SCALE_X
    y = y_stage * MOVEMENT_SCALE_Y
    return (x, y)


class LamNIMixin:
    def _lamni_compute_scan_center(self, x, y, angle_deg):
        # assuming a scan point was found at interferometer x,y at zero degrees
        # this function computes the new interferometer coordinates of this spot
        # at a different rotation angle based on the lamni geometry
        alpha = angle_deg / 180 * np.pi
        stage_x, stage_y = lamni_to_stage_coordinates(x, y)
        stage_x_rot = np.cos(alpha) * stage_x - np.sin(alpha) * stage_y
        stage_y_rot = np.sin(alpha) * stage_x + np.cos(alpha) * stage_y
        return lamni_from_stage_coordinates(stage_x_rot, stage_y_rot)

    def lamni_new_scan_center_interferometer(self, x, y):
        """move to new scan center. xy in mm"""
        lsamx_user_params = self.device_manager.devices.lsamx.user_parameter
        if lsamx_user_params is None or lsamx_user_params.get("center") is None:
            raise RuntimeError("lsamx center is not defined")
        lsamy_user_params = self.device_manager.devices.lsamy.user_parameter
        if lsamy_user_params is None or lsamy_user_params.get("center") is None:
            raise RuntimeError("lsamy center is not defined")
        lsamx_center = lsamx_user_params.get("center")
        lsamy_center = lsamy_user_params.get("center")

        # could first check if feedback is enabled
        yield from self.stubs.send_rpc_and_wait("rtx", "controller.feedback_disable")
        time.sleep(0.05)

        rtx_current = yield from self.stubs.send_rpc_and_wait("rtx", "readback.get")
        rty_current = yield from self.stubs.send_rpc_and_wait("rty", "readback.get")
        lsamx_current = yield from self.stubs.send_rpc_and_wait("lsamx", "readback.get")
        lsamy_current = yield from self.stubs.send_rpc_and_wait("lsamy", "readback.get")

        x_stage, y_stage = lamni_to_stage_coordinates(x, y)

        x_center_expect, y_center_expect = lamni_from_stage_coordinates(
            lsamx_current - lsamx_center, lsamy_current - lsamy_center
        )

        # in microns
        x_drift = x_center_expect * 1000 - rtx_current
        y_drift = y_center_expect * 1000 - rty_current

        logger.info(f"Current uncompensated drift of setup is x={x_drift:.3f}, y={y_drift:.3f}")

        move_x = x_stage + lsamx_center + lamni_to_stage_coordinates(x_drift, y_drift)[0] / 1000
        move_y = y_stage + lsamy_center + lamni_to_stage_coordinates(x_drift, y_drift)[1] / 1000

        coarse_move_req_x = np.abs(lsamx_current - move_x)
        coarse_move_req_y = np.abs(lsamy_current - move_y)

        self.device_manager.devices.lsamx.enabled_set = True
        self.device_manager.devices.lsamy.enabled_set = True

        if (
            np.abs(y_drift) > 150
            or np.abs(x_drift) > 150
            or (coarse_move_req_y < 0.003 and coarse_move_req_x < 0.003)
        ):
            logger.info("No drift correction.")
        else:
            logger.info(
                f"Compensating {[val/1000 for val in lamni_to_stage_coordinates(x_drift,y_drift)]}"
            )
            yield from self.stubs.set_and_wait(
                device=["lsamx", "lsamy"], positions=[move_x, move_y]
            )

        time.sleep(0.01)
        rtx_current = yield from self.stubs.send_rpc_and_wait("rtx", "readback.get")
        rty_current = yield from self.stubs.send_rpc_and_wait("rty", "readback.get")

        logger.info(f"New scan center interferometer {rtx_current:.3f}, {rty_current:.3f} microns")

        # second iteration
        x_center_expect, y_center_expect = lamni_from_stage_coordinates(x_stage, y_stage)

        # in microns
        x_drift2 = x_center_expect * 1000 - rtx_current
        y_drift2 = y_center_expect * 1000 - rty_current
        logger.info(
            f"Uncompensated drift of setup after first iteration is x={x_drift2:.3f}, y={y_drift2:.3f}"
        )

        if np.abs(x_drift2) > 5 or np.abs(y_drift2) > 5:
            logger.info(
                f"Compensating second iteration {[val/1000 for val in lamni_to_stage_coordinates(x_drift2,y_drift2)]}"
            )
            move_x = (
                x_stage
                + lsamx_center
                + lamni_to_stage_coordinates(x_drift, y_drift)[0] / 1000
                + lamni_to_stage_coordinates(x_drift2, y_drift2)[0] / 1000
            )
            move_y = (
                y_stage
                + lsamy_center
                + lamni_to_stage_coordinates(x_drift, y_drift)[1] / 1000
                + lamni_to_stage_coordinates(x_drift2, y_drift2)[1] / 1000
            )
            yield from self.stubs.set_and_wait(
                device=["lsamx", "lsamy"], positions=[move_x, move_y]
            )
            time.sleep(0.01)
            rtx_current = yield from self.stubs.send_rpc_and_wait("rtx", "readback.get")
            rty_current = yield from self.stubs.send_rpc_and_wait("rty", "readback.get")

            logger.info(
                f"New scan center interferometer after second iteration {rtx_current:.3f}, {rty_current:.3f} microns"
            )
            x_drift2 = x_center_expect * 1000 - rtx_current
            y_drift2 = y_center_expect * 1000 - rty_current
            logger.info(
                f"Uncompensated drift of setup after second iteration is x={x_drift2:.3f}, y={y_drift2:.3f}"
            )
        else:
            logger.info("No second iteration required")

        self.device_manager.devices.lsamx.enabled_set = False
        self.device_manager.devices.lsamy.enabled_set = False

        yield from self.stubs.send_rpc_and_wait("rtx", "controller.feedback_enable_without_reset")


class LamNIMoveToScanCenter(RequestBase, LamNIMixin):
    scan_name = "lamni_move_to_scan_center"
    scan_report_hint = None
    scan_type = "step"
    required_kwargs = []
    arg_input = [ScanArgType.FLOAT, ScanArgType.FLOAT, ScanArgType.FLOAT]
    arg_bundle_size = None

    def __init__(self, *args, parameter=None, **kwargs):
        """
        Move LamNI to a new scan center.

        Args:
            *args: shift x, shift y, tomo angle in deg

        Examples:
            >>> scans.lamni_move_to_scan_center(1.2, 2.8, 12.5)
        """
        super().__init__(parameter=parameter, **kwargs)

    def run(self):
        center_x, center_y = self._lamni_compute_scan_center(*self.caller_args)
        yield from self.lamni_new_scan_center_interferometer(center_x, center_y)


class LamNIFermatScan(ScanBase, LamNIMixin):
    scan_name = "lamni_fermat_scan"
    scan_report_hint = "table"
    scan_type = "step"
    required_kwargs = ["fov_size", "exp_time", "step", "angle"]
    arg_input = []
    arg_bundle_size = None

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A LamNI scan following Fermat's spiral.

        Kwargs:
            fov_size [um]: Fov in the piezo plane (i.e. piezo range). Max 80 um
            step [um]: stepsize
            shift_x/y [mm]: extra shift in x/y. The shift is directly applied to the scan. It will not be auto rotated. (default 0).
            center_x/center_y [mm]: center position in x/y at 0 deg. This shift is rotated
                               using the geometry of LamNI
                               It is determined by the first 'click' in the x-ray eye alignemnt procedure
            angle [deg]: rotation angle (will rotate first)
            scan_type: fly (i.e. HW triggered step in case of LamNI) or step
            stitch_x/y: shift scan to adjacent stitch region
            fov_circular [um]: generate a circular field of view in the sample plane. This is an additional cropping to fov_size.
            stitch_overlap [um]: overlap of the stitched regions
        Returns:

        Examples:
            >>> scans.lamni_fermat_scan(fov_size=[20], step=0.5, exp_time=0.1)
            >>> scans.lamni_fermat_scan(fov_size=[20, 25], center_x=0.02, center_y=0, shift_x=0, shift_y=0, angle=0, step=0.5, fov_circular=0, exp_time=0.1)
        """

        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        scan_kwargs = parameter.get("kwargs", {})
        self.fov_size = scan_kwargs.get("fov_size")
        if len(self.fov_size) == 1:
            self.fov_size *= 2  # if we only have one argument, let's assume it's a square
        self.step = scan_kwargs.get("step", 0.1)
        self.center_x = scan_kwargs.get("center_x", 0)
        self.center_y = scan_kwargs.get("center_y", 0)
        self.shift_x = scan_kwargs.get("shift_x", 0)
        self.shift_y = scan_kwargs.get("shift_y", 0)
        self.angle = scan_kwargs.get("angle", 0)
        self.scan_type = scan_kwargs.get("scan_type", "fly")
        self.stitch_x = scan_kwargs.get("stitch_x", 0)
        self.stitch_y = scan_kwargs.get("stitch_y", 0)
        self.fov_circular = scan_kwargs.get("fov_circular", 0)
        self.stitch_overlap = scan_kwargs.get("stitch_overlap", 1)
        # self.keep_plot = scan_kwargs.get("keep_plot", 0)
        self.optim_trajectory = scan_kwargs.get("optim_trajectory", "corridor")
        self.optim_trajectory_corridor = scan_kwargs.get("optim_trajectory_corridor")

    def initialize(self):
        self.scan_motors = ["rtx", "rty"]

    def _optimize_trajectory(self):
        self.positions = self.optimize_corridor(
            self.positions, corridor_size=self.optim_trajectory_corridor
        )

    def prepare_positions(self):
        self._calculate_positions()
        self._optimize_trajectory()
        # self._sort_positions()

        self.num_pos = len(self.positions)
        self._check_min_positions()

    def _check_min_positions(self):
        if self.num_pos < 20:
            raise ScanAbortion(
                f"The number of positions must exceed 20. Currently: {self.num_pos}."
            )

    def _lamni_check_pos_in_fov_range_and_circ_fov(self, x, y) -> bool:
        # this function checks if positions are reachable in a scan
        # these x y intererometer positions are not shifted to the scan center
        # so its purpose is to see if the position is reachable by the
        # rotated piezo stage. For a scan these positions have to be shifted to
        # the current scan center before starting the scan
        stage_x, stage_y = lamni_to_stage_coordinates(x, y)
        stage_x_with_stitch, stage_y_with_stitch = self._lamni_compute_stitch_center(
            self.stitch_x, self.stitch_y, self.angle
        )
        stage_x_with_stitch, stage_y_with_stitch = lamni_to_stage_coordinates(
            stage_x_with_stitch, stage_y_with_stitch
        )

        # piezo stage is currently rotated to stage_angle_deg in degrees
        # rotate positions to the piezo stage system
        alpha = (self.angle - 300 + 30.5) / 180 * np.pi
        stage_x_rot = np.cos(alpha) * stage_x + np.sin(alpha) * stage_y
        stage_y_rot = -np.sin(alpha) * stage_x + np.cos(alpha) * stage_y

        stage_x_rot_with_stitch = (
            np.cos(alpha) * stage_x_with_stitch + np.sin(alpha) * stage_y_with_stitch
        )
        stage_y_rot_with_stitch = (
            -np.sin(alpha) * stage_x_with_stitch + np.cos(alpha) * stage_y_with_stitch
        )

        return (
            np.abs(stage_x_rot) <= (self.fov_size[1] / 2)
            and np.abs(stage_y_rot) <= (self.fov_size[0] / 2)
            and (
                self.fov_circular == 0
                or (
                    np.power((stage_x_rot_with_stitch + stage_x_rot), 2)
                    + np.power((stage_y_rot_with_stitch + stage_y_rot), 2)
                )
                <= pow((self.fov_circular / 2), 2)
            )
        )

    def _prepare_setup(self):
        yield from self.stubs.send_rpc_and_wait("rtx", "controller.clear_trajectory_generator")
        yield from self.lamni_rotation(self.angle)
        total_shift_x, total_shift_y = self._compute_total_shift()
        yield from self.lamni_new_scan_center_interferometer(total_shift_x, total_shift_y)
        # self._plot_target_pos()
        if self.scan_type == "fly":
            yield from self._transfer_positions_to_LamNI()

    # def _plot_target_pos(self):
    #     # return
    #     plt.plot(self.positions[:, 0], self.positions[:, 1], alpha=0.2)
    #     plt.scatter(self.positions[:, 0], self.positions[:, 1])
    #     plt.savefig("mygraph.png")
    #     if not self.keep_plot:
    #         plt.clf()
    #     # plt.show()

    def _transfer_positions_to_LamNI(self):
        yield from self.stubs.send_rpc_and_wait(
            "rtx", "controller.add_pos_to_scan", (self.positions.tolist(),)
        )

    def _calculate_positions(self):
        self.positions = self.get_lamni_fermat_spiral_pos(
            -np.abs(self.fov_size[0] / 2),
            np.abs(self.fov_size[0] / 2),
            -np.abs(self.fov_size[1] / 2),
            np.abs(self.fov_size[1] / 2),
            step=self.step,
            spiral_type=0,
            center=False,
        )

    def _lamni_compute_stitch_center(self, xcount, ycount, angle_deg):
        alpha = angle_deg / 180 * np.pi
        stage_x = xcount * (self.fov_size[0] - self.stitch_overlap)
        stage_y = ycount * (self.fov_size[1] - self.stitch_overlap)
        x_rot = np.cos(alpha) * stage_x - np.sin(alpha) * stage_y
        y_rot = np.sin(alpha) * stage_x + np.cos(alpha) * stage_y

        return lamni_from_stage_coordinates(x_rot, y_rot)

    def _compute_total_shift(self):
        _shfitx, _shfity = self._lamni_compute_scan_center(self.center_x, self.center_y, self.angle)
        x_stitch_shift, y_stitch_shift = self._lamni_compute_stitch_center(
            self.stitch_x, self.stitch_y, self.angle
        )
        logger.info(
            f"Total shift [mm] {_shfitx+x_stitch_shift/1000+self.shift_x}, {_shfity+y_stitch_shift/1000+self.shift_y}"
        )
        return (
            _shfitx + x_stitch_shift / 1000 + self.shift_x,
            _shfity + y_stitch_shift / 1000 + self.shift_y,
        )

    def get_lamni_fermat_spiral_pos(
        self, m1_start, m1_stop, m2_start, m2_stop, step=1, spiral_type=0, center=False
    ):
        """[summary]

        Args:
            m1_start (float): start position motor 1
            m1_stop (float): end position motor 1
            m2_start (float): start position motor 2
            m2_stop (float): end position motor 2
            step (float, optional): Step size. Defaults to 1.
            spiral_type (float, optional): Angular offset in radians that determines the shape of the spiral.
            A spiral with spiral_type=2 is the same as spiral_type=0. Defaults to 0.
            center (bool, optional): Add a center point. Defaults to False.

        Raises:
            TypeError: [description]
            TypeError: [description]
            TypeError: [description]

        Returns:
            [type]: [description]

        Yields:
            [type]: [description]
        """
        positions = []
        phi = 2 * np.pi * ((1 + np.sqrt(5)) / 2.0) + spiral_type * np.pi

        start = int(not center)

        length_axis1 = np.abs(m1_stop - m1_start)
        length_axis2 = np.abs(m2_stop - m2_start)
        n_max = int(length_axis1 * length_axis2 * 3.2 / step / step)

        total_shift_x, total_shift_y = self._compute_total_shift()

        for ii in range(start, n_max):
            radius = step * 0.57 * np.sqrt(ii)
            # FOV is restructed below at check pos in range
            # if abs(radius * np.sin(ii * phi)) > length_axis1 / 2:
            #    continue
            # if abs(radius * np.cos(ii * phi)) > length_axis2 / 2:
            #    continue
            x = radius * np.sin(ii * phi)
            y = radius * np.cos(ii * phi)
            if self._lamni_check_pos_in_fov_range_and_circ_fov(x, y):
                positions.extend([(x + total_shift_x * 1000, y + total_shift_y * 1000)])
                # for testing we just shift by center_i and prepare also the setup to center_i
        return np.array(positions)

    def lamni_rotation(self, angle):
        # get last setpoint (cannot be based on pos get because they will deviate slightly)
        lsamrot_current_setpoint = yield from self.stubs.send_rpc_and_wait(
            "lsamrot", "user_setpoint.get"
        )
        if angle == lsamrot_current_setpoint:
            logger.info("No rotation required")
        else:
            logger.info("Rotating to requested angle")
            yield from self.stubs.scan_report_instruction(
                {
                    "readback": {
                        "RID": self.metadata["RID"],
                        "devices": ["lsamrot"],
                        "start": [lsamrot_current_setpoint],
                        "end": [angle],
                    }
                }
            )
            yield from self.stubs.set_and_wait(device=["lsamrot"], positions=[angle])

    def scan_core(self):
        if self.scan_type == "step":
            for ind, pos in self._get_position():
                for self.burst_index in range(self.burst_at_each_point):
                    yield from self._at_each_point(ind, pos)
                self.burst_index = 0
        elif self.scan_type == "fly":
            # use a device message to receive the scan number and
            # scan ID before sending the message to the device server
            yield from self.stubs.kickoff(device="rtx")
            while True:
                yield from self.stubs.read_and_wait(group="primary", wait_group="readout_primary")
                msg = self.device_manager.producer.get(MessageEndpoints.device_status("rt_scan"))
                if msg:
                    status = BECMessage.DeviceStatusMessage.loads(msg)
                    status_id = status.content.get("status", 1)
                    request_id = status.metadata.get("RID")
                    if status_id == 0 and self.metadata.get("RID") == request_id:
                        break
                    if status_id == 2 and self.metadata.get("RID") == request_id:
                        raise ScanAbortion(
                            f"An error occured during the LamNI readout: {status.metadata.get('error')}"
                        )

                time.sleep(1)
                logger.debug("reading monitors")
            # yield from self.device_rpc("rtx", "controller.kickoff")

    def run(self):
        self.initialize()
        yield from self.read_scan_motors()
        self.prepare_positions()
        yield from self._prepare_setup()
        yield from self.open_scan()
        yield from self.stage()
        yield from self.run_baseline_reading()
        yield from self.scan_core()
        yield from self.finalize()
        yield from self.unstage()
        yield from self.cleanup()
