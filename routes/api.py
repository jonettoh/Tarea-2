
#from msilib.schema import ProgId
from turtle import distance, position
from urllib import response
from flask import Blueprint, jsonify, request
import json
import requests
from models.AirportModel import AirportModel

from models.entities.airport import Airport, AirportDetail

from models.FlightModel import FlightModel
from models.entities.flight import Flight, FlightDetail
import psycopg2

main=Blueprint('api_blueprint', __name__)


#get all airtports
@main.route('/airports')
def get_airports():

    try:
        airports = AirportModel.get_airports()
        return jsonify(airports)
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500

#get a single airportdetail
@main.route('/airports/<airport_id>')
def get_airport(airport_id):

    try:
        airport = AirportModel.get_airport(airport_id)
        if airport != None:
            return jsonify(airport), 200
        else:
            return '', 404
    except Exception as ex:
        return jsonify({'error': 'Missing parameter: %s'%(type(ex))}), 400

#add an airportdetail
@main.route('/airports', methods=['POST'])
def add_airport():

    try:
        #aca se puede agregar la validacion a cada dato
        #manejo de id en minuto 57
        airport_id = request.json['id']
        name=request.json['name']
        country=request.json['country']
        city=request.json['city']
        position = request.json['position']
        airport = AirportDetail(airport_id,name,country,city,position)
        affected_rows=AirportModel.add_airport(airport)
        if affected_rows ==1:
            return airport.to_JSON(), 201
        else:
            return jsonify({'message':"Error on insert"}), 500
    except psycopg2.errors.UniqueViolation as ex:
        return jsonify({'error': 'Airport with id %s already exists'%(airport_id)}), 409
    except KeyError as ex:
        return jsonify({'error': 'Missing parameter: %s'%(ex)}), 400
    except Exception as ex:
        return jsonify({'error': 'Missing parameter: %s'%(type(ex))}), 400


#borrar un aeropuerto
@main.route('/airports/<airport_id>', methods=['DELETE'])
def delete_airport(airport_id):

    try:
        #aca se puede agregar la validacion a cada dato
        #manejo de id en minuto 57
    
        affected_rows=AirportModel.delete_airport(airport_id)
        if affected_rows ==1:
            return '',204
        else:
            return jsonify({'error': "Airport with id %s not found"%(airport_id)}), 404
    except Exception as ex:
        return jsonify({'error': '%s'%(type(ex))}), 400


#actualizar nombre de aeropuerto
@main.route('/airports/<airport_id>', methods=['PATCH'])
def update_airport(airport_id):

    try:
        #aca se puede agregar la validacion a cada dato
        #manejo de id en minuto 57
        #airport_id = request.json['airport_id']
        name=request.json['name']
        airport = Airport(airport_id,name)

        affected_rows=AirportModel.update_airport(airport)
        if affected_rows ==1:
            return '',204
        else:
            return jsonify({'message':"Error on update"}), 404
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500


#get all flights
@main.route('/flights')
def get_flights():

    try:
        flights = FlightModel.get_flights()
        return jsonify(flights), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500

#get a single flightdetail
@main.route('/flights/<flight_id>')
def get_flight(flight_id):

    try:
        flight = FlightModel.get_flight(flight_id)
        if flight != None:
            return jsonify(flight), 200
        else:
            return '', 404
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500

#add an flightdetail
@main.route('/flights', methods=['POST'])
def add_flight():

    try:
        #aca se puede agregar la validacion a cada dato
        #manejo de id en minuto 57
        flight_id = request.json['id']
        departure=request.json['departure']
        destination=request.json['destination']
        origin = AirportModel.get_airport(departure)
        landing = AirportModel.get_airport(destination)
        lat1 = origin['position']['lat']
        lat2 = landing['position']['lat']
        long1 = origin['position']['long']
        long2 = landing['position']['long']
        url = "https://tarea-2.2022-2.tallerdeintegracion.cl/distance?initial=%s,%s&final=%s,%s"%(lat1,long1,lat2,long2,)
        response = requests.get(url).json()
        flight = FlightDetail(flight_id,departure,destination,response['distance'],0,response['bearing'],origin['position'])
        affected_rows=FlightModel.add_flight(flight)
        if affected_rows ==1:
            return flight.to_JSON(), 201
        else:
            return jsonify({'message':"Error on insert"}), 500
    except Exception as ex:
        return jsonify({'error': 'Missing parameter:'+str(ex)}), 400


#borrar un vuelo
@main.route('/flights/<flight_id>', methods=['DELETE'])
def delete_flight(flight_id):

    try:
        #aca se puede agregar la validacion a cada dato
        #manejo de id en minuto 57
    
        affected_rows=FlightModel.delete_flight(flight_id)
        if affected_rows ==1:
            return '',204
        else:
            return jsonify({'message':"Error on delete"}), 404
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500


#actualizar ubicacion
@main.route('/flights/<flight_id>/position', methods=['POST'])
def update_flight(flight_id):

    try:
        #aca se puede agregar la validacion a cada dato
        #manejo de id en minuto 57
        #flight_id = request.json['flight_id']
        new_position=request.json
        flight = get_flight(flight_id)
        position = flight['position']
        url = 'https://tarea-2.2022-2.tallerdeintegracion.cl/distance?initial=%s,%s&final=%s,%s',(position['lat'],position['long'],new_position['lat'],new_position['long'],)
        response = request.get(url)
        flight.position = new_position
        flight.total_distance += float(response['distance'])
        flight.bearing = float(response['bearing'])
        
        affected_rows=FlightModel.update_flight(flight)
        if affected_rows ==1:
            return '',204
        else:
            return jsonify({'message':"Error on update"}), 404
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500


@main.route('/status')
def status():
    return '',204
        