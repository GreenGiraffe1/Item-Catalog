# Catalog Web App

**Catalog Web App** is a project that display a catalog of computer
components. The component item is organized into one of several categories.
The items can be displayed by as one long comprehensive list, or grouped
into a list by selecting a particular category. An item's detailed
description can be viewed by clicking on an item. **Catalog Web App**
supports user registration, and logging via Facebook Login or Google Login
OAuth2.0 verification. User's who are signed-in are able to create new items,
and edit or delete items they've created. Permissions are in place to prevent
users from modifying other users' content, and to prevent non-registered users
from doing the same, or from creating new content themselves.

## Setup:
Begin the setup by making sure you have an active Internet connection, and
cloning all files from GitHub to the same local directory.

You'll need to sign-up for accounts with Facebook and Google if you haven't
already, and create a new app with each provider:
* For Google, you'll go to their
[developer site](https://console.developers.google.com), login, and click on
the carrot tab in the top left. It will open a menu where you'll click the
plus "+" sign to create a new project. You'll give it a name, and then click
on the "credentials"  item in the left-hand menu. Click "create credentials",
and select "OAuth client ID" from the drop-down. Click on "configure consent
screen", and fill it out for your application (only an email and product
name are required to begin). On the next page choose the radio button for
"Web Appliation", and give it a name, and enter your Authorized JavaScript
origins, and Authorized redirect URIs. You'll then be presented with your
client ID, and client secret. Add the client ID to ```login.html```, and
download the associated JSON file by clicking on the download icon to the
right. Rename the downloaded file to ```client_secrets.json``` and place it in
the main directory where you cloned this repository.
* For Facebook you'll go to their
[developer site](https://developers.facebook.com/), sign-in, and in the
top-right corner, in the drop-down menu, select add a new App. You'll give it
a name, and on the next page you'll click "+Add Product" and choose "Facebook
Login". Under settings you'll enter in your redirect URI for your project.
You'll need to add the App ID, and client secrets to the file
```fb_client_secrets.json```. You'll also add the App ID to ```login.html```
where the Facebook JavaScript SDK is initialized.


##### To deploy your this application with your own items / categories you'll need to:
* Obtain a [Google Maps API key](https://developers.google.com/maps/documentation/embed/get-api-key)


## Usage:
To begin using this WebApp, make sure all files are in the same local directory
and that you have an active Internet connection.

## Attribution:
This project was created while I was taking the Udacity Full-Stack Nanodegree,
and significant chunks of the structure / ideas behind the structure were
provided by the course author. [INSERT STUFF]

This project uses the [OAuth2.0](https://oauth.net/2/) framework to support 3rd party login.

[SQLAlchemy](http://www.sqlalchemy.org/) is employed as an Object Relational
Mapper (ORM) to allow me to make full use of a SQL backed database inside this
Python application.

[Flask](http://flask.pocoo.org/) framework for Python is used to simplify the
design functionality of the Web app.

## License:
**Catalog Web App** is a public domain work, with license
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).