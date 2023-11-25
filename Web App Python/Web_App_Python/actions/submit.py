from flask import render_template, request

from Web_App_Python.DatabaseConnection.database import collection
from pprint import pprint

def print_all_documents():
    documents = collection.find()
    for document in documents:
        pprint(document)

def handle_submit():
    # Get the values from the form
    month = int(float(request.form.get('Month')))
    usg_apt = request.form.get('usg_apt')
    fg_apt = request.form.get('fg_apt')
    carrier = request.form.get('carrier')
    type = request.form.get('type')
    scheduled = int(float(request.form.get('Scheduled')))

    # Create a new record
    new_record = {
        'Month': month,
        'usg_apt': usg_apt,
        'fg_apt': fg_apt,
        'carrier': carrier,
        'type': type,
        'Scheduled': scheduled
    }

    # Insert the new record into the database
    try:
        collection.insert_one(new_record)
        return render_template('success.html', records=[new_record])
    except:
        return render_template('failure.html')
