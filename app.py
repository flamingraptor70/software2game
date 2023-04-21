import json
import os

import mysql.connector
from flask import Flask, request
from flask_cors import CORS
from peli import Peli

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "content-type"

peli = Peli("Atte")

peli.ArvoPaikat()
peli.luoSotilaatLentokentille()
'''peli.Matkat()'''
peli.Kauppa()