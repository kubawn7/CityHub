class Event:
    def __init__(self, event_id, title, location, date, organizer_id):
        self.event_id = event_id
        self.title = title
        self.location = location
        self.date = date
        self.organizer_id = organizer_id

    def __str__(self):
        return f"------------------------------\nnazwa: {self.title}\nlokalizacja: {self.location}\ndata: {self.date}\n------------------------------"