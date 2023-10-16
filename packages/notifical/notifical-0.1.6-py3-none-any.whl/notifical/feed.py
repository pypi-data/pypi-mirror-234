from typing import List, Optional, Callable
from dataclasses import dataclass, field
from icalendar import Event, Calendar
from datetime import datetime, timedelta
import re
import requests
from itertools import product

@dataclass
class EventMatch(object):
    unique_event_id: str
    ical_event: Event
    fire_function: Callable
    fire_time: datetime

@dataclass
class EventTrigger(object):
    summary_regex: Optional[re.Pattern] = None
    description_regex: Optional[re.Pattern] = None
    trigger: Callable = lambda:None
    offset: int = 0

    @staticmethod
    def _ical_field():
        raise Exception("implement this method")
    
    def match(self, event: Event) -> Optional[EventMatch]:
        esummary = event.get('SUMMARY', "")
        edescription = event.get('DESCRIPTION', "")
        if self.summary_regex and not self.summary_regex.search(esummary):
            return None
        if self.description_regex and not self.description_regex.search(edescription):
            return None

        etime = event[self._ical_field()].dt
        odelta = timedelta(seconds=abs(self.offset))
        if self.offset < 0:
            fire_time = etime - odelta
        else:
            fire_time = etime + odelta

        event_uid = event['UID']
        event_rid = event.get('RECURRENCE-ID','single')
        event_key = f"{event_uid}:{event_rid}"
        return EventMatch(
            event_key,
            event,
            self.trigger,
            fire_time
        )

@dataclass
class EventStartTrigger(EventTrigger):
    name: str = "Event Start Trigger"
    
    @staticmethod
    def _ical_field():
        return "DTSTART"

@dataclass
class EventEndTrigger(EventTrigger):
    name: str = "Event End Trigger"
    
    @staticmethod
    def _ical_field():
        return "DTEND"

@dataclass
class Feed(object):
    url: str
    triggers: List[EventTrigger] = field(default_factory=lambda:[])
    refresh_interval: int = 300

    def fetch(self) -> List[EventMatch]:
        resp = requests.get(self.url)
        cal = Calendar.from_ical(resp.content)
        return list(filter(lambda a: a != None, map(lambda tup: tup[0].match(tup[1]), product(self.triggers, cal.walk("VEVENT")))))
