import builtins
import datetime
import os
import subprocess
import threading
import time
from collections import defaultdict
from pathlib import Path

import h5py
import numpy as np
from bec_lib.alarm_handler import AlarmBase
from bec_lib.core import bec_logger
from bec_lib.core.pdf_writer import PDFWriter
from typeguard import typechecked

from bec_client.plugins.cSAXS import epics_get, epics_put, fshclose, fshopen

from .lamni_optics_mixin import LamNIOpticsMixin

logger = bec_logger.logger
bec = builtins.__dict__.get("bec")


class XrayEyeAlign:
    # pixel calibration, multiply to get mm
    # PIXEL_CALIBRATION = 0.2/209 #.2 with binning
    PIXEL_CALIBRATION = 0.2 / 218  # .2 with binning

    def __init__(self, client, lamni) -> None:
        self.client = client
        self.lamni = lamni
        self.device_manager = client.device_manager
        self.scans = client.scans
        self.xeye = self.device_manager.devices.xeye
        self.alignment_values = defaultdict(list)
        self._reset_init_values()
        self.corr_pos_x = []
        self.corr_pos_y = []
        self.corr_angle = []
        self.corr_pos_x_2 = []
        self.corr_pos_y_2 = []
        self.corr_angle_2 = []

    def reset_correction(self):
        self.corr_pos_x = []
        self.corr_pos_y = []
        self.corr_angle = []

    def reset_correction_2(self):
        self.corr_pos_x_2 = []
        self.corr_pos_y_2 = []
        self.corr_angle_2 = []

    def reset_xray_eye_correction(self):
        self.client.delete_global_var("tomo_fit_xray_eye")

    @property
    def tomo_fovx_offset(self):
        val = self.client.get_global_var("tomo_fov_offset")
        if val is None:
            return 0.0
        return val[0] / 1000

    @tomo_fovx_offset.setter
    @typechecked
    def tomo_fovx_offset(self, val: float):
        val_old = self.client.get_global_var("tomo_fov_offset")
        if val_old is None:
            val_old = [0.0, 0.0]
        self.client.set_global_var("tomo_fov_offset", [val * 1000, val_old[1]])

    @property
    def tomo_fovy_offset(self):
        val = self.client.get_global_var("tomo_fov_offset")
        if val is None:
            return 0.0
        return val[1] / 1000

    @tomo_fovy_offset.setter
    @typechecked
    def tomo_fovy_offset(self, val: float):
        val_old = self.client.get_global_var("tomo_fov_offset")
        if val_old is None:
            val_old = [0.0, 0.0]
        self.client.set_global_var("tomo_fov_offset", [val_old[0], val * 1000])

    def _reset_init_values(self):
        self.shift_xy = [0, 0]
        self._xray_fov_xy = [0, 0]

    def save_frame(self):
        epics_put("XOMNYI-XEYE-SAVFRAME:0", 1)

    def update_frame(self):
        epics_put("XOMNYI-XEYE-ACQDONE:0", 0)
        # start live
        epics_put("XOMNYI-XEYE-ACQ:0", 1)
        # wait for start live
        while epics_get("XOMNYI-XEYE-ACQDONE:0") == 0:
            time.sleep(0.5)
            print("waiting for live view to start...")
        fshopen()

        epics_put("XOMNYI-XEYE-ACQDONE:0", 0)

        while epics_get("XOMNYI-XEYE-ACQDONE:0") == 0:
            print("waiting for new frame...")
            time.sleep(0.5)

        time.sleep(0.5)
        # stop live view
        epics_put("XOMNYI-XEYE-ACQ:0", 0)
        time.sleep(1)
        # fshclose
        print("got new frame")

    def _disable_rt_feedback(self):
        self.device_manager.devices.rtx.controller.feedback_disable()

    def _enable_rt_feedback(self):
        self.device_manager.devices.rtx.controller.feedback_enable_with_reset()

    def tomo_rotate(self, val: float):
        # pylint: disable=undefined-variable
        umv(self.device_manager.devices.lsamrot, val)

    def get_tomo_angle(self):
        return self.device_manager.devices.lsamrot.readback.read()["lsamrot"]["value"]

    def update_fov(self, k: int):
        self._xray_fov_xy[0] = max(epics_get(f"XOMNYI-XEYE-XWIDTH_X:{k}"), self._xray_fov_xy[0])
        self._xray_fov_xy[1] = max(0, self._xray_fov_xy[0])

    @property
    def movement_buttons_enabled(self):
        return [epics_get("XOMNYI-XEYE-ENAMVX:0"), epics_get("XOMNYI-XEYE-ENAMVY:0")]

    @movement_buttons_enabled.setter
    def movement_buttons_enabled(self, enabled: bool):
        enabled = int(enabled)
        epics_put("XOMNYI-XEYE-ENAMVX:0", enabled)
        epics_put("XOMNYI-XEYE-ENAMVY:0", enabled)

    def send_message(self, msg: str):
        epics_put("XOMNYI-XEYE-MESSAGE:0.DESC", msg)

    def align(self):
        # reset shift xy and fov params
        self._reset_init_values()
        self.reset_correction()
        self.reset_correction_2()

        # this makes sure we are in a defined state
        self._disable_rt_feedback()

        epics_put("XOMNYI-XEYE-PIXELSIZE:0", self.PIXEL_CALIBRATION)

        self._enable_rt_feedback()

        # initialize
        # disable movement buttons
        self.movement_buttons_enabled = False

        epics_put("XOMNYI-XEYE-ACQ:0", 0)
        self.send_message("please wait...")

        # put sample name
        epics_put("XOMNYI-XEYE-SAMPLENAME:0.DESC", "Let us LAMNI...")

        # first step
        self._disable_rt_feedback()
        k = 0

        # move zone plate in, eye in to get beam position
        self.lamni.lfzp_in()

        self.update_frame()

        # enable submit buttons
        self.movement_buttons_enabled = False
        epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
        epics_put("XOMNYI-XEYE-STEP:0", 0)
        self.send_message("Submit center value of FZP.")

        while True:
            if epics_get("XOMNYI-XEYE-SUBMIT:0") == 1:
                val_x = epics_get(f"XOMNYI-XEYE-XVAL_X:{k}") * self.PIXEL_CALIBRATION  # in mm
                val_y = epics_get(f"XOMNYI-XEYE-YVAL_Y:{k}") * self.PIXEL_CALIBRATION  # in mm
                self.alignment_values[k] = [val_x, val_y]
                print(
                    f"Clicked position {k}: x {self.alignment_values[k][0]}, y {self.alignment_values[k][1]}"
                )

                if k == 0:  # received center value of FZP
                    self.send_message("please wait ...")
                    # perform movement: FZP out, Sample in
                    self.lamni.loptics_out()
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    print("Moving sample in, FZP out")

                    self._disable_rt_feedback()
                    time.sleep(0.3)
                    self._enable_rt_feedback()
                    time.sleep(0.3)

                    # zero is now at the center
                    self.update_frame()
                    self.send_message("Go and find the sample")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
                    self.movement_buttons_enabled = True

                elif (
                    k == 1
                ):  # received sample center value at samroy 0 ie the final base shift values
                    msg = f"Base shift values from movement are x {self.shift_xy[0]}, y {self.shift_xy[1]}"
                    print(msg)
                    logger.info(msg)
                    self.shift_xy[0] += (
                        self.alignment_values[0][0] - self.alignment_values[1][0]
                    ) * 1000
                    self.shift_xy[1] += (
                        self.alignment_values[1][1] - self.alignment_values[0][1]
                    ) * 1000
                    print(
                        f"Base shift values from movement and clicked position are x {self.shift_xy[0]}, y {self.shift_xy[1]}"
                    )

                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000,
                        self.shift_xy[1] / 1000,
                        self.get_tomo_angle(),
                    ).wait()

                    self.send_message("please wait ...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    time.sleep(1)

                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000,
                        self.shift_xy[1] / 1000,
                        self.get_tomo_angle(),
                    ).wait()

                    epics_put("XOMNYI-XEYE-ANGLE:0", self.get_tomo_angle())
                    self.update_frame()
                    self.send_message("Submit sample center and FOV (0 deg)")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
                    self.update_fov(k)

                elif 1 < k < 10:  # received sample center value at samroy 0 ... 315
                    self.send_message("please wait ...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button

                    # we swtich feedback off before rotating to not have it on and off again later for smooth operation
                    self._disable_rt_feedback()
                    self.tomo_rotate((k - 1) * 45 - 45 / 2)
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000,
                        self.shift_xy[1] / 1000,
                        self.get_tomo_angle(),
                    ).wait()
                    self._disable_rt_feedback()
                    self.tomo_rotate((k - 1) * 45)
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000,
                        self.shift_xy[1] / 1000,
                        self.get_tomo_angle(),
                    ).wait()

                    epics_put("XOMNYI-XEYE-ANGLE:0", self.get_tomo_angle())
                    self.update_frame()
                    self.send_message("Submit sample center")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", 0)
                    epics_put("XOMNYI-XEYE-ENAMVX:0", 1)
                    self.update_fov(k)

                elif k == 10:  # received sample center value at samroy 270 and done
                    self.send_message("done...")
                    epics_put("XOMNYI-XEYE-SUBMIT:0", -1)  # disable submit button
                    self.movement_buttons_enabled = False
                    self.update_fov(k)
                    break

                k += 1
                epics_put("XOMNYI-XEYE-STEP:0", k)
            if k < 2:
                # allow movements, store movements to calculate center
                _xrayeyalignmvx = epics_get("XOMNYI-XEYE-MVX:0")
                _xrayeyalignmvy = epics_get("XOMNYI-XEYE-MVY:0")
                if _xrayeyalignmvx != 0 or _xrayeyalignmvy != 0:
                    self.shift_xy[0] = self.shift_xy[0] + _xrayeyalignmvx
                    self.shift_xy[1] = self.shift_xy[1] + _xrayeyalignmvy
                    self.scans.lamni_move_to_scan_center(
                        self.shift_xy[0] / 1000,
                        self.shift_xy[1] / 1000,
                        self.get_tomo_angle(),
                    ).wait()
                    print(
                        f"Current center horizontal {self.shift_xy[0]} vertical {self.shift_xy[1]}"
                    )
                    epics_put("XOMNYI-XEYE-MVY:0", 0)
                    epics_put("XOMNYI-XEYE-MVX:0", 0)
                    self.update_frame()

            time.sleep(0.2)

        self.write_output()
        fovx = self._xray_fov_xy[0] * self.PIXEL_CALIBRATION * 1000 / 2
        fovy = self._xray_fov_xy[1] * self.PIXEL_CALIBRATION * 1000 / 2
        print(
            f"The largest field of view from the xrayeyealign was \nfovx = {fovx:.0f} microns, fovy = {fovy:.0f} microns"
        )
        print("Use matlab routine to fit the current alignment...")

        print(
            f"This additional shift is applied to the base shift values\n which are x {self.shift_xy[0]}, y {self.shift_xy[1]}"
        )

        self._disable_rt_feedback()

        self.tomo_rotate(0)

        print(
            "\n\nNEXT LOAD ALIGNMENT PARAMETERS\nby running lamni.align.read_xray_eye_correction()\n"
        )

        self.client.set_global_var("tomo_fov_offset", self.shift_xy)

    def write_output(self):
        with open(
            os.path.expanduser("~/Data10/specES1/internal/xrayeye_alignmentvalues"), "w"
        ) as alignment_values_file:
            alignment_values_file.write(f"angle\thorizontal\tvertical\n")
            for k in range(2, 11):
                fovx_offset = (self.alignment_values[0][0] - self.alignment_values[k][0]) * 1000
                fovy_offset = (self.alignment_values[k][1] - self.alignment_values[0][1]) * 1000
                print(
                    f"Writing to file new alignment: number {k}, value x {fovx_offset}, y {fovy_offset}"
                )
                alignment_values_file.write(f"{(k-2)*45}\t{fovx_offset}\t{fovy_offset}\n")

    def read_xray_eye_correction(self, dir_path=os.path.expanduser("~/Data10/specES1/internal/")):
        tomo_fit_xray_eye = np.zeros((2, 3))
        with open(os.path.join(dir_path, "ptychotomoalign_Ax.txt"), "r") as file:
            tomo_fit_xray_eye[0][0] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Bx.txt"), "r") as file:
            tomo_fit_xray_eye[0][1] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Cx.txt"), "r") as file:
            tomo_fit_xray_eye[0][2] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Ay.txt"), "r") as file:
            tomo_fit_xray_eye[1][0] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_By.txt"), "r") as file:
            tomo_fit_xray_eye[1][1] = file.readline()

        with open(os.path.join(dir_path, "ptychotomoalign_Cy.txt"), "r") as file:
            tomo_fit_xray_eye[1][2] = file.readline()

        self.client.set_global_var("tomo_fit_xray_eye", tomo_fit_xray_eye.tolist())
        # x amp, phase, offset, y amp, phase, offset
        #  0 0    0 1    0 2     1 0    1 1    1 2

        print("New alignment parameters loaded from X-ray eye")
        print(
            f"X Amplitude {tomo_fit_xray_eye[0][0]},"
            f"X Phase {tomo_fit_xray_eye[0][1]}, "
            f"X Offset {tomo_fit_xray_eye[0][2]},"
            f"Y Amplitude {tomo_fit_xray_eye[1][0]},"
            f"Y Phase {tomo_fit_xray_eye[1][1]},"
            f"Y Offset {tomo_fit_xray_eye[1][2]}"
        )

    def lamni_compute_additional_correction_xeye_mu(self, angle):
        tomo_fit_xray_eye = self.client.get_global_var("tomo_fit_xray_eye")
        if tomo_fit_xray_eye is None:
            print("Not applying any additional correction. No x-ray eye data available.\n")
            return (0, 0)

        # x amp, phase, offset, y amp, phase, offset
        #  0 0    0 1    0 2     1 0    1 1    1 2
        correction_x = (
            tomo_fit_xray_eye[0][0] * np.sin(np.radians(angle) + tomo_fit_xray_eye[0][1])
            + tomo_fit_xray_eye[0][2]
        ) / 1000
        correction_y = (
            tomo_fit_xray_eye[1][0] * np.sin(np.radians(angle) + tomo_fit_xray_eye[1][1])
            + tomo_fit_xray_eye[1][2]
        ) / 1000

        print(f"Xeye correction x {correction_x}, y {correction_y} for angle {angle}\n")
        return (correction_x, correction_y)

    def compute_additional_correction(self, angle):
        if not self.corr_pos_x:
            print("Not applying any additional correction. No data available.\n")
            return (0, 0)

        # find index of closest angle
        for j, _ in enumerate(self.corr_pos_x):
            newangledelta = np.fabs(self.corr_angle[j] - angle)
            if j == 0:
                angledelta = newangledelta
                additional_correction_shift_x = self.corr_pos_x[j]
                additional_correction_shift_y = self.corr_pos_y[j]
                continue

            if newangledelta < angledelta:
                additional_correction_shift_x = self.corr_pos_x[j]
                additional_correction_shift_y = self.corr_pos_y[j]
                angledelta = newangledelta

        if additional_correction_shift_x == 0 and angle < self.corr_angle[0]:
            additional_correction_shift_x = self.corr_pos_x[0]
            additional_correction_shift_y = self.corr_pos_y[0]

        if additional_correction_shift_x == 0 and angle > self.corr_angle[-1]:
            additional_correction_shift_x = self.corr_pos_x[-1]
            additional_correction_shift_y = self.corr_pos_y[-1]
        print(
            f"Additional correction shifts: {additional_correction_shift_x} {additional_correction_shift_y}"
        )
        return (additional_correction_shift_x, additional_correction_shift_y)

    def read_additional_correction(self, correction_file: str):
        with open(correction_file, "r") as f:
            num_elements = f.readline()
            int_num_elements = int(num_elements.split(" ")[2])
            print(int_num_elements)
            corr_pos_x = []
            corr_pos_y = []
            corr_angle = []
            for j in range(0, int_num_elements * 3):
                line = f.readline()
                value = line.split(" ")[2]
                name = line.split(" ")[0].split("[")[0]
                if name == "corr_pos_x":
                    corr_pos_x.append(float(value) / 1000)
                elif name == "corr_pos_y":
                    corr_pos_y.append(float(value) / 1000)
                elif name == "corr_angle":
                    corr_angle.append(float(value))
        self.corr_pos_x = corr_pos_x
        self.corr_pos_y = corr_pos_y
        self.corr_angle = corr_angle
        return

    def compute_additional_correction_2(self, angle):
        if not self.corr_pos_x_2:
            print("Not applying any additional secondary correction. No data available.\n")
            return (0, 0)

        # find index of closest angle
        for j, _ in enumerate(self.corr_pos_x_2):
            newangledelta = np.fabs(self.corr_angle_2[j] - angle)
            if j == 0:
                angledelta = newangledelta
                additional_correction_shift_x = self.corr_pos_x_2[j]
                additional_correction_shift_y = self.corr_pos_y_2[j]
                continue

            if newangledelta < angledelta:
                additional_correction_shift_x = self.corr_pos_x_2[j]
                additional_correction_shift_y = self.corr_pos_y_2[j]
                angledelta = newangledelta

        if additional_correction_shift_x == 0 and angle < self.corr_angle_2[0]:
            additional_correction_shift_x = self.corr_pos_x_2[0]
            additional_correction_shift_y = self.corr_pos_y_2[0]

        if additional_correction_shift_x == 0 and angle > self.corr_angle_2[-1]:
            additional_correction_shift_x = self.corr_pos_x_2[-1]
            additional_correction_shift_y = self.corr_pos_y_2[-1]
        print(
            f"Additional correction shifts 2: {additional_correction_shift_x} {additional_correction_shift_y}"
        )
        return (additional_correction_shift_x, additional_correction_shift_y)

    def read_additional_correction_2(self, correction_file: str):
        with open(correction_file, "r") as f:
            num_elements = f.readline()
            int_num_elements = int(num_elements.split(" ")[2])
            print(int_num_elements)
            corr_pos_x = []
            corr_pos_y = []
            corr_angle = []
            for j in range(0, int_num_elements * 3):
                line = f.readline()
                value = line.split(" ")[2]
                name = line.split(" ")[0].split("[")[0]
                if name == "corr_pos_x":
                    corr_pos_x.append(float(value) / 1000)
                elif name == "corr_pos_y":
                    corr_pos_y.append(float(value) / 1000)
                elif name == "corr_angle":
                    corr_angle.append(float(value))
        self.corr_pos_x_2 = corr_pos_x
        self.corr_pos_y_2 = corr_pos_y
        self.corr_angle_2 = corr_angle
        return


