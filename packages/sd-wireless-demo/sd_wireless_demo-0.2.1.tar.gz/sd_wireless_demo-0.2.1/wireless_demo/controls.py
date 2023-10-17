
from __future__ import annotations

from textual.widget import Widget
from textual.widgets import Static, Label, LoadingIndicator, ProgressBar
from textual.reactive import reactive
from textual import events, on
from textual.message import Message
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container

from rich.pretty import Pretty

from textual import work
from textual.worker import get_current_worker


from wireless_demo.demo_sd_sdk import sd


class LoadingWidget(Widget):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def compose(self) -> ComposeResult:
        yield Label(self.label)
        yield LoadingIndicator()


class Notification(Static):
    def on_mount(self) -> None:
        self.set_timer(3, self.remove)

    async def on_click(self) -> None:
        await self.remove()


class HasDevice(Static):
    def __init__(self, connected_device, content="", **kwargs):
        super().__init__(content, **kwargs)
        self.device = connected_device


class Toggle(Static):
    collapsed = reactive(False)

    def render(self) -> str:
        return (":arrow_forward:" if self.collapsed else ":arrow_down_small:") + " Device Information"


class DeviceInformation(HasDevice):
    collapsed = reactive(False)

    def compose(self,) -> ComposeResult:
        yield Toggle()
        yield Static(Pretty(self.device.device_info.to_dict()))
        yield Static("[bold underline]Device Information Service (DIS)[/]")
        dis = {
            "Manufacturer Name" : self.device.wireless_control.ManufacturerName,
            "Model Number" : self.device.wireless_control.ModelNumber,
            "Serial Number" : self.device.wireless_control.SerialNumber,
            "Hardware Revision" : self.device.wireless_control.HardwareRevision,
        }
        yield Static(Pretty(dis))

    def on_mount(self,) -> None:
        self.query_one(Toggle).collapsed = True
        self.add_class("collapsed")

    def on_click(self,) -> None:
        collapsed = self.query_one(Toggle).collapsed
        if collapsed:
            self.remove_class("collapsed")
            self.query_one(Toggle).collapsed = False
        else:
            self.add_class("collapsed")
            self.query_one(Toggle).collapsed = True

class BatteryIndicator(HasDevice):
    level = reactive(0)

    def compose(self) -> ComposeResult:
        with Horizontal(classes="level-indicator"):
            yield Label("       :battery:")
            yield ProgressBar(total=100, show_eta=False)

    def on_mount(self) -> None:
        self.level = self.device.wireless_control.BatteryLevel

    def watch_level(self, new_level: int):
        self.query_one(ProgressBar).progress = new_level

class VolumeControl(HasDevice):
    volume = reactive(0)

    def compose(self) -> ComposeResult:
        with Horizontal(classes="level-indicator"):
            yield Label("Volume   ")
            yield ProgressBar(total=100, show_eta=False)

    def on_mount(self) -> None:
        self.volume = self.device.wireless_control.Volume
        # Workaround for bug in Tooltips on compound widgets
        for part in self.query_one(ProgressBar).query("*"):
            part.tooltip = "Left-click: Volume Down\nMiddle-click: Volume 50%\nRight-click: Volume Up"
        # self.query_one(ProgressBar).tooltip = "Left-click: Volume Down\nMiddle-click: Volume 50%\nRight-click: Volume Up"

    def watch_volume(self, new_volume: int):
        self.query_one(ProgressBar).progress = new_volume

    def on_click(self,  event: events.Click) -> None:
        if event.button == 1:
            self.device.wireless_control.ChangeVolume(False)
        elif event.button == 2:
            self.device.wireless_control.Volume = 50
        elif event.button == 3:
            self.device.wireless_control.ChangeVolume(True)


class MicAttenuation(HasDevice):
    atten = reactive(0)

    def compose(self) -> ComposeResult:
        with Horizontal(classes="level-indicator"):
            yield Label("Mic Level")
            yield ProgressBar(total=100, show_eta=False)

    def on_mount(self) -> None:
        self.atten = self.device.wireless_control.MicAttenuation
        # Workaround for bug in Tooltips on compound widgets
        for part in self.query_one(ProgressBar).query("*"):
            part.tooltip = "Left-click: -5%\nMiddle-click: 50%\nRight-click: +5%"
        # self.query_one(ProgressBar).tooltip = "Left-click: -5%\nMiddle-click: 50%\nRight-click: +5%"

    def watch_atten(self, new_atten: int):
        self.query_one(ProgressBar).progress = new_atten

    def on_click(self,  event: events.Click) -> None:
        if event.button == 1:
            self.device.wireless_control.MicAttenuation = max(0, self.atten - 5)
        elif event.button == 2:
            self.device.wireless_control.MicAttenuation = 50
        elif event.button == 3:
            self.device.wireless_control.MicAttenuation = min(100, self.atten + 5)


