import flask
from flask import jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["DEBUG"] = True
CORS(app, resources={r"./*":{"origins":["http://127.0.0.1:5500","*"]}})

menuData = {
           '1號餐': { 'name': '456大麥克', 'price': 72 },
           '2號餐': { 'name': '雙層牛肉吉事堡', 'price': 62 },
           '3號餐': { 'name': '嫩煎雞腿堡', 'price': 82 },
           'A': { 'name': '中薯+飲料', 'price': 55 },
           'B': { 'name': '冰旋風+飲料', 'price': 85 },
           'C': { 'name': '麥克雞塊+薯條+飲料', 'price': 100 }
       }
@app.route('/',methods=['GET'])
def home():
   return "<h1>Welecome to my flask server.</h1>"

@app.route('/menu',methods=['GET'])
def menu():
   return jsonify(menuData)

app.run()

