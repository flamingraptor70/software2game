import json
import os

import mysql.connector
from flask import Flask, request
from flask_cors import CORS
from peli import Peli

peli = Peli("Atte")

peli.ArvoPaikat()
peli.luoSotilaatLentokentille()
'''peli.Matkat()'''
peli.Kauppa()