class AuxAttenuation(HasDevice):
    atten = reactive(0)

    def compose(self) -> ComposeResult:
        with Horizontal(classes="level-indicator"):
            yield Label("Aux Level")
            yield ProgressBar(total=100, show_eta=False)

    def on_mount(self) -> None:
        self.atten = self.device.wireless_control.AuxAttenuation
        # Workaround for bug in Tooltips on compound widgets
        for part in self.query_one(ProgressBar).query("*"):
            part.tooltip = "Left-click: -5%\nMiddle-click: 50%\nRight-click: +5%"
        # self.query_one(ProgressBar).tooltip = "Left-click: -5%\nMiddle-click: 50%\nRight-click: +5%"

    def watch_atten(self, new_atten: int):
        self.query_one(ProgressBar).progress = new_atten

    def on_click(self,  event: events.Click) -> None:
        if event.button == 1:
            self.device.wireless_control.AuxAttenuation = max(0, self.atten - 5)
        elif event.button == 2:
            self.device.wireless_control.AuxAttenuation = 50
        elif event.button == 3:
            self.device.wireless_control.AuxAttenuation = min(100, self.atten + 5)


class MemoryPanel(HasDevice):
    class MemorySetEvent(Message):
        def __init__(self, memory: int) -> None:
            self.memory = memory
            super().__init__()

    def on_click(self, event: events.Click) -> None:
        if event.button == 1:
            self.device.wireless_control.ChangeMemory(False)
        elif event.button == 2:
            memory = int(self.id.split("memoryindicator")[1])
            self.device.wireless_control.CurrentMemory = memory
        elif event.button == 3:
            self.device.wireless_control.ChangeMemory(True)


class MemoryControl(HasDevice):
    memory = reactive(0)
    num_memories = 0

    def compose(self,) -> ComposeResult:
        memories = []
        self.num_memories = self.device.wireless_control.NumberOfMemories
        for mem in range(self.num_memories):
            s = MemoryPanel(self.device, content=f"{mem}", id=f"memoryindicator{mem}", classes="memoryindicator")
            if not self.device.wireless_control.MemoryEnabled(mem):
                s.add_class("disabled")
            memories.append(s)
            s.tooltip = "Left-click: Memory Down\nMiddle-click: Memory Set\nRight-click:Memory Up"

        yield Static("Memory", classes="currentmemory")
        yield Horizontal(*memories)

    def on_mount(self) -> None:
        self.memory = self.device.wireless_control.CurrentMemory

    def watch_memory(self, new_memory: int):
        for mem in range(self.num_memories):
            if mem == new_memory:
                self.query_one(f"#memoryindicator{mem}").add_class("current")
            else:
                self.query_one(f"#memoryindicator{mem}").remove_class("current")

    def on_memory_panel_memory_set_event(self, event: MemoryPanel.MemorySetEvent) -> None:
        self.memory = self.device.wireless_control.CurrentMemory
        if self.memory != event.memory:
            self.app.logger.info(f"ERROR: Current memory {self.memory} did not match expected {event.memory}!")


class ECMemory(Widget):
    memory = reactive("-1", layout=True)  

    def render(self) -> str:
        return f"{self.memory}"


class ECMemoryControl(HasDevice):
    ec_memory = reactive(0)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("EC Memory:")
            yield ECMemory()

    def on_mount(self) -> None:
        self.ec_memory = self.device.wireless_control.ECMemory

    def watch_ec_memory(self, new_ec_memory: int):
        self.query_one(ECMemory).memory = new_ec_memory


class ProductPanel(HasDevice):

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Product library loaded.\nTODO: Something useful")


class SDKControlPanel(Widget):
    ezairo: reactive[object | None] = reactive(None)

    def __init__(self, connected_device) -> None:
        super().__init__()
        self.device = connected_device

    def compose(self) -> ComposeResult:
        if self.app.product_library is not None:
            yield LoadingWidget(f"Reading device parameters...")
        else:
            yield Label("")

    def on_mount(self) -> None:
        if self.app.product_library is not None:
            self.sync_with_device()
        else:
            self.display = False

    def watch_ezairo(self, _old: object, _new: object) -> None:
        if _new is not None:
            self.call_after_refresh(self.show_product_panel)

    async def show_product_panel(self,) -> None:
        await self.query_one(LoadingWidget).remove()
        # Change UI to show SDK UI
        self.call_after_refresh(self.mount, ProductPanel(self.ezairo))

    @work(exclusive=True)
    def sync_with_device(self,) -> None:
        worker = get_current_worker()
        _res = self.app.sdk.create_product(self.device.com_adaptor,
                                           self.app.product_library)
        if not worker.is_cancelled:
            def _update_reactive(new_value):
                self.ezairo = new_value
            self.app.call_from_thread(_update_reactive, _res)


