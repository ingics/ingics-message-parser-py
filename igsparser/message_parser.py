import re
import sys
import json
from datetime import datetime
from .advertisement import Advertisement

class MessageData:
    def __init__(self, msg):
        match = re.match('^\\$(.+),([0-9a-fA-F]{12}),([0-9a-fA-F]{12}),(-?\\d+),([0-9a-fA-F]*)(,(.+))?', msg)
        if match:
            self.beacon = match.group(2)
            self.gateway = match.group(3)
            self.rssi = int(match.group(4))
            self.fullMessage = msg
            if sys.version_info[0] < 3 or sys.version_info[1] < 4:
                import time
                self.timestamp = time.time()
            else:
                from datetime import datetime
                self.timestamp = datetime.now().timestamp()
            if match.group(6) is not None:
                self.timestamp = float(match.group(7))
            self.advertisement = Advertisement(match.group(5))
        else:
            raise ValueError()

class MessageParser:

    @staticmethod
    def parse(message, callback = None):
        try:
            data = json.loads(message)['data']
        except:
            data = re.split('\\r?\\n', message)
        results = []
        for msg in data:
            log = MessageData(msg)
            if callable(callback):
                callback(log, len(results))
            results.append(log)
        return results if not callable(callback) else None

