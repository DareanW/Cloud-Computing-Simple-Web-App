"""
Routes and views for the flask application.
"""

from pprint import pprint
from datetime import datetime
from flask import render_template, request
from Web_App_Python import app
from Web_App_Python.actions.submit import handle_submit
from pymongo import MongoClient
        
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Group_18_Database']

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

@app.route('/read')
def read():
    """Renders the read page."""
    return render_template(
        'read.html',
        title='Read',
        year=datetime.now().year,
        message='Read the Airline records stored in the Mongo Database.'
    )

@app.route('/submit', methods=['POST'])
def submit():
    return handle_submit()

@app.route('/query', methods=['GET'])
def query():
    # Get query parameters
    month = request.args.get('Month')
    month_operator = request.args.get('Month_operator')
    usg_apt = request.args.get('usg_apt')
    fg_apt = request.args.get('fg_apt')
    carrier = request.args.get('carrier')
    type = request.args.get('type')
    scheduled = request.args.get('Scheduled')
    scheduled_operator = request.args.get('Scheduled_operator')

    # Build query
    filters = []
    if month:
        if month_operator == 'le':
            filters.append({'Month': {'$lte': int(float(month))}})
        elif month_operator == 'ge':
            filters.append({'Month': {'$gte': int(float(month))}})
        else:  # Default to 'eq'
            filters.append({'Month': int(float(month))})
    if usg_apt:
        filters.append({'usg_apt': usg_apt})
    if fg_apt:
        filters.append({'fg_apt': fg_apt})
    if carrier:
        filters.append({'carrier': carrier})
    if type:
        filters.append({'type': type})
    if scheduled:
        if scheduled_operator == 'le':
            filters.append({'Scheduled': {'$lte': int(float(scheduled))}})
        elif scheduled_operator == 'ge':
            filters.append({'Scheduled': {'$gte': int(float(scheduled))}})
        else:  # Default to 'eq'
            filters.append({'Scheduled': int(float(scheduled))})

    # Combine filters using AND logic
    query = {}
    if filters:
        query['$and'] = filters

    # Execute query
    from .database.database import collection
    cursor = collection.find(query)
    
    # Convert cursor to list
    results = [result for result in cursor]
    
    # Print results
    for result in results:
        pprint(result)
        
    # Render results page
    return render_template('Results.html', title='Query Results', message='Here are your results:', results=results)
