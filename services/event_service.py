from data_store import events
from models.events import Event
from utils.generator import generate_id


class EventService:

    @staticmethod
    def create_event(title, location, date, organizer_id):
        event = Event(
            generate_id(),
            title,
            location,
            date,
            organizer_id
        )

        events.append(event)

        print("Wydarzenie zostało utworzone")
        return event

    @staticmethod
    def list_events(user_role=None):
        if not events:
            print("Brak wydarzeń")
            return
        print("Lista wydarzeń:")
        for event in events:
            print(f"ID: {event.event_id} \n {event}")

