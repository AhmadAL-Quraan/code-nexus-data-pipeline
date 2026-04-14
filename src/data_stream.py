from abc import ABC, abstractmethod
from typing import Any

# Allowed standard library imports: abc, collections, typing


class DataProcessor(ABC):
    queue: list
    counter: int

    def __init__(self) -> None:
        self.queue = list()
        self.counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            if self.queue:
                return self.queue.pop(0)
            else:
                raise IndexError("Data stream is empty.")
        except IndexError as e:
            print(f"Got exception: {e}")

        return -1, ""


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        true: bool = (
            True if all(isinstance(i, (int, float)) for i in data) else False
        )
        if isinstance(data, list) and true:
            return True
        return False

    def ingest(self, data: int | float | list[int] | list[float]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, (int, float)):
                    self.queue.append((self.counter, str(data)))
                    self.counter += 1
                if isinstance(data, list):
                    for item in data:
                        self.queue.append((self.counter, str(item)))
                        self.counter += 1
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
                    self.queue.append((self.counter, str(data)))
                    self.counter += 1
                if isinstance(data, list):
                    for item in data:
                        self.queue.append((self.counter, str(item)))
                        self.counter += 1
            else:
                raise ValueError("Improper numeric data")
        except ValueError as e:
            print(f"Got exception: {e}")


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            if all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            ):
                return True
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    if all(
                        isinstance(key, str) and isinstance(value, str)
                        for key, value in item.items()
                    ):
                        return True

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        try:
            if self.validate(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        self.queue.append(
                            (
                                self.counter,
                                f"\
{str(key)}: {str(value)}",
                            )
                        )
                        self.counter += 1
                if isinstance(data, list):
                    for i in data:
                        log_level = i.get("log_level")
                        log_message = i.get("log_message")

                        self.queue.append(
                            (
                                self.counter,
                                f"\
{log_level}: {log_message}",
                            )
                        )

                        self.counter += 1

            else:
                raise ValueError(f"Invalid data: {data}. \
The key, value in dict must be string.")
        except ValueError as e:
            print(f"Got exception: {e}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    numeric_processor = NumericProcessor()
    print("Trying to validate data '42':", end=" ")
    print(numeric_processor.validate(42))
    print("Trying to validate data 'Hello':", end=" ")
    print(numeric_processor.validate("Hello"))
    print("Test invalid ingestion of string 'foo' without prior validation:")
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
    print(f"Processing data: {list2}")
    print("Extracting 1 value...")
    text_processor.ingest(list2)
    value2 = text_processor.output()

    print(f"Text value {value2[0]}: {value2[1]}")
    print()
    print("Testing Log Processor...")
    log_processor = LogProcessor()

    print(f"Trying \
to validate input 'Hello': {log_processor.validate('Hello')}")
    list3 = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {list3}")
    log_processor.ingest(list3)
    print("Extracting 2 values...")
    value3 = log_processor.output()
    print(f"Log entry {value3[0]}: {value3[1]}")
    value3 = log_processor.output()
    print(f"Log entry {value3[0]}: {value3[1]}")
