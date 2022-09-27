from multiprocessing import connection
import re
from database.db import get_connection
from .entities.airport import Airport, AirportDetail
import json

class AirportModel():

    @classmethod
    def get_airports(self):
        try:
            connection = get_connection()
            airports=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT airport_id, name FROM airports" )
                results= cursor.fetchall()

                for row in results:
                    airport= Airport(row[0],row[1])
                    airports.append(airport.to_JSON())
            connection.close()
            return airports
        

        except Exception as ex:
            raise ex

    @classmethod
    def get_airport(self,id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT airport_id, name, country, city, position FROM airports WHERE airport_id= %s",(id,) )
                result= cursor.fetchone()

                airport= None
                if result != None:
                    airport= AirportDetail(result[0],result[1],result[2], result[3], result[4])
                    airport = airport.to_JSON()
            connection.close()
            return airport
        

        except Exception as ex:
            raise ex
    
    @classmethod
    def add_airport(self,airport):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO airports (airport_id, name, country, city, position) VALUES (%s,%s,%s,%s,%s)",(airport.airport_id, airport.name, airport.country, airport.city, json.dumps(airport.position)) )
                affected_rows = cursor.rowcount
                connection.commit()     
            
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise ex

    @classmethod
    def delete_airport(self,airport_id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM airports WHERE airport_id=%s",(airport_id,) )
                affected_rows = cursor.rowcount
                connection.commit()     
            
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise ex

    @classmethod
    def update_airport(self,airport):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE airports SET name=%s WHERE airport_id = %s",(airport.name,airport.airport_id) )
                affected_rows = cursor.rowcount
                connection.commit()     
            
            connection.close()
            return affected_rows
        
        except Exception as ex:
            raise ex