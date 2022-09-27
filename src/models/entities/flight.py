from itertools import count


class Flight():

    def __init__(self, id, departure=None, destination=None) -> None:
        self.id = id
        self.departure = departure
        self.destination = destination
        
    
    def to_JSON(self):
        return{
            'id':self.id,
            'departure':self.departure,
            'destination':self.destination
        }

class FlightDetail():

    def __init__(self, flight_id, departure=None, destination=None, total_distance=None, traveled_distance=None,bearing=None, position=None) -> None:
        self.flight_id = flight_id
        self.departure = departure
        self.destination = destination
        self.total_distance = float(total_distance)
        self.traveled_distance = float(traveled_distance)
        self.bearing = float(bearing)
        self.position = position

    def to_JSON(self):
        return{
            "id":self.flight_id,
            'departure': self.departure,
            'destination': self.destination,
            'total_distance': self.total_distance,
            'traveled_distance': self.traveled_distance,
            'bearing': self.bearing,
            'position': self.position
        }