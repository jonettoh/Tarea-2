from multiprocessing import connection
from unittest import result
from database.db import get_connection
from .entities.flight import Flight, FlightDetail
from flask import jsonify
import json

class FlightModel():

    @classmethod
    def get_flights(self):
        try:
            connection = get_connection()
            flights=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT flight_id, departure, destination FROM flights" )
                results= cursor.fetchall()

                for row in results:
                    flight= Flight(row[0],row[1], row[2])
                    flights.append(flight.to_JSON())
            connection.close()
            return flights
        

        except Exception as ex:
            raise ex

    @classmethod
    def get_flight(self,id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT flight_id, departure, destination, total_distance, traveled_distance, bearing, position FROM flights WHERE flight_id= %s",(id,) )
                result= cursor.fetchone()

                flight= None
                if result != None:
                    flight= FlightDetail(result[0],result[1],result[2], result[3], result[4],result[5],result[6],)
                    flight = flight.to_JSON()
    
            connection.close()
            return flight
        

        except Exception as ex:
            raise ex
    
    @classmethod
    def add_flight(self,flight):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO flights (flight_id, departure, destination,total_distance,traveled_distance,bearing,position) VALUES (%s,%s,%s,%s,%s,%s,%s)",(flight.flight_id, json.dumps(flight.departure),json.dumps(flight.destination),flight.total_distance,flight.traveled_distance,flight.bearing,json.dumps(flight.position) ) )
                affected_rows = cursor.rowcount
                connection.commit()     
            
            connection.close()
            return affected_rows
        

        except Exception as ex:
            raise ex

    @classmethod
    def delete_flight(self,flight_id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM flights WHERE flight_id=%s",(flight_id,) )
                affected_rows = cursor.rowcount
                connection.commit()     
            
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise ex

    @classmethod
    def update_flight(self,flight):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE flights SET name=%s WHERE flight_id = %s",(flight.name,flight.flight_id) )
                affected_rows = cursor.rowcount
                connection.commit()     
            
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise ex

    

    