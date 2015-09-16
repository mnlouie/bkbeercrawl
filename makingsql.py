#!/usr/local/bin/python


"""
Usage: makingsql.py

This script reads in a json file and writes the data to a mySQL db
"""

import MySQLdb
import json

#test variables for database access
HOST = 'localhost'
USER = 'root'
PASSWD = ''
DATABASE = 'beer_db'

# beer DB data to insert into new table  ### my file was a list of dictionaries
data = []
with open('masterbeer.json') as f:
    for line in f:
        data.append(json.loads(line))

db_connect = MySQLdb.connect(
    host = HOST,
    user = USER,
    passwd = PASSWD)

cursor = db_connect.cursor()

#cursor.execute('create database full_beer_db')
#cursor.execute('CREATE DATABASE tmp_beer')
#creates the database

#cursor.execute('SHOW DATABASE')

cursor.execute('use full_beer_db')
#cursor.execute('USE tmp_beer')
cursor.execute("""
CREATE TABLE beer_info(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    brew TEXT,
    style TEXT,
    link TEXT,
    PRIMARY KEY (id)
    )
    """)


add_beer = ("INSERT INTO beer_info "
           " (name, description, brew, style, link)"
           " VALUES (%s, %s, %s, %s, %s)")
#beer_data = ('Test Ale', 'GREAT BEER', 'insight brewery', 'ale', 'website')


for li in data:
    for da in li:
        beer_data = (da, li[da][0],li[da][1],li[da][2],li[da][3])
        cursor.execute(add_beer, beer_data)


# commit the things you execute
db_connect.commit()

cursor.close()
db_connect.close()
