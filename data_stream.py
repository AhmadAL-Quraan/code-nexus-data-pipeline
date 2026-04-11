from abc import ABC, abstractmethod
from typing import Any
from collections import deque


class DataProcessor(ABC):
    _queue: deque = deque()
    _counter: int = 0

    def __init__(self) -> None:
        self._queue = deque()
        self._counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            if self._queue:
                return self._queue.popleft()
            else:
                raise IndexError("Data stream is empty.")
        except IndexError as e:
            print(f"Got exception: {e}")

        return -1, ""


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        # all --> return True if all elements of the iterable are true (or if the iterable is empty).
        if isinstance(data, list) and all(isinstance(i, (int, float)) for i in data):
            return True
        return False

    def ingest(self, data: int | float | list[int] | list[float]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, (int, float)):
                    self._queue.append((self._counter, str(data)))
                    self._counter += 1
                if isinstance(data, list):
                    for item in data:
                        self._queue.append((self._counter, str(item)))
                        self._counter += 1
            else:
                raise ValueError("Improper numeric data")
        except ValueError as e:
            print(f"Got exception: {e}")


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and all(isinstance(i, str) for i in data):
            return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, str):
                    self._queue.append((self._counter, str(data)))
                    self._counter += 1
                if isinstance(data, list):
                    for item in data:
                        self._queue.append((self._counter, str(item)))
                        self._counter += 1
            else:
                raise ValueError("Improper numeric data")
        except ValueError as e:
            print(f"Got exception: {e}")


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    return False
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False
                for key, value in item.items():
                    if not isinstance(key, str) or not isinstance(value, str):
                        return False

        return True

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if self.validate(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    self._queue.append((self._counter, f"{key}: {value}"))
                    self._counter += 1
            if isinstance(data, list):
                for i in data:
                    for key, value in i.items():
                        self._queue.append((self._counter, f"{key}: {value}"))
                        self._counter += 1

        else:
            raise ValueError(
                f"Invalid data: {data}. The key, value in dict must be string."
            )


if __name__ == "__main__":
    print("Testing Numeric Processor...")
    numeric_processor = NumericProcessor()
    print(f"Trying to validate data '42':", end=" ")
    print(numeric_processor.validate(42))
    print(f"Trying to validate data 'Hello':", end=" ")
    print(numeric_processor.validate("Hello"))
    print("Test invalid ingestion of string ’foo’ without prior validation:")
    numeric_processor.ingest("foo")
    list1 = [1, 2, 3, 4, 5]
    print(f"Processing data: {list1}")
    numeric_processor.ingest(list1)
    value1 = numeric_processor.output()
    print(f"Numeric value {value1[0]}: {value1[1]}")
    value1 = numeric_processor.output()
    print(f"Numeric value {value1[0]}: {value1[1]}")
    value1 = numeric_processor.output()
    print(f"Numeric value {value1[0]}: {value1[1]}")

    print()
    print("Testing Text Processor...")
    text_processor = TextProcessor()
    print(f"Trying to validate input '42': {text_processor.validate(42)}")
    list2 = ["Hello", "Nexus", "World"]
    print("Extracting 1 value...")
    text_processor.ingest(list2)
    value2 = text_processor.output()

    print(f"Text value {value2[0]}: {value2[1]}")
    print()
    print("Testing Log Processor...")
    log_processor = LogProcessor()

    print(f"Trying to validate input 'Hello': {log_processor.validate("Hello")}")
    print(
        "Processing data: [{’log_level’: ’NOTICE’, ’log_message’:’Connection to server’}, {’log_level’: ’ERROR’, ’log_message’:’Unauthorized access!!’}]"
    )
    print("Extracting 2 values...")
    value3 = log_processor.output()
    print(f"Log entry {value3[0]}: {value3[1]}")
    value3 = log_processor.output()
    print(f"Log entry {value3[0]}: {value3[1]}")
