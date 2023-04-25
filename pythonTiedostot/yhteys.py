import mysql.connector

yhteys = mysql.connector.connect(
    user="attetor",
    password="1234",
    host="mysql.metropolia.fi",
    port=3306,
    database="attetor",
    autocommit=True
)