class LamNI(LamNIOpticsMixin):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.align = XrayEyeAlign(client, self)

        self.check_shutter = True
        self.check_light_available = True
        self.check_fofb = True
        self._check_msgs = []
        self.tomo_id = -1
        self.special_angles = []
        self.special_angle_repeats = 20
        self.special_angle_tolerance = 20
        self._current_special_angles = []
        self._beam_is_okay = True
        self._stop_beam_check_event = None
        self.beam_check_thread = None

    def get_beamline_checks_enabled(self):
        print(
            f"Shutter: {self.check_shutter}\nFOFB: {self.check_fofb}\nLight available: {self.check_light_available}"
        )

    @property
    def beamline_checks_enabled(self):
        return {
            "shutter": self.check_shutter,
            "fofb": self.check_fofb,
            "light available": self.check_light_available,
        }

    @beamline_checks_enabled.setter
    def beamline_checks_enabled(self, val: bool):
        self.check_shutter = val
        self.check_light_available = val
        self.check_fofb = val
        self.get_beamline_checks_enabled()

    def set_special_angles(self, angles: list, repeats: int = 20, tolerance: float = 0.5):
        """Set the special angles for a tomo

        Args:
            angles (list): List of special angles
            repeats (int, optional): Number of repeats at a special angle. Defaults to 20.
            tolerance (float, optional): Number of repeats at a special angle. Defaults to 0.5.

        """
        self.special_angles = angles
        self.special_angle_repeats = repeats
        self.special_angle_tolerance = tolerance

    def remove_special_angles(self):
        """Remove the special angles and set the number of repeats to 1"""
        self.special_angles = []
        self.special_angle_repeats = 1

    @property
    def tomo_shellstep(self):
        val = self.client.get_global_var("tomo_shellstep")
        if val is None:
            return 1
        return val

    @tomo_shellstep.setter
    def tomo_shellstep(self, val: float):
        self.client.set_global_var("tomo_shellstep", val)

    @property
    def tomo_circfov(self):
        val = self.client.get_global_var("tomo_circfov")
        if val is None:
            return 0.0
        return val

    @tomo_circfov.setter
    def tomo_circfov(self, val: float):
        self.client.set_global_var("tomo_circfov", val)

    @property
    def tomo_countingtime(self):
        val = self.client.get_global_var("tomo_countingtime")
        if val is None:
            return 0.1
        return val

    @tomo_countingtime.setter
    def tomo_countingtime(self, val: float):
        self.client.set_global_var("tomo_countingtime", val)

    @property
    def manual_shift_x(self):
        val = self.client.get_global_var("manual_shift_x")
        if val is None:
            return 0.0
        return val

    @manual_shift_x.setter
    def manual_shift_x(self, val: float):
        self.client.set_global_var("manual_shift_x", val)

    @property
    def manual_shift_y(self):
        val = self.client.get_global_var("manual_shift_y")
        if val is None:
            return 0.0
        return val

    @manual_shift_y.setter
    def manual_shift_y(self, val: float):
        self.client.set_global_var("manual_shift_y", val)

    @property
    def lamni_piezo_range_x(self):
        val = self.client.get_global_var("lamni_piezo_range_x")
        if val is None:
            return 20
        return val

    @lamni_piezo_range_x.setter
    def lamni_piezo_range_x(self, val: float):
        if dev.rtx.user_parameter and dev.rtx.user_parameter.get("large_range_scan", True):
            self.client.set_global_var("lamni_piezo_range_x", val)
            return
        if val > 80:
            raise ValueError("Piezo range cannot be larger than 80 um.")
        self.client.set_global_var("lamni_piezo_range_x", val)

    @property
    def lamni_piezo_range_y(self):
        val = self.client.get_global_var("lamni_piezo_range_y")
        if val is None:
            return 20
        return val

    @lamni_piezo_range_y.setter
    def lamni_piezo_range_y(self, val: float):
        if dev.rtx.user_parameter and dev.rtx.user_parameter.get("large_range_scan", True):
            self.client.set_global_var("lamni_piezo_range_y", val)
            return
        if val > 80:
            raise ValueError("Piezo range cannot be larger than 80 um.")
        self.client.set_global_var("lamni_piezo_range_y", val)

    @property
    def corridor_size(self):
        val = self.client.get_global_var("corridor_size")
        if val is None:
            val = -1
        return val

    @corridor_size.setter
    def corridor_size(self, val: float):
        self.client.set_global_var("corridor_size", val)

    @property
    def lamni_stitch_x(self):
        val = self.client.get_global_var("lamni_stitch_x")
        if val is None:
            return 0
        return val

    @lamni_stitch_x.setter
    @typechecked
    def lamni_stitch_x(self, val: int):
        self.client.set_global_var("lamni_stitch_x", val)

    @property
    def lamni_stitch_y(self):
        val = self.client.get_global_var("lamni_stitch_y")
        if val is None:
            return 0
        return val

    @lamni_stitch_y.setter
    @typechecked
    def lamni_stitch_y(self, val: int):
        self.client.set_global_var("lamni_stitch_y", val)

    @property
    def ptycho_reconstruct_foldername(self):
        val = self.client.get_global_var("ptycho_reconstruct_foldername")
        if val is None:
            return "ptycho_reconstruct"
        return val

    @ptycho_reconstruct_foldername.setter
    def ptycho_reconstruct_foldername(self, val: str):
        self.client.set_global_var("ptycho_reconstruct_foldername", val)

    @property
    def tomo_angle_stepsize(self):
        val = self.client.get_global_var("tomo_angle_stepsize")
        if val is None:
            return 10.0
        return val

    @tomo_angle_stepsize.setter
    def tomo_angle_stepsize(self, val: float):
        self.client.set_global_var("tomo_angle_stepsize", val)

    @property
    def tomo_stitch_overlap(self):
        val = self.client.get_global_var("tomo_stitch_overlap")
        if val is None:
            return 0.2
        return val

    @tomo_stitch_overlap.setter
    def tomo_stitch_overlap(self, val: float):
        self.client.set_global_var("tomo_stitch_overlap", val)

    @property
    def sample_name(self):
        val = self.client.get_global_var("sample_name")
        if val is None:
            return "bec_test_sample"
        return val

    @sample_name.setter
    @typechecked
    def sample_name(self, val: str):
        self.client.set_global_var("sample_name", val)

    def write_to_spec_log(self, content):
        try:
            with open(
                os.path.expanduser(
                    "~/Data10/specES1/log-files/specES1_started_2022_11_30_1313.log"
                ),
                "a",
            ) as log_file:
                log_file.write(content)
        except Exception:
            logger.warning("Failed to write to spec log file (omny web page).")

    def write_to_scilog(self, content, tags: list = None):
        try:
            if tags is not None:
                tags.append("BEC")
            else:
                tags = ["BEC"]
            msg = bec.logbook.LogbookMessage()
            msg.add_text(content).add_tag(tags)
            self.client.logbook.send_logbook_message(msg)
        except Exception:
            logger.warning("Failed to write to scilog.")

    def tomo_scan_projection(self, angle: float):
        scans = builtins.__dict__.get("scans")

        additional_correction = self.align.compute_additional_correction(angle)
        additional_correction_2 = self.align.compute_additional_correction_2(angle)
        correction_xeye_mu = self.align.lamni_compute_additional_correction_xeye_mu(angle)

        self._current_scan_list = []

        for stitch_x in range(-self.lamni_stitch_x, self.lamni_stitch_x + 1):
            for stitch_y in range(-self.lamni_stitch_y, self.lamni_stitch_y + 1):
                # pylint: disable=undefined-variable
                self._current_scan_list.append(bec.queue.next_scan_number)
                logger.info(
                    f"scans.lamni_fermat_scan(fov_size=[{self.lamni_piezo_range_x},{self.lamni_piezo_range_y}], step={self.tomo_shellstep}, stitch_x={0}, stitch_y={0}, stitch_overlap={1},"
                    f"center_x={self.align.tomo_fovx_offset}, center_y={self.align.tomo_fovy_offset}, "
                    f"shift_x={self.manual_shift_x+correction_xeye_mu[0]-additional_correction[0]-additional_correction_2[0]}, "
                    f"shift_y={self.manual_shift_y+correction_xeye_mu[1]-additional_correction[1]-additional_correction_2[1]}, "
                    f"fov_circular={self.tomo_circfov}, angle={angle}, scan_type='fly')"
                )
                log_message = f"{str(datetime.datetime.now())}: LamNI scan projection at angle {angle}, scan number {bec.queue.next_scan_number}.\n"
                self.write_to_spec_log(log_message)
                # self.write_to_scilog(log_message, ["BEC_scans", self.sample_name])
                corridor_size = self.corridor_size if self.corridor_size > 0 else None
                scans.lamni_fermat_scan(
                    fov_size=[self.lamni_piezo_range_x, self.lamni_piezo_range_y],
                    step=self.tomo_shellstep,
                    stitch_x=stitch_x,
                    stitch_y=stitch_y,
                    stitch_overlap=self.tomo_stitch_overlap,
                    center_x=self.align.tomo_fovx_offset,
                    center_y=self.align.tomo_fovy_offset,
                    shift_x=(
                        self.manual_shift_x
                        + correction_xeye_mu[0]
                        - additional_correction[0]
                        - additional_correction_2[0]
                    ),
                    shift_y=(
                        self.manual_shift_y
                        + correction_xeye_mu[1]
                        - additional_correction[1]
                        - additional_correction_2[1]
                    ),
                    fov_circular=self.tomo_circfov,
                    angle=angle,
                    scan_type="fly",
                    exp_time=self.tomo_countingtime,
                    optim_trajectory_corridor=corridor_size,
                )

    def _run_beamline_checks(self):
        msgs = []
        dev = builtins.__dict__.get("dev")
        try:
            if self.check_shutter:
                shutter_val = dev.x12sa_es1_shutter_status.read(cached=True)
                if shutter_val["value"].lower() != "open":
                    self._beam_is_okay = False
                    msgs.append("Check beam failed: Shutter is closed.")
            if self.check_light_available:
                machine_status = dev.sls_machine_status.read(cached=True)
                if machine_status["value"] not in [
                    "Light Available",
                    "Light-Available",
                ]:
                    self._beam_is_okay = False
                    msgs.append("Check beam failed: Light not available.")
            if self.check_fofb:
                fast_orbit_feedback = dev.sls_fast_orbit_feedback.read(cached=True)
                if fast_orbit_feedback["value"] != "running":
                    self._beam_is_okay = False
                    msgs.append("Check beam failed: Fast orbit feedback is not running.")
        except Exception:
            logger.warning("Failed to check beam.")
        return msgs

    def _check_beam(self):
        while not self._stop_beam_check_event.is_set():
            self._check_msgs = self._run_beamline_checks()

            if not self._beam_is_okay:
                self._stop_beam_check_event.set()
            time.sleep(1)

    def _start_beam_check(self):
        self._beam_is_okay = True
        self._stop_beam_check_event = threading.Event()

        self.beam_check_thread = threading.Thread(target=self._check_beam, daemon=True)
        self.beam_check_thread.start()

    def _was_beam_okay(self):
        self._stop_beam_check_event.set()
        self.beam_check_thread.join()
        return self._beam_is_okay

    def _print_beamline_checks(self):
        for msg in self._check_msgs:
            logger.warning(msg)

    def _wait_for_beamline_checks(self):
        self._print_beamline_checks()
        try:
            msg = bec.logbook.LogbookMessage()
            msg.add_text(
                f"<p><mark class='pen-red'><strong>Beamline checks failed at {str(datetime.datetime.now())}: {''.join(self._check_msgs)}</strong></mark></p>"
            ).add_tag(["BEC", "beam_check"])
            self.client.logbook.send_logbook_message(msg)
        except Exception:
            logger.warning("Failed to send update to SciLog.")

        while True:
            self._beam_is_okay = True
            self._check_msgs = self._run_beamline_checks()
            if self._beam_is_okay:
                break
            self._print_beamline_checks()
            time.sleep(1)

        try:
            msg = bec.logbook.LogbookMessage()
            msg.add_text(
                f"<p><mark class='pen-red'><strong>Operation resumed at {str(datetime.datetime.now())}.</strong></mark></p>"
            ).add_tag(["BEC", "beam_check"])
            self.client.logbook.send_logbook_message(msg)
        except Exception:
            logger.warning("Failed to send update to SciLog.")

    def add_sample_database(
        self,
        samplename,
        date,
        eaccount,
        scan_number,
        setup,
        sample_additional_info,
        user,
    ):
        """Add a sample to the omny sample database. This also retrieves the tomo id."""
        subprocess.run(
            f"wget --user=omny --password=samples -q -O /tmp/currsamplesnr.txt 'https://omny.web.psi.ch/samples/newmeasurement.php?sample={samplename}&date={date}&eaccount={eaccount}&scannr={scan_number}&setup={setup}&additional={sample_additional_info}&user={user}'",
            shell=True,
        )
        with open("/tmp/currsamplesnr.txt") as tomo_number_file:
            tomo_number = int(tomo_number_file.read())
        return tomo_number

    def _at_each_angle(self, angle: float) -> None:
        self.tomo_scan_projection(angle)
        self.tomo_reconstruct()

        ### XMCD ###
        # 2 projections, 1 for each polarization state
        # cp()
        # self.tomo_scan_projection(angle)
        # self.tomo_reconstruct()
        # cm()
        # self.tomo_scan_projection(angle)
        # self.tomo_reconstruct()

    def sub_tomo_scan(self, subtomo_number, start_angle=None):
        """start a subtomo"""
        dev = builtins.__dict__.get("dev")
        bec = builtins.__dict__.get("bec")
        if self.tomo_id > 0:
            tags = ["BEC_subtomo", self.sample_name, f"tomo_id_{self.tomo_id}"]
        else:
            tags = ["BEC_subtomo", self.sample_name]
        self.write_to_scilog(
            f"Starting subtomo: {subtomo_number}. First scan number: {bec.queue.next_scan_number}.",
            tags,
        )

        if start_angle is None:
            if subtomo_number == 1:
                start_angle = 0
            elif subtomo_number == 2:
                start_angle = self.tomo_angle_stepsize / 8.0 * 4
            elif subtomo_number == 3:
                start_angle = self.tomo_angle_stepsize / 8.0 * 2
            elif subtomo_number == 4:
                start_angle = self.tomo_angle_stepsize / 8.0 * 6
            elif subtomo_number == 5:
                start_angle = self.tomo_angle_stepsize / 8.0 * 1
            elif subtomo_number == 6:
                start_angle = self.tomo_angle_stepsize / 8.0 * 5
            elif subtomo_number == 7:
                start_angle = self.tomo_angle_stepsize / 8.0 * 3
            elif subtomo_number == 8:
                start_angle = self.tomo_angle_stepsize / 8.0 * 7

        # _tomo_shift_angles (potential global variable)
        _tomo_shift_angles = 0
        angle_end = start_angle + 360
        for angle in np.linspace(
            start_angle + _tomo_shift_angles,
            angle_end,
            num=int(360 / self.tomo_angle_stepsize) + 1,
            endpoint=True,
        ):
            successful = False
            error_caught = False
            if 0 <= angle < 360.05:
                print(f"Starting LamNI scan for angle {angle}")
                while not successful:
                    self._start_beam_check()
                    if not self.special_angles:
                        self._current_special_angles = []
                    if self._current_special_angles:
                        next_special_angle = self._current_special_angles[0]
                        if np.isclose(angle, next_special_angle, atol=0.5):
                            self._current_special_angles.pop(0)
                            num_repeats = self.special_angle_repeats
                    else:
                        num_repeats = 1
                    try:
                        start_scan_number = bec.queue.next_scan_number
                        for i in range(num_repeats):
                            self._at_each_angle(angle)
                        error_caught = False
                    except AlarmBase as exc:
                        if exc.alarm_type == "TimeoutError":
                            bec.queue.request_queue_reset()
                            time.sleep(2)
                            error_caught = True
                        else:
                            raise exc

                    if self._was_beam_okay() and not error_caught:
                        successful = True
                    else:
                        self._wait_for_beamline_checks()
                end_scan_number = bec.queue.next_scan_number
                for scan_nr in range(start_scan_number, end_scan_number):
                    self._write_tomo_scan_number(scan_nr, angle, subtomo_number)

    def _write_tomo_scan_number(self, scan_number: int, angle: float, subtomo_number: int) -> None:
        tomo_scan_numbers_file = os.path.expanduser(
            "~/Data10/specES1/dat-files/tomography_scannumbers.txt"
        )
        with open(tomo_scan_numbers_file, "a+") as out_file:
            # pylint: disable=undefined-variable
            out_file.write(
                f"{scan_number} {angle} {dev.lsamrot.read()['lsamrot']['value']:.3f} {self.tomo_id} {subtomo_number} {0} {'lamni'}\n"
            )

    def tomo_scan(self, subtomo_start=1, start_angle=None):
        """start a tomo scan"""
        bec = builtins.__dict__.get("bec")
        scans = builtins.__dict__.get("scans")
        self._current_special_angles = self.special_angles.copy()

        if subtomo_start == 1 and start_angle is None:
            # pylint: disable=undefined-variable
            self.tomo_id = self.add_sample_database(
                self.sample_name,
                str(datetime.date.today()),
                bec.active_account.decode(),
                bec.queue.next_scan_number,
                "lamni",
                "test additional info",
                "BEC",
            )
            self.write_pdf_report()
        with scans.dataset_id_on_hold:
            for ii in range(subtomo_start, 9):
                self.sub_tomo_scan(ii, start_angle=start_angle)
                start_angle = None

    def tomo_parameters(self):
        """print and update the tomo parameters"""
        print("Current settings:")
        print(f"Counting time           <ctime>  =  {self.tomo_countingtime} s")
        print(f"Stepsize microns         <step>  =  {self.tomo_shellstep}")
        print(
            f"Piezo range (max 80)  <microns>  =  {self.lamni_piezo_range_x}, {self.lamni_piezo_range_y}"
        )
        print(f"Stitching number x,y             =  {self.lamni_stitch_x}, {self.lamni_stitch_y}")
        print(f"Stitching overlap                =  {self.tomo_stitch_overlap}")
        print(f"Circuilar FOV diam    <microns>  =  {self.tomo_circfov}")
        print(f"Reconstruction queue name        =  {self.ptycho_reconstruct_foldername}")
        print(
            "For information, fov offset is rotating and finding the ROI, manual shift moves rotation center"
        )
        print(f"   _tomo_fovx_offset       <mm>  =  {self.align.tomo_fovx_offset}")
        print(f"   _tomo_fovy_offset       <mm>  =  {self.align.tomo_fovy_offset}")
        print(f"   _manual_shift_x         <mm>  =  {self.manual_shift_x}")
        print(f"   _manual_shift_y         <mm>  =  {self.manual_shift_y}")
        print(f"Angular step within sub-tomogram:   {self.tomo_angle_stepsize} degrees")
        print(f"Resulting in number of projections: {360/self.tomo_angle_stepsize*8}")
        print(f"Sample name: {self.sample_name}\n")

        user_input = input("Are these parameters correctly set for your scan? ")
        if user_input == "y":
            print("good then")
        else:
            self.tomo_countingtime = self._get_val("<ctime> s", self.tomo_countingtime, float)
            self.tomo_shellstep = self._get_val("<step size> um", self.tomo_shellstep, float)
            self.lamni_piezo_range_x = self._get_val(
                "<piezo range X (max 80)> um", self.lamni_piezo_range_x, float
            )
            self.lamni_piezo_range_y = self._get_val(
                "<piezo range Y (max 80)> um", self.lamni_piezo_range_y, float
            )
            self.lamni_stitch_x = self._get_val("<stitch X>", self.lamni_stitch_x, int)
            self.lamni_stitch_y = self._get_val("<stitch Y>", self.lamni_stitch_y, int)
            self.tomo_circfov = self._get_val("<circular FOV> um", self.tomo_circfov, float)
            self.ptycho_reconstruct_foldername = self._get_val(
                "Reconstruction queue ", self.ptycho_reconstruct_foldername, str
            )
            tomo_numberofprojections = self._get_val(
                "Number of projections", 360 / self.tomo_angle_stepsize * 8, int
            )

            print(f"The angular step will be {360/tomo_numberofprojections}")
            self.tomo_angle_stepsize = 360 / tomo_numberofprojections * 8
            print(f"The angular step in a subtomogram it will be {self.tomo_angle_stepsize}")
            self.sample_name = self._get_val("sample name", self.sample_name, str)

    @staticmethod
    def _get_val(msg: str, default_value, data_type):
        return data_type(input(f"{msg} ({default_value}): ") or default_value)

    def tomo_reconstruct(self, base_path="~/Data10/specES1"):
        """write the tomo reconstruct file for the reconstruction queue"""
        bec = builtins.__dict__.get("bec")
        base_path = os.path.expanduser(base_path)
        ptycho_queue_path = Path(os.path.join(base_path, self.ptycho_reconstruct_foldername))
        ptycho_queue_path.mkdir(parents=True, exist_ok=True)

        # pylint: disable=undefined-variable
        last_scan_number = bec.queue.next_scan_number - 1
        ptycho_queue_file = os.path.abspath(
            os.path.join(ptycho_queue_path, f"scan_{last_scan_number:05d}.dat")
        )
        with open(ptycho_queue_file, "w") as queue_file:
            scans = " ".join([str(scan) for scan in self._current_scan_list])
            queue_file.write(f"p.scan_number {scans}\n")
            queue_file.write(f"p.check_nextscan_started 1\n")

    def write_pdf_report(self):
        """create and write the pdf report with the current LamNI settings"""
        dev = builtins.__dict__.get("dev")
        header = (
            " \n" * 3
            + "  :::            :::       :::   :::   ::::    ::: ::::::::::: \n"
            + "  :+:          :+: :+:    :+:+: :+:+:  :+:+:   :+:     :+:     \n"
            + "  +:+         +:+   +:+  +:+ +:+:+ +:+ :+:+:+  +:+     +:+     \n"
            + "  +#+        +#++:++#++: +#+  +:+  +#+ +#+ +:+ +#+     +#+     \n"
            + "  +#+        +#+     +#+ +#+       +#+ +#+  +#+#+#     +#+     \n"
            + "  #+#        #+#     #+# #+#       #+# #+#   #+#+#     #+#     \n"
            + "  ########## ###     ### ###       ### ###    #### ########### \n"
        )
        padding = 20
        piezo_range = f"{self.lamni_piezo_range_x:.2f}/{self.lamni_piezo_range_y:.2f}"
        stitching = f"{self.lamni_stitch_x:.2f}/{self.lamni_stitch_y:.2f}"
        dataset_id = str(self.client.queue.next_dataset_number)
        content = [
            f"{'Sample Name:':<{padding}}{self.sample_name:>{padding}}\n",
            f"{'Measurement ID:':<{padding}}{str(self.tomo_id):>{padding}}\n",
            f"{'Dataset ID:':<{padding}}{dataset_id:>{padding}}\n",
            f"{'Sample Info:':<{padding}}{'Sample Info':>{padding}}\n",
            f"{'e-account:':<{padding}}{str(self.client.username):>{padding}}\n",
            f"{'Number of projections:':<{padding}}{int(360 / self.tomo_angle_stepsize * 8):>{padding}}\n",
            f"{'First scan number:':<{padding}}{self.client.queue.next_scan_number:>{padding}}\n",
            f"{'Last scan number approx.:':<{padding}}{self.client.queue.next_scan_number + int(360 / self.tomo_angle_stepsize * 8) + 10:>{padding}}\n",
            f"{'Current photon energy:':<{padding}}{dev.mokev.read(cached=True)['value']:>{padding}.4f}\n",
            f"{'Exposure time:':<{padding}}{self.tomo_countingtime:>{padding}.2f}\n",
            f"{'Fermat spiral step size:':<{padding}}{self.tomo_shellstep:>{padding}.2f}\n",
            f"{'Piezo range (FOV sample plane):':<{padding}}{piezo_range:>{padding}}\n",
            f"{'Restriction to circular FOV:':<{padding}}{self.tomo_circfov:>{padding}.2f}\n",
            f"{'Stitching:':<{padding}}{stitching:>{padding}}\n",
            f"{'Number of individual sub-tomograms:':<{padding}}{8:>{padding}}\n",
            f"{'Angular step within sub-tomogram:':<{padding}}{self.tomo_angle_stepsize:>{padding}.2f}\n",
        ]
        content = "".join(content)
        user_target = os.path.expanduser(f"~/Data10/documentation/tomo_scan_ID_{self.tomo_id}.pdf")
        with PDFWriter(user_target) as file:
            file.write(header)
            file.write(content)
        subprocess.run(
            "xterm /work/sls/spec/local/XOMNY/bin/upload/upload_last_pon.sh &",
            shell=True,
        )
        # status = subprocess.run(f"cp /tmp/spec-e20131-specES1.pdf {user_target}", shell=True)
        msg = bec.logbook.LogbookMessage()
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LamNI_logo.png")
        msg.add_file(logo_path).add_text("".join(content).replace("\n", "</p><p>")).add_tag(
            [
                "BEC",
                "tomo_parameters",
                f"dataset_id_{dataset_id}",
                "LamNI",
                self.sample_name,
            ]
        )
        self.client.logbook.send_logbook_message(msg)


