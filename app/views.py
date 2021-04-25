"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager, csrf
from flask import render_template, request, redirect, url_for, flash, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.userforms import RegisterForm, LoginForm
from app.models import Users, Cars, Favourites
import datetime

#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

import jwt
from flask import _request_ctx_stack
from functools import wraps
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for your application.
###  

#@app.route('/') 
#def home():
 #   """Render website's home page."""
  #  return app.send_static_file('index.html')


@app.route('/api/register', methods=['POST'])
def register():

    form=RegisterForm()
    error=[]

    if request.method == 'POST':
        if form.validate_on_submit():

            username = form.username.data
            password = form.password.data
            name = form.name.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            #existing email and user error handling 
            checkname = Users.query.filter_by(username=username).first()
            checkemail = Users.query.filter_by(email=email).first()
            if checkname is None:
                if checkemail is None:
                    
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    nuser = Users(username=username, password=password, name=name, email=email,
                                    location=location, biography=biography, photo=filename, date_joined=date)
                    
                    db.session.add(nuser)
                    db.session.commit()

                    flash('User successfully registered.', 'success')

                    user = Users.query.filter_by(username=username).first()

                    userdata = [{
                        'id': user.id,'username': username,'name': name,'photo': filename,'email': email,'location': location,'biography': biography,'date_joined': date}]
                    return jsonify(data=userdata)
                else:
                    error.append("Email is already taken")
            else:
                error.append('Username is already taken')
        er=formerrors(form).append(error)
        return jsonify(errors= er)

@app.route('/api/auth/login', methods=['POST'])
def login():

    form=LoginForm()
    error=[]

    if request.method == 'POST':
        if form.validate_on_submit():

            username = form.username.data
            password = form.password.data
            
            user = Users.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                payload = {'id': user.id,'username': user.username,'iat': datetime.datetime.now(datetime.timezone.utc),'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=45)}

                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

                return jsonify(data={'message': 'Login was successful!', 'token': token, 'id': user.id})
            else:
                error.append('Username or Password is incorrect!')
        er=formerrors(form).append(error)
        return jsonify(errors= er)




@app.route('/api/auth/logout', methods=['POST'])
@requires_auth 
def logout():
    return jsonify(data={'message': 'Logout was successful!'})

"""




"""

@app.route('/api/search', methods=['GET'])
# @requires_auth
def searchCar():
    results = []
    
    if request.method =='GET':
        
        make = request.args.get('searchbymake')
        model = request.args.get('searchbymodel')

        
        # To be changed to the actual db name
        car = car.query.all()        
        results = db.session.execute('select * from car where car.model like :model or car.make like :make' , {'model': model, 'make': make}).all()
        
        if results == []:
                flash('Car model not found', 'danger')
        results.sort()

        for r in results:
            foundCar = ()
            foundCar['id'] = r.id
            foundCar['user_id']=r.user_id
            foundCar['year'] = r.year
            foundCar['price'] = r.price
            foundCar['photo'] = r.photo
            foundCar['make'] = r.make
            foundCar['model'] = r.model
            results.append(foundCar)

        return jsonify(searchCars = results)


        


 



# Under review for after db edits
@app.route('/api/users/{user_id}',methods=['GET'])
# @requires_auth
def userDetail(user_id):
    if request.method == 'GET':
        user = Users.query.all()
        results = db.session.execute('select * from car where user.user_id like :userid' , {'userid': user_id}).all()
        
        userDetails = ()
        userDetails['id'] = user.id
        userDetails['username'] = user.username
        userDetails['name'] = user.name
        userDetails['email'] = user.email
        userDetails['location'] = user.location
        userDetails['biography'] = user.biography
        userDetails['photo'] = user.photo

        return jsonify(userDetails = userDetails)
    
        
@app.route('/api/users/{userid}/favourite', methods=["POST"])
def addFavorite(userid):
    if request.is_json:
        data = request.get_json(force=True)
        faveCar = Cars(userid, data["id"], data["description"], data["make"], data["model"],
                    data["colour"], data["year"], data["transmission"], data["car_type"], data["price"], data["photo"])
                                
        db.session.add(faveCar)
        db.session.commit()

        result = {"error": "null",
                  "data": {
                      "car":{
                          "id": faveCar.id,
                          "description": faveCar.description,
                          "make": faveCar.make,
                          "model": faveCar.model,
                          "colour": faveCar.colour,
                          "year": faveCar.year,
                          "transmission": faveCar.transmission,
                          "car_type": faveCar.car_type,
                          "price": faveCar.price,
                          "photo": faveCar.photo,

                      }
                  }, 
                  "message":"Success"}
        flash('Favorite car added successfully', 'success')
        print ("Success")
    else:
        result = {"error": "true", "data": {}, "message": "Unable add car"}
        print ("failed")
    print ("returning")
    return jsonify(result)
    
@app.route('/api/users/<userid>/favourites', methods=["GET"])
# @login_required
def userFavourite(userid):
    """Returns JSON data for a user's wishlist"""

    favorite = {"error": "null","data": {"cars":[]},"message":"Success"}

    temp = Cars.query.filter_by(owner_id=userid).all()

    for f in temp:
        favorite["data"]["cars"].append({ "id": f.id,
                          "description": f.description,
                          "make": f.make,
                          "model": f.model,
                          "colour": f.colour,
                          "year": f.year,
                          "transmission": f.transmission,
                          "car_type": f.car_type,
                          "price": f.price,
                          "photo": f.photo,
                          })
    
    return jsonify(favorite)    

@app.route('/api/cars', methods=['GET'])
# @requires_auth
def Cars():

    
    if request.method =='GET':

        # To be changed to the actual db name
        car = car.query.all()        

        

        return jsonify(car = car)

###
# The functions below should be applicable to all Flask apps.
###
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".

    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')




@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

def formerrors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
