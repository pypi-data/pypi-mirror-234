from __future__ import annotations
import logging

from rich.console import RenderableType

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.screen import Screen
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (
    Footer,
    Header,
    Static,
    TextLog,
    ListView,
    ListItem,
    Button,
)
from textual.events import ScreenResume
from textual.message import Message

from wireless_demo.demo_sd_sdk import SDKHelper, sd
from wireless_demo.controls import HearingAidControlPanels, HearingAidControlPanel

__version__ = "0.2.1"

_title = "Pre Suite Wireless Demo"


class Version(Static):

    def render(self) -> RenderableType:
        return f"[b]v{__version__}"


class Body(Container):
    pass


class Title(Static):
    pass

class SelectedScanItems(Static):
    total = reactive(0)

    def render(self,) -> str:
        return f"{self.total} devices selected"

class ScanResultDisplay(ListItem):
    """A widget to display a scan result"""
    name = reactive("")
    device_id = reactive("")
    rssi = reactive(0)

    def __init__(self, scan_data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.scan_data = scan_data
        self.name = scan_data["DeviceName"]
        self.device_id = scan_data["DeviceID"]
        self.rssi = int(scan_data["RSSI"])

    def render(self) -> str:
        return f"{self.name} ({self.device_id})    [{self.rssi} dBm]"

    def get_integer_mac_addresses(self,):
        mac_str = self.device_id.replace(":", "").replace("-", "")
        mac_addr1 = int(mac_str[0:6], 16)
        mac_addr2 = int(mac_str[6:], 16)
        return (mac_addr1, mac_addr2)


class ScanResultsListViews(Widget):
    def compose(self) -> ComposeResult:
        yield Container(
            Horizontal (
                Vertical (
                    Title("Discovered LEFT devices", classes="listtitle"),
                    ListView(id="scanresultsleft"),
                    id="scanpaneleft",
                ),
                Vertical (
                    Title("Discovered RIGHT devices", classes="listtitle"),
                    ListView(id="scanresultsright"),
                    id="scanpaneright",
                )
            ),
            SelectedScanItems(),
        )


class ScanningScreen(Screen):
    TITLE = _title
    BINDINGS = [
        ("ctrl+x", "exit_scan_mode", "Exit Scan Mode"),
        ("ctrl+r", "clear_scan_lists", "Clear And Rescan"),
    ]

    class ScanEvent(Message):
        def __init__(self, scan_data: dict) -> None:
            self.scan_data = scan_data
            super().__init__()

    def compose(self) -> ComposeResult:
        # See https://github.com/Textualize/textual/issues/1307
        yield Container(
            Header(show_clock=True),
            Body(
                ScanResultsListViews(),
                Version(),
            ),
        )
        yield Footer()

    def on_scanning_screen_scan_event(self, message: ScanningScreen.ScanEvent) -> None:
        # print(f"Got scan event with data: {message.scan_data}")
        self.app.logger.debug(f"Got scan event with data: {message.scan_data}")
        try:
            side = message.scan_data.get('ManufacturingData', {}).get('side', None)
            _id = '#scanresultsleft' if side == sd.kLeft else '#scanresultsright'
            new_result = ScanResultDisplay(message.scan_data)
            self.query_one(_id).mount(new_result)
            new_result.scroll_visible()
            part1, part2 = new_result.get_integer_mac_addresses()
            new_result.tooltip = f"MAC Part 1: {part1}\nMAC Part 2: {part2}"
        except AttributeError:
            pass

    @on(ScreenResume)
    def _start_scanning(self,):

        def scan_cb(scan_data):
            self.post_message(self.ScanEvent(scan_data))

        self.app.sdk.start_scanning(scan_cb)
        self.app.logger.debug(f"Device scan started.")
        self.query_one(SelectedScanItems).total = 0
        self.app.left_device = None
        self.app.right_device = None

    def _stop_scanning(self,):
        self.app.sdk.stop_scanning()
        self.app.logger.debug(f"Device scan stopped.")

    async def action_exit_scan_mode(self) -> None:
        self._stop_scanning()
        await self.app.query(ScanResultDisplay).remove()
        self.app.pop_screen()

    async def action_clear_scan_lists(self) -> None:
        await self.app.query(ScanResultDisplay).remove()
        self._stop_scanning()
        self._start_scanning()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # Update the items to use in the app
        if event.list_view is self.query_one('#scanresultsleft'):
            self.app.left_device = event.item.scan_data
        elif event.list_view is self.query_one('#scanresultsright'):
            self.app.right_device = event.item.scan_data
        devices = [w for w in [self.app.left_device, self.app.right_device] if w is not None]
        self.query_one(SelectedScanItems).total = len(devices)


class QuitScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="quitdialog",
        )

    @on(Button.Pressed, "#quit")
    def quit(self):
        self.app.do_exit()

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        self.app.pop_screen()

