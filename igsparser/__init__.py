
from .message_parser import MessageParser
from .msd import Msd
from .advertisement import Advertisement

class MsdParser:
    @staticmethod
    def parse(content):
        if (type(content) is str):
            return Msd(bytearray.fromhex(content))
        elif (type(content) is bytearray):
            return Msd(content)
        elif (type(content) is bytes):
            return Msd(bytearray(content))
        else:
            raise ValueError('unsupport content type')

class PayloadParser:
    @staticmethod
    def parse(payload):
        return Advertisement(bytes(payload))

__all__ = [ 'MessageParser', 'PayloadParser', 'MsdParser' ]
