import base64
import os
import uuid
from datetime import date

from PIL import Image
import numpy as np

from classifier import train_model, train, load_model
from util import green_prop, blur_detection
from flask import Flask, request, session
import uuid
from webpage import webpage_blueprint
from auth import auth_blueprint
from api import api_blueprint
import dataaccess.ImageCRUD as ImageDao
import dataaccess.DataCon as DataCon

conn = DataCon.get_connection()

app = Flask(__name__, static_folder='static')
app.secret_key = 'secret'

app.register_blueprint(webpage_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':

    load_model()

    app.run(host="0.0.0.0", port=8080, debug=True) #changed the port, 8080 is needed for Cloud Run
