import attr

from strategy_bridge.bus import DataReader, DataBus, DataWriter
from strategy_bridge.common import config
from strategy_bridge.pb.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket
from strategy_bridge.processors import BaseProcessor
from strategy_bridge.utils.debugger import debugger


@attr.s(auto_attribs=True)
class VisionCombiner(BaseProcessor):

    vision_reader: DataReader = attr.ib(init=False)
    combined_vision_writer: DataWriter = attr.ib(init=False)

    def initialize(self, data_bus: DataBus) -> None:
        super(VisionCombiner, self).initialize(data_bus)

        self.vision_reader = DataReader(self.data_bus, config.VISION_DETECTIONS_TOPIC)
        self.combined_vision_writer = DataWriter(self.data_bus, config.COMBINED_VISION_DETECTIONS_TOPIC, 30)
        self._ssl_converter = SSL_WrapperPacket()

    @debugger
    def process(self):
        for ssl_record in self.vision_reader.read_new():
            ssl_package = ssl_record.content
            ssl_package = self._ssl_converter.FromString(ssl_package)
            print(type(ssl_package))
