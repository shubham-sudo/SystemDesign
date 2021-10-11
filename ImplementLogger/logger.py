import heapq
from datetime import datetime
from typing import MutableMapping, MutableSequence, Tuple, AnyStr

from ilogger import ILogger


class Logger(ILogger):
    def __init__(self):
        self.heap: MutableSequence[Tuple[datetime, AnyStr]] = list()
        self.lookup: MutableMapping[AnyStr, datetime] = dict()

    def start(self, process_id: str, start_time: datetime):

        if not isinstance(start_time, datetime):
            raise ValueError("`start_time` should be of type datetime")

        heapq.heappush(self.heap, (start_time, process_id))

    def end(self, process_id: str, end_time: datetime):

        if not isinstance(end_time, datetime):
            raise ValueError("`end_time` should be of type datetime.")

        self.lookup[process_id] = end_time

    def poll(self):

        while self.heap and self.heap[0][1] in self.lookup:
            process = heapq.heappop(self.heap)
            print(f"{process[1]} started at {process[0]} ended at {self.lookup[process[1]]}")
            del self.lookup[process[1]]