class MagLamNI(LamNI):
    def sub_tomo_scan(self, subtomo_number, start_angle=None):
        super().sub_tomo_scan(subtomo_number, start_angle)
        # self.rotate_slowly(0)

    def rotate_slowly(self, angle, step_size=20):
        current_angle = dev.lsamrot.read(cached=True)["value"]
        steps = int(np.ceil(np.abs(current_angle - angle) / step_size)) + 1
        for target_angle in np.linspace(current_angle, angle, steps, endpoint=True):
            umv(dev.lsamrot, target_angle)
            scans.lamni_move_to_scan_center(
                self.align.tomo_fovx_offset, self.align.tomo_fovy_offset, target_angle
            )

    def _at_each_angle(self, angle: float) -> None:
        if "lamni_at_each_angle" in builtins.__dict__:
            lamni_at_each_angle(self, angle)
            return

        self.tomo_scan_projection(angle)
        self.tomo_reconstruct()

        # # cm()
        # # umv(dev.ppth,15.1762) #11.567 keV
        # for ii in range(2):
        #     self.tomo_scan_projection(angle)
        #     self.tomo_reconstruct()
        # # cp()
        # # umv(dev.ppth,15.1827) #11.567 keV
        # for ii in range(2):
        #     self.tomo_scan_projection(angle)
        #     self.tomo_reconstruct()


