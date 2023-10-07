from __future__ import print_function

import threading
import time

import IPython
from bec_lib.alarm_handler import AlarmBase
from bec_lib.client import BECClient
from bec_lib.core import ServiceConfig, bec_logger
from bec_lib.core.connector import ConnectorBase
from IPython.terminal.prompts import Prompts, Token

from .beamline_mixin import BeamlineMixin
from .bec_magics import BECMagics
from .callbacks.ipython_live_updates import IPythonLiveUpdates
from .signals import ScanInterruption, SigintHandler

logger = bec_logger.logger


class BECIPythonClient(BECClient):
    def __init__(self, forced=False) -> None:
        pass

    def __repr__(self) -> str:
        return "BECClient\n\nTo get a list of available commands, type `bec.show_all_commands()`"

    def initialize(
        self,
        config: ServiceConfig = None,
        connector_cls: ConnectorBase = None,
        wait_for_server=True,
    ):
        """initialize the BEC client"""
        super().initialize(config, connector_cls, wait_for_server=wait_for_server)
        # pylint: disable=attribute-defined-outside-init
        self._sighandler = SigintHandler(self)
        self._beamline_mixin = BeamlineMixin()
        self._ip = None
        self._exit_event = threading.Event()
        self._exit_handler_thread = None
        self._hli_funcs = {}
        self.live_updates = IPythonLiveUpdates(self)

    def start(self):
        """start the client"""
        super().start()
        self._start_exit_handler()
        self._configure_ipython()

    def bl_show_all(self):
        self._beamline_mixin.bl_show_all()

    def _set_ipython_prompt_scan_number(self, scan_number: int):
        if self._ip:
            self._ip.prompts.scan_number = scan_number + 1

    def _configure_ipython(self):
        self._ip = IPython.get_ipython()
        if self._ip is None:
            return

        self._ip.prompts = BECClientPrompt(ip=self._ip, client=self, username="demo")
        self._load_magics()
        self._ip.events.register("post_run_cell", log_console)
        self._ip.set_custom_exc((Exception,), _ip_exception_handler)  # register your handler

    def _set_error(self):
        if self._ip is not None:
            self._ip.prompts.status = 0

    def _set_busy(self):
        if self._ip is not None:
            self._ip.prompts.status = 1

    def _set_idle(self):
        if self._ip is not None:
            self._ip.prompts.status = 2

    def _start_exit_handler(self):
        self._exit_handler_thread = threading.Thread(target=self._exit_thread)
        self._exit_handler_thread.daemon = True
        self._exit_handler_thread.start()

    def _shutdown_exit_handler(self):
        self._exit_event.set()
        if self._exit_handler_thread:
            self._exit_handler_thread.join()

    def _load_magics(self):
        magics = BECMagics(self._ip, self)
        self._ip.register_magics(magics)

    def shutdown(self):
        """shutdown the client and all its components"""
        super().shutdown()
        self._shutdown_exit_handler()
        print("done")

    def _exit_thread(self):
        main_thread = threading.main_thread()
        while main_thread.is_alive() and not self._exit_event.is_set():
            time.sleep(0.1)
        if not self._exit_event.is_set():
            self.shutdown()


def _ip_exception_handler(self, etype, evalue, tb, tb_offset=None):
    if issubclass(etype, (AlarmBase, ScanInterruption)):
        print(f"\x1b[31m BEC alarm:\x1b[0m: {evalue}")
        return
    self.showtraceback((etype, evalue, tb), tb_offset=None)  # standard IPython's printout


class BECClientPrompt(Prompts):
    def __init__(self, ip, username, client, status=0):
        self._username = username
        self.client = client
        self.status = status
        super().__init__(ip)

    def in_prompt_tokens(self, cli=None):
        if self.status == 0:
            status_led = Token.OutPromptNum
        elif self.status == 1:
            status_led = Token.PromptNum
        else:
            status_led = Token.Prompt
        return [
            (status_led, "\u2022"),
            (Token.Prompt, " " + self.username),
            (Token.Prompt, " ["),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, "/"),
            (Token.PromptNum, str(self.client.queue.next_scan_number)),
            (Token.Prompt, "] "),
            (Token.Prompt, "❯❯ "),
        ]

    @property
    def username(self):
        """current username"""
        return self._username

    @username.setter
    def username(self, value):
        self._username = value


def log_console(execution_info):
    """log the console input"""
    logger.info(f"[CONSOLE LOG] | {execution_info.info.raw_cell}")
