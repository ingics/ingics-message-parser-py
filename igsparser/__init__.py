
from .message_parser import MessageParser
from .advertisement import Advertisement

class PayloadParser:
    @staticmethod
    def parse(payload):
        ad = Advertisement(payload)
        return ad

__all__ = [ 'MessageParser', 'PayloadParser' ]
