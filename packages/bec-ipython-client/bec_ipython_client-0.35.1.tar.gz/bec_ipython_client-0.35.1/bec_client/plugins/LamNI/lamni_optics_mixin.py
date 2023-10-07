import builtins
import time

from rich import box
from rich.console import Console
from rich.table import Table

from bec_client.plugins.cSAXS import epics_get, epics_put, fshclose

# import builtins to avoid linter errors
dev = builtins.__dict__.get("dev")
umv = builtins.__dict__.get("umv")
bec = builtins.__dict__.get("bec")


class LamNIOpticsMixin:
    @staticmethod
    def _get_user_param_safe(device, var):
        param = dev[device].user_parameter
        if not param or param.get(var) is None:
            raise ValueError(f"Device {device} has no user parameter definition for {var}.")
        return param.get(var)

    def leye_out(self):
        self.loptics_in()
        fshclose()
        leyey_out = self._get_user_param_safe("leyey", "out")
        umv(dev.leyey, leyey_out)

        epics_put("XOMNYI-XEYE-ACQ:0", 2)
        # move rotation stage to zero to avoid problems with wires
        umv(dev.lsamrot, 0)
        umv(dev.dttrz, 5854, dev.fttrz, 2395)

    def leye_in(self):
        bec.queue.next_dataset_number += 1
        # move rotation stage to zero to avoid problems with wires
        umv(dev.lsamrot, 0)
        umv(dev.dttrz, 6419.677, dev.fttrz, 2959.979)
        while True:
            moved_out = (input("Did the flight tube move out? (Y/n)") or "y").lower()
            if moved_out == "y":
                break
            if moved_out == "n":
                return
        leyex_in = self._get_user_param_safe("leyex", "in")
        leyey_in = self._get_user_param_safe("leyey", "in")
        umv(dev.leyex, leyex_in, dev.leyey, leyey_in)
        self.align.update_frame()

    def _lfzp_in(self):
        loptx_in = self._get_user_param_safe("loptx", "in")
        lopty_in = self._get_user_param_safe("lopty", "in")
        umv(
            dev.loptx, loptx_in, dev.lopty, lopty_in
        )  # for 7.2567 keV and 150 mu, 60 nm fzp, loptz 83.6000 for propagation 1.4 mm

    def lfzp_in(self):
        """
        move in the lamni zone plate.
        This will disable rt feedback, move the FZP and re-enabled the feedback.
        """
        if "rtx" in dev and dev.rtx.enabled:
            dev.rtx.controller.feedback_disable()

        self._lfzp_in()

        if "rtx" in dev and dev.rtx.enabled:
            dev.rtx.controller.feedback_enable_with_reset()

    def loptics_in(self):
        """
        Move in the lamni optics, including the FZP and the OSA.
        """
        self.lfzp_in()
        self.losa_in()

    def loptics_out(self):
        """Move out the lamni optics"""
        if "rtx" in dev and dev.rtx.enabled:
            dev.rtx.controller.feedback_disable()

        # self.lcs_out()
        self.losa_out()
        loptx_out = self._get_user_param_safe("loptx", "out")
        lopty_out = self._get_user_param_safe("lopty", "out")
        umv(dev.loptx, loptx_out, dev.lopty, lopty_out)

        if "rtx" in dev and dev.rtx.enabled:
            time.sleep(1)
            dev.rtx.controller.feedback_enable_with_reset()

    def lcs_in(self):
        # umv lcsx -1.852 lcsy -0.095
        pass

    def lcs_out(self):
        umv(dev.lcsy, 3)

    def losa_in(self):
        # 6.2 keV, 170 um FZP
        # umv(dev.losax, -1.4450000, dev.losay, -0.1800)
        # umv(dev.losaz, -1)
        # 6.7, 170
        # umv(dev.losax, -1.4850, dev.losay, -0.1930)
        # umv(dev.losaz, 1.0000)
        # 7.2, 150
        losax_in = self._get_user_param_safe("losax", "in")
        losay_in = self._get_user_param_safe("losay", "in")
        losaz_in = self._get_user_param_safe("losaz", "in")
        umv(dev.losax, losax_in, dev.losay, losay_in)
        umv(dev.losaz, losaz_in)
        # 11 kev
        # umv(dev.losax, -1.161000, dev.losay, -0.196)
        # umv(dev.losaz, 1.0000)

    def losa_out(self):
        losay_out = self._get_user_param_safe("losay", "out")
        losaz_out = self._get_user_param_safe("losaz", "out")
        umv(dev.losaz, losaz_out)
        umv(dev.losay, losay_out)

    def lfzp_info(self):
        loptz_val = dev.loptz.read()["loptz"]["value"]
        distance = -loptz_val + 85.6 + 52
        print(f"The sample is in a distance of {distance:.1f} mm from the FZP.")

        diameters = [80e-6, 100e-6, 120e-6, 150e-6, 170e-6, 200e-6, 220e-6, 250e-6]

        mokev_val = dev.mokev.read()["mokev"]["value"]
        console = Console()
        table = Table(
            title=f"At the current energy of {mokev_val:.4f} keV we have following options:",
            box=box.SQUARE,
        )
        table.add_column("Diameter", justify="center")
        table.add_column("Focal distance", justify="center")
        table.add_column("Current beam size", justify="center")

        wavelength = 1.2398e-9 / mokev_val

        for diameter in diameters:
            outermost_zonewidth = 60e-9
            focal_distance = diameter * outermost_zonewidth / wavelength
            beam_size = (
                -diameter / (focal_distance * 1000) * (focal_distance * 1000 - distance) * 1e6
            )
            table.add_row(
                f"{diameter*1e6:.2f} microns",
                f"{focal_distance:.2f} mm",
                f"{beam_size:.2f} microns",
            )

        console.print(table)

        print("OSA Information:")
        # print(f"Current losaz %.1f\n", A[losaz])
        # print("The OSA will collide with the sample plane at %.1f\n\n", 89.3-A[loptz])
        print(
            "The numbers presented here are for a sample in the plane of the lamni sample holder.\n"
        )
