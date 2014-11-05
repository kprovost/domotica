from abc import ABCMeta, abstractmethod

class Poller(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def poll(self, s7conn):
        pass