class HearingAidWirelessControl(Widget):
    def __init__(self, connected_device) -> None:
        super().__init__()
        self.device = connected_device

    def compose(self) -> ComposeResult:
        yield Container(
            BatteryIndicator(self.device),
            VolumeControl(self.device),
            MicAttenuation(self.device),
            AuxAttenuation(self.device),
            MemoryControl(self.device),
            ECMemoryControl(self.device),
            SDKControlPanel(self.device),
            DeviceInformation(self.device),
        )

    def on_hearing_aid_control_panel_sdk_event(self, sdk_event: HearingAidControlPanel.SdkEvent) -> None:
        # Based on the event we got, update the child controls
        # self.app.logger.info(f"Got event type {sdk_event.event_type} with data {sdk_event.event_data}")
        if sdk_event.event_type == sd.kBatteryEvent:
            self.query_one(BatteryIndicator).level = int(sdk_event.event_data["BatteryLevel"])
        elif sdk_event.event_type == sd.kVolumeEvent:
            self.query_one(VolumeControl).volume = int(sdk_event.event_data["VolumeLevel"])
        elif sdk_event.event_type == sd.kMicAttenuationEvent:
            self.query_one(MicAttenuation).atten = int(sdk_event.event_data["MicLevel"])
        elif sdk_event.event_type == sd.kAuxAttenuationEvent:
            self.query_one(AuxAttenuation).atten = int(sdk_event.event_data["AuxLevel"])
        elif sdk_event.event_type == sd.kMemoryEvent:
            self.query_one(MemoryControl).memory = int(sdk_event.event_data["CurrentMemory"])
        elif sdk_event.event_type == sd.kECMemoryEvent:
            self.query_one(ECMemoryControl).ec_memory = int(sdk_event.event_data["ECMemory"])
        else:
            self.app.logger.info(f"Got event type {sdk_event.event_type} with data {sdk_event.event_data}")
        # Avoid event bubbling back up to parent widget
        sdk_event.stop(True)


class HearingAidControlPanel(Widget):
    device_info: reactive[dict | None] = reactive(None)
    connected_device: reactive[object | None] = reactive(None)

    class SdkEvent(Message):
        def __init__(self, event_type: int, event_data: dict) -> None:
            self.event_type = event_type
            self.event_data = event_data
            super().__init__()

    class DeviceDisconnectedEvent(Message):
        pass

    def on_mount(self) -> None:
        self.display = False

    def watch_device_info(self, _old: dict, _new: dict) -> None:
        if _old is None and _new is not None:
            self.display = True
            self.mount(LoadingWidget(f"Connecting to '{self.device_info['DeviceName']}' ({self.device_info['DeviceID']})..."))
            self.connect_device()

        elif _new is None:
            if self.connected_device:
                self.connected_device.close()
                self.connected_device = None
            self.display = False

    @work(exclusive=True)
    def connect_device(self,) -> None:
        worker = get_current_worker()
        _res = self.app.sdk.connect_device(self.device_info)
        if not worker.is_cancelled:
            def _update_reactive(new_value):
                self.connected_device = new_value
            self.app.call_from_thread(_update_reactive, _res)

    def watch_connected_device(self, _old: object, _new: object) -> None:
        if _new is not None:
            self.app.logger.info(f"Connected: ({self.device_info})")
            self.call_later(self.show_control_panel)
        else:
            try:
                self.query_one(HearingAidWirelessControl).remove()
            except:
                pass
            self.app.logger.debug("Device disconnected")

    async def show_control_panel(self,) -> None:
        await self.query_one(LoadingWidget).remove()
        self.connected_device.on_event = self.on_sdk_event
        # Change UI to show wireless control panel
        self.call_after_refresh(self.mount, HearingAidWirelessControl(self.connected_device))

    def on_sdk_event(self, event_type, event_data):
        if event_type == sd.kConnectionEvent and int(event_data["ConnectionState"]) in [sd.kDisconnected, sd.kDisconnecting]:
            self.post_message(self.DeviceDisconnectedEvent())
        else:
            try:
                widget = self.query_one(HearingAidWirelessControl)
                widget.post_message(self.SdkEvent(event_type, event_data))
            except:
                pass

    @on(DeviceDisconnectedEvent)
    def device_disconnected(self):
        if self.device_info is not None:
            self.app.logger.info(f"Device disconnected: ({self.device_info})")
            self.app.mount(Notification(f"{self.device_info['DeviceID']} disconnected"))
            self.disconnect_device()

    def disconnect_device(self,):
        self.device_info = None


class HearingAidControlPanels(Widget):
    def compose(self) -> ComposeResult:
        with Container():
            with Horizontal ():
                yield HearingAidControlPanel(id="deviceleft")
                yield HearingAidControlPanel(id="deviceright")
