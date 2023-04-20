import json
import os

import mysql.connector
from flask import Flask, request
from flask_cors import CORS
from peli import Peli

peli = Peli()

peli.LuoPeli("Atte", 1000, 1000, 1000, 0)
peli.ArvoPaikat()
peli.ValitseAloitus()