class DataDrivenLamNI(LamNI):
    def __init__(self, client):
        super().__init__(client)
        self.tomo_data = {}

    def tomo_scan(
        self,
        subtomo_start=1,
        start_index=None,
        fname="~/Data10/data_driven_config/datadriven_params.h5",
    ):
        """start a tomo scan"""
        bec = builtins.__dict__.get("bec")
        scans = builtins.__dict__.get("scans")

        fname = os.path.expanduser(fname)

        if not os.path.exists(fname):
            raise FileNotFoundError(f"Could not find datadriven params file in {fname}.")
        content = f"Loading tomo parameters from {fname}."
        logger.warning(content)
        tags = ["Data_driven_file", "BEC"]
        msg = bec.logbook.LogbookMessage()
        msg.add_text(content).add_tag(tags)
        self.client.logbook.send_logbook_message(msg)
        self._update_tomo_data_from_file(fname)

        self._current_special_angles = self.special_angles.copy()

        if subtomo_start == 1 and start_index is None:
            # pylint: disable=undefined-variable
            self.tomo_id = self.add_sample_database(
                self.sample_name,
                str(datetime.date.today()),
                bec.active_account.decode(),
                bec.queue.next_scan_number,
                "lamni",
                "test additional info",
                "BEC",
            )
            self.write_pdf_report()
        with scans.dataset_id_on_hold:
            self.sub_tomo_data_driven(start_index)

    def sub_tomo_scan(self):
        raise NotImplementedError(
            "Cannot run sub_tomo_scan with data-driven LamNI. Please use lamni.tomo_scan(subtomo_start=<START_NUM>) instead."
        )

    def _at_each_angle(
        self,
        angle=None,
        stepsize=None,
        loptz_pos=None,
        manual_shift_x=0,
        manual_shift_y=0,
    ):
        # Do something...
        # self.tomo_parameters
        self.manual_shift_x = manual_shift_x
        self.manual_shift_y = manual_shift_y
        self.tomo_shellstep = stepsize  # in microns
        if loptz_pos is not None:
            dev.rtx.controller.feedback_disable()
            umv(dev.loptz, loptz_pos)
        super()._at_each_angle(angle=angle)

    def sub_tomo_data_driven(self, start_index=None):
        # for theta, stepsize, sample_to_focus, probe_diameter, subtomo_id in zip(*self.tomo_data.values()):

        for scan_index, scan_data in enumerate(zip(*self.tomo_data.values())):
            if start_index and scan_index < start_index:
                continue
            (
                angle,
                stepsize,
                loptz_pos,
                propagation_distance,
                manual_shift_x,
                manual_shift_y,
                subtomo_number,
            ) = scan_data
            bec.metadata.update(
                {key: float(val) for key, val in zip(self.tomo_data.keys(), scan_data)}
            )
            successful = False
            error_caught = False
            if 0 <= angle < 360.05:
                print(f"Starting LamNI scan for angle {angle}")
                while not successful:
                    self._start_beam_check()
                    if not self.special_angles:
                        self._current_special_angles = []
                    if self._current_special_angles:
                        next_special_angle = self._current_special_angles[0]
                        if np.isclose(angle, next_special_angle, atol=0.5):
                            self._current_special_angles.pop(0)
                            num_repeats = self.special_angle_repeats
                    else:
                        num_repeats = 1
                    try:
                        start_scan_number = bec.queue.next_scan_number
                        for i in range(num_repeats):
                            self._at_each_angle(
                                float(angle),
                                stepsize=float(stepsize),
                                loptz_pos=float(loptz_pos),
                                manual_shift_x=float(manual_shift_x),
                                manual_shift_y=float(manual_shift_y),
                            )
                        error_caught = False
                    except AlarmBase as exc:
                        if exc.alarm_type == "TimeoutError":
                            bec.queue.request_queue_reset()
                            time.sleep(2)
                            error_caught = True
                        else:
                            raise exc

                    if self._was_beam_okay() and not error_caught:
                        successful = True
                    else:
                        self._wait_for_beamline_checks()
                end_scan_number = bec.queue.next_scan_number
                for scan_nr in range(start_scan_number, end_scan_number):
                    self._write_tomo_scan_number(scan_nr, angle, subtomo_number)

    def _update_tomo_data_from_file(self, fname: str) -> None:
        with h5py.File(fname, "r") as file:
            self.tomo_data["theta"] = np.array([*file["theta"]]).flatten()
            self.tomo_data["stepsize"] = np.array([*file["stepsize"]]).flatten()
            self.tomo_data["loptz"] = np.array([*file["loptz"]]).flatten()
            self.tomo_data["propagation_distance"] = np.array(
                [*file["relative_propagation_distance"]]
            ).flatten()
            self.tomo_data["manual_shift_x"] = np.array([*file["manual_shift_x"]]).flatten()
            self.tomo_data["manual_shift_y"] = np.array([*file["manual_shift_y"]]).flatten()
            self.tomo_data["subtomo_id"] = np.array([*file["subtomo_id"]]).flatten()

        shapes = []
        for data in self.tomo_data.values():
            shapes.append(data.shape)
        if len(set(shapes)) > 1:
            raise ValueError(f"Tomo data file has entries of inconsistent lengths: {shapes}.")
