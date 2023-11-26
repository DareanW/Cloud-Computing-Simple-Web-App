"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import Web_App_Python.views
from Web_App_Python.DatabaseConnection.database import databaseClient
