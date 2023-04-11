import flask
from flask import jsonify, request
from flask_cors import CORS
import pymysql

app = flask.Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["DEBUG"] = True
CORS(app, resources={r"./*":{"origins":["http://127.0.0.1:5500","*"]}})

db = pymysql.connect(
   host = 'localhost',
   port = 3306,
   user = 'root',
   password = '',
   database = 'school',
   charset = 'utf8mb4'
)

cursor = db.cursor()


menuData = {
           '1號餐': { 'name': '大麥克', 'price': 72, 'mealType':'main' },
           '2號餐': { 'name': '雙層牛肉吉事堡', 'price': 62, 'mealType':'main' },
           '3號餐': { 'name': '嫩煎雞腿堡', 'price': 82, 'mealType':'main' },
           'A': { 'name': '中薯+飲料', 'price': 55, 'mealType':'side' },
           'B': { 'name': '冰旋風+飲料', 'price': 85, 'mealType':'side' },
           'C': { 'name': '麥克雞塊+薯條+飲料', 'price': 100, 'mealType':'side' }
       }
@app.route('/',methods=['GET'])
def home():
   return "<h1>Welecome to my flask server.</h1>"

@app.route('/menu',methods=['GET'])
def menu():
   return jsonify(menuData)

@app.route('/db/students',methods=['GET', 'POST'])
def students():
   res = {"success":False, "info":"查詢失敗"}
   try:
      if request.method == 'GET':
         sql = 'SELECT * FROM `students` WHERE `s_nickname` LIKE "小%"'
         cursor.execute(sql)

         if cursor.rowcount > 0:
            # results = cursor.fetchall()

            columns = cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

            res['success'] = True
            res['info'] = '查詢成功'
            res['results'] = results
            res['des'] = cursor.description
            res['length'] = cursor.rowcount
         else:
            res['info'] = '查無資料'

         db.commit()

      elif request.method == 'POST':
         res['info'] = '登入失敗'

         # res['username'] = request.json['username']
         # res['password'] = request.json['password']

         sql = "SELECT * FROM `students` WHERE `s_name`='{}' AND `s_nickname` = '{}'".format(request.json['username'], request.json['password'])
         cursor.execute(sql)

         if cursor.rowcount > 0:
            # results = cursor.fetchall()
            columns = cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

            res['success'] = True
            res['info'] = '登入成功'
            res['results'] = results
         else:
            res['info'] = '查無資料'

         db.commit()

   except Exception as e:
      db.rollback()
      res['info'] = f'SQL 執行失敗: {e}'

   return jsonify(res)


@app.route('/db/students/<int:id>', methods=['GET'])
def student(id):
   res = {"success":False, "info":"查詢失敗"}
   
   try:
      if request.method == 'GET':
         sql = 'SELECT * FROM `students` WHERE `s_id` ={} '.format(id)
         cursor.execute(sql)

         if cursor.rowcount > 0:
            # results = cursor.fetchall()

            columns = cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

            res['success'] = True
            res['info'] = '查詢成功'
            res['results'] = results
            # res['des'] = cursor.description
            res['length'] = cursor.rowcount
         else:
            res['info'] = '查無資料'

         db.commit()

   except Exception as e:
      db.rollback()
      res['info'] = f'SQL 執行失敗: {e}'

   return jsonify(res)


app.run()

