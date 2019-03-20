#!/usr/bin/env python

__author__ = 'jhoelzer'

import requests
import time
import turtle


def astronaut_list():
    url = 'http://api.open-notify.org/astros.json'
    res = requests.get(url)
    res_data = res.json()

    print('Number of astronauts in space {}'.format(res_data['number']))

    for astronaut in res_data['people']:
        print('{} is aboard the {}'.format(
            astronaut['name'], astronaut['craft']))


def coordinates():
    url = 'http://api.open-notify.org/iss-now.json'
    res = requests.get(url)
    res_data = res.json()
    latitude = res_data['iss_position']['latitude']
    longitude = res_data['iss_position']['longitude']
    timestamp = time.ctime(res_data['timestamp'])

    print('Latitude: {} \n Longitude: {} \n Time: {}'.format(
        latitude, longitude, timestamp))

    return (latitude, longitude, timestamp)


def create_screen():
    screen = turtle.Screen()
    screen.setup(width=720, height=360, startx=None, starty=None)
    screen.bgpic('map.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)

    return screen


def iss_map(screen, latitude, longitude):
    iss = turtle.Turtle()
    screen.register_shape('iss.gif')
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    iss.goto(float(longitude), float(latitude))


def indy_pass_time(latitude, longitude):
    url = 'http://api.open-notify.org/iss-pass.json'
    coord = {'lat': 39.7684, 'lon': -86.1581}
    res = requests.get(url, params=coord)
    pass_time = time.ctime(res.json()['response'][0]['risetime'])

    return pass_time


def iss_dot(latitude, longitude, timestamp):
    indy = turtle.Turtle()
    indy.penup()
    indy.color('red')
    indy.goto(longitude, latitude)
    indy.dot(5)
    indy.hideturtle()
    indy.write(indy_pass_time(latitude, longitude))


def indy_coordinates():
    indy_latitude = 39.7684
    indy_longitude = -86.1581
    indy_time = indy_pass_time(indy_latitude, indy_longitude)
    iss_dot(indy_latitude, indy_longitude, indy_time)


def main():
    screen = create_screen()

    print('Astronauts: {}'.format(astronaut_list))
    print('ISS Coordinates: ')
    longitude, latitude, timestamp = coordinates()
    iss_map(screen, latitude, longitude)
    indy_coordinates()
    print('Indianapolis Pass Over Time: {}'.format(
        indy_pass_time(latitude, longitude)))

    screen.exitonclick()


if __name__ == '__main__':
    main()
