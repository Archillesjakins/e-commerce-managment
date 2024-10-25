from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Use PyMySQL as the driver
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Archilles@localhost:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)