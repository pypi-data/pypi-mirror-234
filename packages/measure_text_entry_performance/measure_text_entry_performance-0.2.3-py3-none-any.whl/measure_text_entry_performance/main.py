import time
from typing import Any


class AddEvent:
    def __init__(
        self,
        timestamp: float,
        added_input: str,
    ) -> None:
        self.event_type = "add_new_input"
        self.timestamp = timestamp
        self.added_input = added_input

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "added_input": self.added_input,
        }


class DeleteEvent:
    def __init__(
        self,
        timestamp: float,
        deleted_length: int,
        deleted_str: str | None,
    ) -> None:
        self.event_type = "delete"
        self.timestamp = timestamp
        self.deleted_length = deleted_length
        self.deleted_str = deleted_str

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "deleted_length": self.deleted_length,
            "deleted_str": self.deleted_str,
        }


class EndPhraseEvent:
    def __init__(
        self,
        timestamp: float,
        entered_phrase: str,
    ) -> None:
        self.event_type = "end_phrase"
        self.timestamp = timestamp
        self.entered_phrase = entered_phrase

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "entered_phrase": self.entered_phrase,
        }


class PhraseAndEvents:
    def __init__(
        self,
        phrase: str,
        phrase_number: int,
        start_time: float,
        end_time: float,
        entered_phrase: str,
        events: list[AddEvent | DeleteEvent | EndPhraseEvent],
    ) -> None:
        self.phrase = phrase
        self.phrase_number = phrase_number
        self.start_time = start_time
        self.end_time = end_time
        self.entered_phrase = entered_phrase
        self.events = events

    def to_dict(self):
        return {
            "phrase": self.phrase,
            "phrase_number": self.phrase_number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "entered_phrase": self.entered_phrase,
            "events": [event.to_dict() for event in self.events],
        }


class MeasureTextEntryPerformance:
    def __init__(self, phrase_set: list[str]) -> None:
        self.phrase_set = phrase_set

        self.list_of_phrase_and_events: list[PhraseAndEvents] = []

        self.number_of_current_phrase = 0
        self.start_time_of_current_phrase: None | float = None
        self.end_time_of_current_phrase: None | float = None
        self.events_of_current_phrase: list[
            AddEvent | DeleteEvent | EndPhraseEvent
        ] = []

    def add_new_input(self, input: str | None):
        """
        this is called when new input is occurred

        (in the case of word-level input)

        When the input is a word, call this function with input=word.

        Even if the input is not a word, call this function with input=None to start timer.
        """

        now = time.time()

        if self.start_time_of_current_phrase is None:
            self.start_time_of_current_phrase = now
            print("start timer of current phrase")

        if input is not None:
            self.end_time_of_current_phrase = now
            print("input is occurred. end time of current phrase is updated")

        self.events_of_current_phrase.append(
            AddEvent(
                timestamp=now,
                added_input="" if input is None else input,
            )
        )

    def add_delete(self, deleted_length: int, deleted_str: str | None = None):
        now = time.time()

        self.events_of_current_phrase.append(
            DeleteEvent(
                timestamp=now,
                deleted_length=deleted_length,
                deleted_str=deleted_str,
            )
        )

    def end_phrase(self, entered_phrase: str):
        now = time.time()

        self.events_of_current_phrase.append(
            EndPhraseEvent(
                timestamp=now,
                entered_phrase=entered_phrase,
            )
        )

        if self.number_of_current_phrase + 1 <= len(self.phrase_set):
            self.list_of_phrase_and_events.append(
                PhraseAndEvents(
                    phrase=self.phrase_set[self.number_of_current_phrase],
                    phrase_number=self.number_of_current_phrase,
                    start_time=self.start_time_of_current_phrase,
                    end_time=self.end_time_of_current_phrase,
                    entered_phrase=entered_phrase,
                    events=self.events_of_current_phrase,
                )
            )

            self.number_of_current_phrase += 1
            self.start_time_of_current_phrase = None
            self.end_time_of_current_phrase = None
            self.events_of_current_phrase = []

    def get_current_phrase_count(self) -> int:
        return self.number_of_current_phrase

    def export(self) -> list[dict[str, Any]]:
        dict_list = [pe.to_dict() for pe in self.list_of_phrase_and_events]

        return dict_list
