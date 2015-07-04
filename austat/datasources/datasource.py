from abc import ABCMeta, abstractmethod
import random

class datasource:

    __metaclass__ = ABCMeta
    stats = []

    def getstats(self):
        return self.stats

    def getrandomstat(self, n):
        return self.getstat(self.stats[random.randint(0, len(self.stats)-1)], n)

    @abstractmethod
    def getstat(self, stat, n):
        pass

