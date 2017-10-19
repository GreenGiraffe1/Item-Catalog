from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Catagory, Item


#Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Show all Home Page
@app.route('/')
def showHome():
    # restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    catagories = session.query(Catagory).order_by(asc(Catagory.name))
    processors = session.query(Item).order_by(asc(Item.name))
    return render_template('home.html', processors=processors, catagories=catagories)

@app.route('/categorysummary/')
def showSummary():
    return render_template('categorysummarypublic.html')

















if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)


# END
