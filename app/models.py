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
    description=db.Column(db.String(2000))
    make=db.Column(db.String(100))
    model=db.Column(db.String(100))
    colour=db.Column(db.String(100))
    year=db.Column(db.String(100))
    transmission=db.Column(db.String(100))
    car_type=db.Column(db.String(100))
    price=db.Column(db.Float)
    photo=db.Column(db.String(100))
    user_id=db.Column(db.Integer)#, db.ForeignKey('users.id'))
    #favourites=db.relationship('Favourites', backref='cars')

    def __init__(self,description,make,model,colour,year,transmission,car_type,price,photo,userid):
        self.description = description
        self.make = make
        self.model = model
        self.colour = colour
        self.year = year
        self.transmission = transmission
        self.car_type = car_type
        self.price = price
        self.photo = photo
        self.userid= userid




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
    car_id = db.Column(db.Integer)#, db.ForeignKey('cars.id'))
    user_id = db.Column(db.Integer)#, db.ForeignKey('users.id'))

    
    
    def __init__(self,car_id,user_id):
        self.car_id = car_id
        self.user_id = user_id


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
    username = db.Column(db.String(200))
    password = db.Column(db.String(300))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    location = db.Column(db.String(255))
    biography = db.Column(db.String(2500))
    photo = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime())#, default=datetime.utcnow)
   # cars=db.relationship('Cars', backref='users')
    #favourites=db.relationship('Favourites', backref='users')
    
    
    

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
