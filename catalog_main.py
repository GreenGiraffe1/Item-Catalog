"""
Catalog Web App is a project that displays a catalog of items, and
allows users to interact with them. Component items are organized into
one of several categories. The items can be displayed as one long
comprehensive list, or grouped into sub-lists by category. An item's
detailed description can be viewed by clicking on an item. Catalog Web
App supports user registration, and logging via Facebook Login or
Google Login OAuth2.0 verification. User's who are signed-in are able
to create new items, and edit or delete items they've created.
Permissions are in place to prevent users from modifying other
users' content, and to prevent non-registered users from doing the
same, or from creating new content themselves.
"""


import httplib2
import json
import requests
import random
import string

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response, flash
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from database_setup import Base, User, Catagory, Item


app = Flask(__name__)
CLIENT_ID = (json.loads(open('client_secrets.json', 'r').read())
                                                         ['web']['client_id'])
APPLICATION_NAME = "Catalog Web App"
#Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    """Display catalog home page."""
    catagories = session.query(Catagory).order_by(asc(Catagory.name))
    processors = session.query(Item).order_by(asc(Item.name))
    if 'username' not in login_session:
        return render_template('homepublic.html', processors=processors,
                                catagories=catagories)
    else:
        catagories = session.query(Catagory).order_by(asc(Catagory.name))
        processors = session.query(Item).order_by(asc(Item.name))
        return render_template('home.html', processors=processors,
                                catagories=catagories,
                                username=login_session['username'],
                                picture=login_session['picture'])


@app.route('/category/<int:catagory_id>/')
def showSummary(catagory_id):
    """Display all items belonging to the category selected."""
    catagory = session.query(Catagory).filter_by(id=catagory_id).one()
    items = session.query(Item).filter_by(catagory_id=catagory_id).all()
    if 'username' not in login_session:
        return render_template('categorysummarypublic.html',
                               catagory=catagory,
                               items=items)
    else:
        return render_template('categorysummary.html', catagory=catagory,
                                items=items,
                                username=login_session['username'],
                                picture=login_session['picture'])


@app.route('/item/<int:item_id>/')
def showItem(item_id):
    """Displays details page for the selected item."""
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('itemdetailspublic.html', item=item)
    if login_session['user_id'] != item.user_id:
        return render_template('itemdetailspublic.html', item=item,
                               username=login_session['username'],
                               picture=login_session['picture'])
    else:
        return render_template('itemdetails.html', item=item,
                               username=login_session['username'],
                               picture=login_session['picture'])


@app.route('/item/<int:item_id>/edit/', methods=['GET','POST'])
def editItem(item_id):
    """Display page where a signed-in item creator can update the
    selected item's details.
    """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    catagories = session.query(Catagory).all()
    if login_session['user_id'] != editedItem.user_id:
        return ("<script>function myFunction() {alert('You are not "
                + "authorized to edit this item. Please create your "
                + "own items in order to edit them.');}</script><body "
                + "onload='myFunction()''>")
    if request.method == 'POST':
        if not (request.form['name'] and request.form['description']
                and request.form['catagory']):
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
        return render_template('edititem.html', item=editedItem,
                                catagories=catagories,
                                username=login_session['username'],
                                picture=login_session['picture'])


@app.route('/item/<int:item_id>/delete/', methods=['GET','POST'])
def deleteItem(item_id):
    """Display page where a signed-in item creator can delete the
    selected item.
    """
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != item.user_id:
        return ("<script>function myFunction() {alert('You are not "
                + "authorized to delete this item. Please create your "
                + "own items in order to delete them.');}</script>"
                + "<body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html', item=item,
                               username=login_session['username'],
                               picture=login_session['picture'])


@app.route('/item/new/', methods=['GET','POST'])
def newItem():
    """Display page where sign-in users can create new items."""
    if 'username' not in login_session:
        return redirect('/login')
    catagories = session.query(Catagory).all()
    if request.method == 'POST':
        if not (request.form['name'] and request.form['description']
                and request.form['catagory']):
            flash('All fields must be specified to create a new item.')
            return redirect(url_for('newItem'))
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       catagory_id=request.form['catagory'],
                       user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item Successfully Created')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newitem.html', catagories=catagories,
                               username=login_session['username'],
                               picture=login_session['picture'])


@app.route('/login')
def showLogin():
    """Display the login page."""
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# JSON API's
# Item Details
@app.route('/item/<int:item_id>/JSON')
def itemJSON(item_id):
    """Display detailed information about the selected item in JSON
    format.
    """
    itemDetails = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item_Details=itemDetails.serialize)


#Items by category - List All
@app.route('/JSON')
@app.route('/catalog/JSON')
def allItemsJSON():
    """Display detailed information for all the items in the database
    in JSON format.
    """
    items = session.query(Item).order_by(asc(Item.name))
    return jsonify(Item_List=[i.serialize for i in items])


# User Helper Functions
def create_user(login_session):
    """Creates a new user in the User table of the database given a
    valid login session.
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def get_user_info(user_id):
    """Retrieve and return a user's info, given a valid user ID as
    input.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user

def get_user_id(email):
    """Retrieve and return a user's ID, given a valid user email as
    input.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Log users into their Facebook accounts and the Web app.

    Log users into Facebook and the Web app if their login
    details are correct, and their session state and server states
    match (indicating the no 3rd party is attempting to hi-jack
    the session). Create new user in the User table of the database
    if this is the first time a particular user has logged in.
    Flash confirmation message when a user successfully logs in, or
    an error message when log-in is unsuccessful.
    """7
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    app_id = (json.loads(open('fb_client_secrets.json', 'r')
              .read())['web']['app_id'])
    app_secret = (json.loads(open('fb_client_secrets.json', 'r')
                  .read())['web']['app_secret'])
    url = ('https://graph.facebook.com/oauth/access_token?grant_'
          + 'type=fb_exchange_token&client_id=%s&client_secret=%s&fb_'
          + 'exchange_token=%s') % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.10/me"
    # format result to pull out and store long-lived access token
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = ('https://graph.facebook.com/v2.10/me?access_token=%s&fields=name'
          + ',id,email') % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token
    # Get user picture
    url = ('https://graph.facebook.com/v2.10/me/picture?access_token=%s'
          + '&redirect=0&height=200&width=200') % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]
    # see if user exists in my database - if not add them
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """Disconnects users logged-in from their Facebook accounts."""
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s'
          % (facebook_id,access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Log users into their Google accounts and the Web app.

    Log users into Google and the Web app if their login
    details are correct, and their session state and server states
    match (indicating the no 3rd party is attempting to hi-jack
    the session). Create new user in the User table of the database
    if this is the first time a particular user has logged in.
    Flash confirmation message when a user successfully logs in, or
    an error message when log-in is unsuccessful.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                           + 'connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # Set user_id , and create new user in database, if they are new.
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnects users logged-in from their Google accounts."""
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
          % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        response = make_response(json.dumps('Successfully disconnected.'),
                                            200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given'
                                           + ' user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    """Disconnect users regardless of which login method they used.

    Calls logout function specific to login service used, and then
    deletes all login-session information. Displays a confirmation
    message upon succesful logout, or an error otherwise.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['access_token']
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        if login_session:
            print 'this is the state of the login session'
            print login_session
        else:
            print 'no login_session'
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
