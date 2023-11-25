from flask import render_template, request

from ..database.database import collection
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
    print_all_documents()
    return render_template('success.html', month=month, usg_apt=usg_apt, fg_apt=fg_apt, carrier=carrier, type=type, scheduled=scheduled)