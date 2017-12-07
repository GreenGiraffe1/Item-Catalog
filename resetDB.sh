#!/bin/bash


# Drops Database & Re-creates it fresh
psql -f refreshDB.sql

# Removes leftovers from last DB setup
rm database_setup.pyc

# Sets up the database and its tables
python database_setup.py

# Populates the DB with info
python catalog_populator.py

# Restarts the server
python catalog_main.py
