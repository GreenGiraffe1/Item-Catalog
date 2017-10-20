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
@app.route('/home/')
def showHome():
    # restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    catagories = session.query(Catagory).order_by(asc(Catagory.name))
    processors = session.query(Item).order_by(asc(Item.name))
    return render_template('home.html', processors=processors, catagories=catagories)

@app.route('/category/<int:catagory_id>/')
def showSummary(catagory_id):
    catagory = session.query(Catagory).filter_by(id=catagory_id).one()
    items = session.query(Item).filter_by(catagory_id=catagory_id).all()
    return render_template('categorysummary.html', catagory=catagory, items=items)




@app.route('/item/<int:item_id>/')
def showItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('itemdetails.html', item=item)

@app.route('/item/<int:item_id>/edit/', methods=['GET','POST'])
def editItem(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    catagories = session.query(Catagory).all()
    if request.method == 'POST':
        if not (request.form['name'] and request.form['description'] and request.form['catagory']):
            flash('All fields must be specified to edit an new item.')
            return redirect(url_for('editItem', item_id=item_id))
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['catagory']:
            editedItem.catagory_id = request.form['catagory']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItem', item_id=item_id))
    else:
        return render_template('edititem.html', item=editedItem, catagories=catagories)


@app.route('/item/<int:item_id>/delete/', methods=['GET','POST'])
def deleteItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showHome'))
    else:
        return render_template('deleteitem.html', item=item)

@app.route('/item/new/', methods=['GET','POST'])
def newItem():
    catagories = session.query(Catagory).all()
    if request.method == 'POST':
        if not (request.form['name'] and request.form['description'] and request.form['catagory']):
            flash('All fields must be specified to create a new item.')
            return redirect(url_for('newItem'))
        newItem = Item(name=request.form['name'], description=request.form['description'], catagory_id=request.form['catagory'], user_id=1)
        session.add(newItem)
        session.commit()
        flash('New Item Successfully Created')
        return redirect(url_for('showHome'))
    else:
        return render_template('newitem.html', catagories=catagories)






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)


# END
