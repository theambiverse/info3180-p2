"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, send_from_directory, flash
from app.propertyform import Propertyform
from werkzeug.utils import secure_filename
from app.models import Properties
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/property', methods=['POST', 'GET'])
def property():
    form=Propertyform()
    
    if request.method == 'POST': 
        if form.validate_on_submit:
            photo=form.photo.data
            filename=secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            datab=Properties()

            datab.title=form.title.data
            datab.desc=form.desc.data
            datab.bedroom=form.bedroom.data
            datab.bathroom=form.bathroom.data
            datab.price=form.price.data
            datab.location=form.location.data
            datab.propertytype=form.select.data
            datab.photoname=filename
           
            db.session.add(datab)
            db.session.commit()
        
            flash('Property Added', 'success')
            return redirect(url_for('properties'))

    return render_template('propertyform.html', form=form)

def getprop():
    prop=Properties.query.all()
    results=[{
        "photo":p.photoname,
        "title":p.title,
        "location":p.location,
        "price":p.price,
        "id":p.id,
        "bedroom":p.bedroom,
        "bathroom":p.bathroom,
        "propertytype":p.propertytype,
        "desc":p.desc
        
        
    } for p in prop]
    return results

#def connect_db():
#    return psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/properties')
def properties():
    prop=getprop()

    
    return render_template('properties.html',prop=prop )


@app.route('/properties/<ph>')
def get_image(ph):

    root_dir=os.getcwd()

    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), ph)


def get_uploaded_images():
    rootdir=os.getcwd()
    path=rootdir+ '/uploads' 
    file_list = [] 

    for subdir, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(('.png','.PNG', '.jpg','.JPG', '.jpeg','JPEG')):
                file_list.append(name)

    return file_list


@app.route('/property/<propertyid>')
def viewproperty(propertyid):
    prop=getprop()
    l=[prop,propertyid]
    return render_template('property.html', prop=l)




###
# The functions below should be applicable to all Flask apps.
###

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
