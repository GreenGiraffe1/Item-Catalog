"""
Setup database.
"""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    """Object holding information about individual registered users"""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """return User object data in serializable format"""
        return {
            'name':     self.name,
            'email':    self.email,
            'picture':  self.picture,
            'id':       self.id,
        }


class Category(Base):
    """Object holding information about item categories"""

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """return Category object data in serializable format"""
        return {
            'name': self.name,
            'id':   self.id,
        }


class Item(Base):
    """Object holding information about individual catalog items"""

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(5000), nullable=False)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category")

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    @property
    def serialize(self):
        """return Item object data in serializable format"""
        return {
            'name':        self.name,
            'description': self.description,
            'id':          self.id,
        }

#  The Database must be created before this script will run successfully
engine = create_engine('postgresql+psycopg2://ubuntu:ubuntu'
                       + '@localhost/itemcatalog.db', echo=True)
#     !!! Change "False" to "True" to debug the SQL !!!

# engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)

print "Database has been setup, and its tables defined"
