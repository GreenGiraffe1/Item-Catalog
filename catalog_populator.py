from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catagory, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user1 = User(name="Matt-Bott",
             email="heddy@ahed.com")
            #  picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Menu for UrbanBurger
catagory1 = Catagory(name="Computer Processors")
session.add(catagory1)
session.commit()

item1 = Item(user_id=1, name="Intel i7-7700K", description="4 cores, 8 threads running at base-clock of 4.2GHz",
             catagory=catagory1)

session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Intel i5-7600K", description="4 cores, 4 threads running at base-clock of 3.8GHz",
             catagory=catagory1)

session.add(item2)
session.commit()







print "Added Items & Catagories to App!"

# END
