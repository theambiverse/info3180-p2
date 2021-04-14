from . import db

#db.create_all()
from datetime import datetime
from werkzeug.security import generate_password_hash

class Cars(db.Model): #one-to-one
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(255))
    make=db.Column(db.String(80))
    model=db.Column(db.String(80))
    colour=db.Column(db.String(80))
    year=db.Column(db.String(80))
    transmission=db.Column(db.String(80))
    car_type=db.Column(db.String(80))
    price=db.Column(db.Float)
    photo=db.Column(db.String(80))
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    favourites=db.relationship('Favourites', backref='cars')



    

    #def __init__(self, title,desc,bedroom,bathroom,price,location,propertytype,photoname):
    #   self.title = title
     #   self.desc=desc
      #  self.bedroom=bedroom
       # self.bathroom=bathroom
        #self.price=price
      #  self.location=location
       # self.propertytype=propertytype
        #self.photoname=photoname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Title %r>' % (self.description)

class Favourites(db.Model): #
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    
    
    

    #def __init__(self, title,desc,bedroom,bathroom,price,location,propertytype,photoname):
    #   self.title = title
     #   self.desc=desc
      #  self.bedroom=bedroom
       # self.bathroom=bathroom
        #self.price=price
      #  self.location=location
       # self.propertytype=propertytype
        #self.photoname=photoname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Title %r>' % (self.car_id)

class Users(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(80))
    biography = db.Column(db.String(255))
    photo = db.Column(db.String(80))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    cars=db.relationship('Cars', backref='users')
    favourites=db.relationship('Favourites', backref='users')
    
    
    

    def __init__(self, name, username, password, email,location,biography,photo,date_joined,):
        self.email=email
        self.location=location
        self.biography=biography
        self.photo=photo
        self.date_joined=date_joined
        self.name = name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Title %r>' % (self.username)
