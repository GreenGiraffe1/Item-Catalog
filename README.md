# Catalog Web App

**Catalog Web App** is a project that displays a catalog of items, and
allows users to interact with them. Component items are organized into one
of several categories. The items can be displayed as one long comprehensive
list, or grouped into sub-lists by category. An item's detailed description
can be viewed by clicking on an item. **Catalog Web App** supports user
registration, and logging via Facebook Login or Google Login OAuth2.0
verification. User's who are signed-in are able to create new items, and
edit or delete items they've created. Permissions are in place to prevent
users from modifying other users' content, and to prevent non-registered
users from doing the same, or from creating new content themselves.

## Setup:
This application is designed so it can easily be deployed to a Linux web
server, or to a virtual machine (VM) for testing. In either case, begin by
making sure you have an active Internet connection and Python 2.7x installed
on the system. For the VM, Oracle VirtualBox must be installed on the
system. Clone all files from this GitHub repository to the same directory.

##### Setup a virtual machine (option 1):
In the local directory where you cloned all the files run ```vagrant up```.
This will download and install the virtual machine(VM) to your computer
according to the specifications in ```Vagrantfile```.  Once the VM is up
type ```vagrant ssh``` in the terminal to login to the VM. The cloned files
in your local directory will be available inside the VM at directory
location: ```/vagrant/```.

##### Setup a Web server (option 2):
There are many possible configurations, but these are outside the scope of
this README. Please consult the documentation for your preferred Web hosting
software and provider.

This Web app has been tested to work with Apache server software in an
Amazon Web Services (AWS) virtual instance, running Ubuntu Server.

##### Setup the PostgreSQL Database
Unless already installed, you'll need to download and install the
open-source database software for [PostgreSQL](https://www.postgresql.org/),
[SQLAlchemy](https://www.sqlalchemy.org/), and
[Psycopg2](http://initd.org/psycopg/).  Depending on your Linux distribution
this software may be available from your package manager. After all three
have been installed, start up PostgreSQL from the shell terminal. Create a
new user and supply a password (This is the user the Web app will use to
access the database). Create a new database named ```itemcatalog.db```. Next
you'll need to modify the database connection string in the following three
files: ```database_setup.py```, ```catalog_populator.py```,
and ```catalog_main.py```. Please refer to
[SQLAlchemy's documentation](https://docs.sqlalchemy.org/en/rel_1_1/
dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2)
for instruction on how to modify the connection string for your host
environment.

#####  Initialize & Populate the database.
From your server / VM shell terminal, where the cloned files are present,
run ```database_setup.py``` to create the database. At this point you will
need to give your database's user permission to modify the tables that were
just created. From the SQL prompt execute the following statement for each of
the tables: ```GRANT ALL PRIVILEGES ON TABLE [table_name] TO [user_name];```
Finally, populate the tables with test data by
running ```catalog_populator.py```.


##### Create accounts with Facebook and Google, and create a new app ID with each provider:

* For **Google**, you'll go to their
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
* For **Facebook** you'll go to their
[developer site](https://developers.facebook.com/), sign-in, and in the
top-right corner, in the drop-down menu, select add a new App. You'll give it
a name, and on the next page you'll click "+Add Product" and choose "Facebook
Login". Under settings you'll enter in your redirect URI for your project.
You'll need to add the App ID, and client secrets to the
file ```fb_client_secrets_TEMPLATE.json```. You'll also add the App ID
to ```login.html``` where the Facebook JavaScript SDK is initialized.

## Usage:
After all the setup steps are complete, you should have a fully functioning
Web app. If using the virtual machine run ```catalog_main.py```. You will
see the debugger open, and a series of GET requests will be logged. Your
the application should be accessible from your browser at the
address ```127.0.0.1:8000``` or ```localhost:8000```. At this point all
functionality will be active and users can begin logging-in and
adding content.

## Attribution:
This project was created while I was taking the Udacity Full-Stack Nanodegree,
and significant chunks of the structure / ideas behind the structure were
provided by the course author. Specifically, the OAuth2.0 / social login code
is based heavily on that provided by the course, and the general structure of
the application is inspired heavily be the course author's guidance. The
file ```fb_client_secrets_TEMPLATE``` was also provided by the course author.
The [Flask](http://flask.pocoo.org/) framework for Python is used to simplify
the design functionality of the Web app. This project uses the
[OAuth2.0](https://oauth.net/2/) library to support 3rd party login from
[Facebook](https://www.facebook.com) & [Google](https://www.google.com).
[SQLAlchemy](http://www.sqlalchemy.org/) is employed as an Object Relational
Mapper (ORM) to allow me to make full use of a SQL backed database inside this
Python application. The [Bootstrap](https://getbootstrap.com) framework is
used to organized the user interface.

In deploying this project to Amazon Web Services (AWS) I made heavy reference
use of this [tutorial](https://amunategui.github.io/idea-to-pitch/) written
by Manuel Amunategui. Additionally, this
[forum post](https://discussions.udacity.com/t/solved-configuring-linux-
google-oauth-invalid-request/376259) by fellow Udacity student with
username ```vivilearnstocode2_4i``` was key in getting Facebook and Google
logins to work with this app once it was deployed to AWS.

## License:
**Catalog Web App** is a public domain work, with license
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
