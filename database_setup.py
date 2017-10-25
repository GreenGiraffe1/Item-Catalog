from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

	@property
	def serialize(self):
		"""return object data in serializable format"""
		return {
			'name'      :   self.name,
			'email'     :   self.email,
			'picture'   :   self.picture,
			'id'        :   self.id,
		}

class Catagory(Base):
	__tablename__ = 'catagory'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	@property
	def serialize(self):
		"""return object data in serializable format"""
		return {
			'name'  :   self.name,
			'id'    :   self.id,
		}


class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(5000), nullable=False)
	catagory_id = Column(Integer, ForeignKey('catagory.id'))
	catagory = relationship(Catagory)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""return object data in serializable format"""
		return {
			'name'          : self.name,
			'description'   : self.description,
			'id'            : self.id,
		}





engine = create_engine('sqlite:///itemcatalog.db')


Base.metadata.create_all(engine)
