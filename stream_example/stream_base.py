import threading

from infrastructure.log_wrapper import LogWrapper

class StreamBase(threading.Thread):
    
    def __init__(self,shared_price, price_lock: threading.Lock, price_events, log_name):
        super().__init__()
        self.shared_price = shared_price
        self.price_lock = price_lock
        self.price_events = price_events
        self.log = LogWrapper(log_name)
        
    def log_message(self, msg, error=False):
        if error == True:
            self.log.logger.error(msg)
        else:
            self.log.logger.debug(msg)