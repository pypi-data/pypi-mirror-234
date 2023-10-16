import requests
from notifical.feed import Feed, EventMatch
from notifical.config import Config

import asyncio

from icalendar import Calendar
from datetime import datetime, timezone
from typing import List

from dataclasses import dataclass

EVENT_LOOP_SPEED = 300 # polling frequency.  Must be > 2*BUFFER
BUFFER = 20 # This should be at least 2x the time it takes to fetch cal and process

async def sleep_and_fire(seconds, func):
    print(f"Waiting {seconds} seconds")
    await asyncio.sleep(seconds)
    await func() 


@dataclass
class EventLoop(object):
    feed: Feed

    async def run_async(self) -> None:
        last_events_alerted: List[str] = []
        while True:
            results = await asyncio.gather(
                self._schedule_near_events(last_events_alerted),
                asyncio.sleep(self.feed.refresh_interval)
            )
            last_events_alerted = results[0]
    
    async def _schedule_near_events(self, already_alerted: List[str]):
        reftime = datetime.now(timezone.utc)
        event_matches = self.feed.fetch()
        
        def _should_schedule(em: EventMatch) -> bool:
            if em.unique_event_id in already_alerted:
                return False
            delta = em.fire_time - reftime
            delta_seconds = delta.total_seconds()
            return 0 < delta_seconds <= self.feed.refresh_interval+BUFFER
            
        fireable = list(filter(_should_schedule, event_matches))
        for f in fireable:
            now = datetime.now(timezone.utc)
            print(f"{now}: Firing for upcoming event")
            until = f.fire_time - now
            asyncio.ensure_future(sleep_and_fire(until.total_seconds(), f.fire_function))

        return [ f.unique_event_id for f in fireable ]

class Daemon(object):
    def __init__(self, *feeds: Feed):
        self.loops = [ EventLoop(f) for f in feeds ]

    async def run_async(self):
        await asyncio.gather(*[l.run_async() for l in self.loops])

    def run(self):
        asyncio.run(self.run_async())
