from itertools import count


class Airport():

    def __init__(self, airport_id, name=None) -> None:
        self.airport_id = airport_id
        self.name = name
        
    
    def to_JSON(self):
        return{
            'id':self.airport_id,
            'name':self.name  
        }

class AirportDetail():

    def __init__(self, airport_id, name=None, country=None, city=None, position=None) -> None:
        self.airport_id = airport_id
        self.name = name
        self.country = country
        self.city = city
        self.position = position

    def to_JSON(self):
        return{
            'id':self.airport_id,
            'name':self.name,
            'country':self.country,
            'city': self.city,
            'position':self.position
        }