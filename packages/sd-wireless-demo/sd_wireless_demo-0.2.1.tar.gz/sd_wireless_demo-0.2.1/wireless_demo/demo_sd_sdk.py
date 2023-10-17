# NOTE: The following imports depend on the SD_SDK_ROOT environment
#       variable being set appropriately. This is done via the command
#       line arguments in main.py. Ensure you always run that script
#       as the entry point to the system.
from sd_sdk_python import sd, get_product_manager
from sd_sdk_python.sd_sdk import Ezairo
from sd_sdk_python.sd_sdk_wireless import ScanResultHandler, connect_to_device


class SDKHelper(object):
    def __init__(self, programmer,
                 com_port=None,
                 clear_bond_table=False,
                 noah_driver_path=None) -> None:
        self.pm = get_product_manager()
        assert programmer.upper() in ['RSL10', 'NOAHLINK']
        self.programmer_type = sd.kRSL10 if programmer == 'RSL10' else sd.kNoahlinkWireless
        self.com_port = com_port
        self.clear_bond_table = clear_bond_table
        if noah_driver_path is not None:
            self.pm.BLEDriverPath = str(noah_driver_path)

        self.scan_handler = None
        self.scan_async = None

    def start_scanning(self, on_scan_event):
        self.scan_handler = ScanResultHandler(on_scan_event, listen=True)
        # We always use the left side to scan for devices
        self.scan_async = self.pm.BeginScanForWirelessDevices(self.programmer_type,
                                                              self.com_port,
                                                              sd.kLeft, "",
                                                              self.clear_bond_table)

    def stop_scanning(self,):
        results = self.pm.EndScanForWirelessDevices(self.scan_async)
        self.scan_handler.listen_for_events(False)
        self.scan_async = None
        self.scan_handler = None

    def connect_device(self, device_info, timeout=30.0, event_cb=None):
        return connect_to_device(device_info['DeviceID'],
                                 self.programmer_type,
                                 timeout=timeout,
                                 event_cb=event_cb)
 
    def create_product(self, com_adaptor, product_library) -> Ezairo:
        library = self.pm.LoadLibraryFromFile(str(product_library))
        product = library.Products[0].CreateProduct()
        device_info = com_adaptor.DetectDevice()
        assert device_info is not None
        assert device_info.IsValid

        if not product.InitializeDevice(com_adaptor):
            raise RuntimeError("Product is not configured with that product library!")
        return Ezairo(sd, com_adaptor, device_info, product)
