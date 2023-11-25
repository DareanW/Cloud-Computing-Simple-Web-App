"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from Web_App_Python import app
from Web_App_Python.actions.submit import handle_submit

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/create')
def create():
    """Renders the create page."""
    return render_template(
        'create.html',
        title='Create',
        year=datetime.now().year,
        message='Create an Airline record.'
    )

@app.route('/submit', methods=['POST'])
def submit():
    return handle_submit()
