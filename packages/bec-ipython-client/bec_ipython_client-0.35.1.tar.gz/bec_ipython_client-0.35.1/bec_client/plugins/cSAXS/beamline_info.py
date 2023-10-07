import builtins

from rich import box
from rich.table import Table

from bec_client.beamline_mixin import BeamlineShowInfo


class BeamlineInfo(BeamlineShowInfo):
    def show(self):
        """Display information about the current beamline status"""
        console = self._get_console()

        table = Table(title="X12SA Info", box=box.SQUARE)
        table.add_column("Key", justify="left")
        table.add_column("Value", justify="left")

        info = self._get_beamline_info_messages()
        self._add_op_status(table, info)
        self._add_id_gap(table, info)
        self._add_storage_ring_vac(table, info)
        self._add_shutter_status(table, info)
        self._add_mokev(table, info)
        self._add_fe_status(table, info)
        self._add_es1_valve(table, info)
        self._add_xbox1_pressure(table, info)
        self._add_xbox2_pressure(table, info)

        console.print(table)

    def _add_op_status(self, table, info):
        val = self._get_info_val(info, "x12sa_op_status")
        if val not in ["attended"]:
            return table.add_row("Beamline operation", val, style=self.ALARM_STYLE)
        return table.add_row("Beamline operation", val, style=self.DEFAULT_STYLE)

    def _add_shutter_status(self, table, info):
        val = self._get_info_val(info, "x12sa_es1_shutter_status")
        if val.lower() not in ["open"]:
            return table.add_row("Shutter", val, style=self.ALARM_STYLE)
        return table.add_row("Shutter", val, style=self.DEFAULT_STYLE)

    def _add_storage_ring_vac(self, table, info):
        val = self._get_info_val(info, "x12sa_storage_ring_vac")
        if val.lower() not in ["ok"]:
            return table.add_row("Storage ring vacuum", val, style=self.ALARM_STYLE)
        return table.add_row("Storage ring vacuum", val, style=self.DEFAULT_STYLE)

    def _add_es1_valve(self, table, info):
        val = self._get_info_val(info, "x12sa_es1_valve")
        if val.lower() not in ["open"]:
            return table.add_row("ES1 valve", val, style=self.ALARM_STYLE)
        return table.add_row("ES1 valve", val, style=self.DEFAULT_STYLE)

    def _add_xbox1_pressure(self, table, info):
        MAX_PRESSURE = 2e-6
        val = info["x12sa_exposure_box1_pressure"]["value"]
        if val > MAX_PRESSURE:
            return table.add_row(
                f"Exposure box 1 pressure (limit for opening the valve: {MAX_PRESSURE:.1e} mbar)",
                f"{val:.1e} mbar",
                style=self.ALARM_STYLE,
            )
        return table.add_row("Exposure box 1 pressure", f"{val:.1e} mbar", style=self.DEFAULT_STYLE)

    def _add_xbox2_pressure(self, table, info):
        MAX_PRESSURE = 2e-6
        val = info["x12sa_exposure_box2_pressure"]["value"]
        if val > MAX_PRESSURE:
            return table.add_row(
                f"Exposure box 2 pressure (limit for opening the valve: {MAX_PRESSURE:.1e} mbar)",
                f"{val:.1e} mbar",
                style=self.ALARM_STYLE,
            )
        return table.add_row("Exposure box 2 pressure", f"{val:.1e} mbar", style=self.DEFAULT_STYLE)

    def _add_fe_status(self, table, info):
        val = self._get_info_val(info, "x12sa_fe_status")
        return table.add_row("Front end shutter", val, style=self.DEFAULT_STYLE)

    def _add_id_gap(self, table, info):
        val = info["x12sa_id_gap"]["value"]
        if val > 8:
            return table.add_row("ID gap", f"{val:.3f} mm", style=self.ALARM_STYLE)
        return table.add_row("ID gap", f"{val:.3f} mm", style=self.DEFAULT_STYLE)

    def _add_mokev(self, table, info):
        val = info["x12sa_mokev"]["value"]
        return table.add_row("Selected energy (mokev)", f"{val:.3f} keV", style=self.DEFAULT_STYLE)

    def _get_beamline_info_messages(self) -> dict:
        dev = builtins.__dict__.get("dev")

        def _get_bl_msg(info, device_name):
            info[device_name] = dev[device_name].read(cached=True)

        info = {}
        _get_bl_msg(info, "x12sa_op_status")
        _get_bl_msg(info, "x12sa_storage_ring_vac")
        _get_bl_msg(info, "x12sa_es1_shutter_status")
        _get_bl_msg(info, "x12sa_id_gap")
        _get_bl_msg(info, "x12sa_mokev")
        _get_bl_msg(info, "x12sa_fe_status")
        _get_bl_msg(info, "x12sa_es1_valve")
        _get_bl_msg(info, "x12sa_exposure_box1_pressure")
        _get_bl_msg(info, "x12sa_exposure_box2_pressure")

        return info
