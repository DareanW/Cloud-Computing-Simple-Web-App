"""
Routes and views for the flask application.
"""

#from pprint import pprint
from datetime import datetime
import time
from flask import render_template, request
from Web_App_Python import app
import Web_App_Python
from Web_App_Python.actions.submit import handle_submit
from Web_App_Python.DatabaseConnection.database import databaseClient
from pymongo import MongoClient, database
        
# Connect to MongoDB
client = databaseClient
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

@app.route('/update')
def update():
    """Renders the update page."""
    return render_template(
        'update.html',
        title='Update',
        year=datetime.now().year,
        message='Update the Specified Airline records stored in the Mongo Database.'
    )

@app.route('/delete')
def delete():
    """Renders the delete page."""
    return render_template(
        'delete.html',
        title='Delete',
        year=datetime.now().year,
        message='Delete the Specified Airline records stored in the Mongo Database.'
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
    from .DatabaseConnection.database import collection
    cursor = collection.find(query)
    
    # Convert cursor to list
    results = [result for result in cursor]
    
    # Print results
    #for result in results:
        #pprint(result)
        
    # Render results page
    return render_template('Results.html', title='Query Results', message='Here are your results:', results=results)

@app.route('/delete', methods=['POST'])
def deleteRecord():
    # Get query parameters
    month = request.form.get('Month')
    month_operator = request.form.get('Month_operator')
    usg_apt = request.form.get('usg_apt')
    fg_apt = request.form.get('fg_apt')
    carrier = request.form.get('carrier')
    type = request.form.get('type')
    scheduled = request.form.get('Scheduled')
    scheduled_operator = request.form.get('Scheduled_operator')

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

    # Execute delete operation
    from .DatabaseConnection.database import collection

    # First save records.
    cursor = collection.find(query)
    
    # Convert cursor to list
    results = [result for result in cursor]

    # Save a copy of the records to be deleted
    saved_records = [record.copy() for record in results]

    result = collection.delete_many(query)

    # Check if the deletion was successful
    if result.deleted_count > 0:
        return render_template('success.html', title='Delete Results', message='The records were successfully deleted.', records=saved_records)
    else:
        return render_template('failure.html', title='Delete Results', message='No records matched the given filters.')

@app.route('/update', methods=['POST'])
def updateRecord():
    # Get query parameters for the old record
    month = request.form.get('Month')
    month_operator = request.form.get('Month_operator')
    usg_apt = request.form.get('usg_apt')
    fg_apt = request.form.get('fg_apt')
    carrier = request.form.get('carrier')
    type = request.form.get('type')
    scheduled = request.form.get('Scheduled')
    scheduled_operator = request.form.get('Scheduled_operator')

    # Get new values
    new_month = request.form.get('new_Month')
    new_usg_apt = request.form.get('new_usg_apt')
    new_fg_apt = request.form.get('new_fg_apt')
    new_carrier = request.form.get('new_carrier')
    new_type = request.form.get('new_type')
    new_scheduled = request.form.get('new_Scheduled')

    # Build query for the old record
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

    # Build update operation
    update_operation = {}
    if new_month:
        update_operation['Month'] = int(float(new_month))
    if new_usg_apt:
        update_operation['usg_apt'] = new_usg_apt
    if new_fg_apt:
        update_operation['fg_apt'] = new_fg_apt
    if new_carrier:
        update_operation['carrier'] = new_carrier
    if new_type:
        update_operation['type'] = new_type
    if new_scheduled:
        update_operation['Scheduled'] = int(float(new_scheduled))

    # Execute update operation
    from .DatabaseConnection.database import collection

    # First save the _id and original values of each record to be updated
    cursor = collection.find(query)
    old_records = [record.copy() for record in cursor]
    ids_to_update = [record['_id'] for record in old_records]

    result = collection.update_many(query, {'$set': update_operation})

    # Check if the update was successful
    if result.modified_count > 0:
        # Query the database again to get the updated records
        updated_records_cursor = collection.find({'_id': {'$in': ids_to_update}})
        updated_records = [record.copy() for record in updated_records_cursor]

        # Create a list of dictionaries containing the old and new values
        records = [{'old': old, 'new': new} for old, new in zip(old_records, updated_records)]

        return render_template('update_success.html', title='Update Results', message='The records were successfully updated.', records=records)
    else:
        return render_template('failure.html', title='Update Results', message='No records matched the given filters.')