class ConsoleLogStream:
    def __init__(self, log_cb) -> None:
        self.log = log_cb
        self.name = "Console Log"

    def write(self, s):
        self.log(str(s).rstrip())

class MainScreen(Screen):
    TITLE = _title
    BINDINGS = [
        ("ctrl+s", "enter_scan_mode", "Scan For Devices"),
        ("f1", "app.toggle_class('TextLog', '-hidden')", "Show Log"),
        ("ctrl+q", "request_quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            TextLog(id="consolelog", classes="-hidden", wrap=False, highlight=True, markup=True),
            Body(
                HearingAidControlPanels(),
                Version(),
            ),
        )
        yield Footer()

    def console_log(self, renderable: RenderableType) -> None:
        self.query_one(TextLog).write(renderable)

    def on_mount(self) -> None:
        sh = logging.StreamHandler(stream=ConsoleLogStream(self.console_log))
        sh.setLevel(logging.INFO)
        self.app.logger.addHandler(sh)
        self.app.logger.info("Pre Suite wireless demo application started")

    def action_request_quit(self) -> None:
        self.app.push_screen("quit")

    def action_enter_scan_mode(self) -> None:
        self.disconnect_all_devices()
        self.app.push_screen("scan")

    @on(ScreenResume)
    def update_device_info(self):
        self.app.logger.debug(f"Using the following devices: [{self.app.left_device}, {self.app.right_device}]")
        self.query_one('#deviceleft').device_info = self.app.left_device
        self.query_one('#deviceright').device_info = self.app.right_device

    def disconnect_all_devices(self,):
        for q in self.query(HearingAidControlPanel):
            q.disconnect_device()


from dataclasses import dataclass
import pathlib
@dataclass
class Args:
    """Class emulating command line arguments to allow running via `textual run --dev`"""
    programmer:str
    com_port:str
    delete_bonds:bool
    debug:bool
    noahlink_driver_path:object
    library_path:object

class DemoApp(App[None]):
    CSS_PATH = "demo_ui.css"
    SCREENS = {"main" : MainScreen(), "scan" : ScanningScreen(), "quit" : QuitScreen()}

    def __init__(self, cmdline_args=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cmdline_args = cmdline_args

        # See if we're being run by `textual run --dev`
        if 'devtools' in self.features:
            self.cmdline_args = Args('RSL10', 'COM7', False, True, None, pathlib.Path("C:\\_dev\\PreSuite\\SoundDesignerSDK\\products\\E7160SL.library"))
            # self.cmdline_args = Args('NOAHLink', '', False, True, pathlib.Path("c:\\Users\\ffwxyx\\.sounddesigner\\nlw\\"), pathlib.Path("C:\\_dev\\PreSuite\\SoundDesignerSDK\\products\\E7160SL.library"))

        self.logger = logging.getLogger("DemoApp")
        # Avoid all output being sent to the console as well
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG if self.cmdline_args.debug else logging.INFO)
        if self.cmdline_args.debug:
            fh = logging.FileHandler('app_debug.log', encoding='utf-8', mode='w')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
            self.logger.addHandler(fh)
        # The device ids we are going to interact with
        self.left_device = None
        self.right_device = None

        self.sdk = SDKHelper(self.cmdline_args.programmer,
                             com_port=self.cmdline_args.com_port,
                             clear_bond_table=self.cmdline_args.delete_bonds,
                             noah_driver_path=self.cmdline_args.noahlink_driver_path)

        self.product_library = None
        if self.cmdline_args.library_path is not None and \
                            self.cmdline_args.library_path.exists() and \
                                                self.cmdline_args.library_path.is_file():
            self.product_library = self.cmdline_args.library_path


    def on_mount(self) -> None:
        self.push_screen("main")

    def exit(self, result = None) -> None:
        self.push_screen("quit")

    def do_exit(self, result = None) -> None:
        # Textual now only queries the active screen so this no longer works...
        # self.query_one(MainScreen).disconnect_all_devices()

        # But this does
        self.SCREENS["main"].disconnect_all_devices()
        super().exit(result)
