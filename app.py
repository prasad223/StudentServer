#!/usr/bin/env python
from flask import Flask, jsonify, abort, make_response, request
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import json

userCollection = None
app = Flask(__name__)
bcrypt = Bcrypt(app)

def setUpDBCollections():
   global userCollection
   client = MongoClient()
   db = client['StudentData']
   userCollection = db['Users']

   

@app.route('/')
def index():
   return make_response(jsonify({ "greeting" :"Welcome! This is just a greeting"}),201)

def checkUserExists(user):
   resp = False
   storedUser = userCollection.find_one({"email" : user["email"]})
   if storedUser:
      if storedUser.get("email") and storedUser.get("password_hash"):
	if bcrypt.check_password_hash(storedUser['password_hash'],user["password"]):
	    resp = True
   return resp

@app.route('/signin', methods=['POST'])
def signIn():
   userInfo = request.json
   if not userInfo or not 'email' in userInfo or not 'password' in userInfo:
     abort(400)
   message = "Invalid User"
   if checkUserExists(userInfo):
        message = "Success"
   return make_response(jsonify({ 'Message': message}),201)

def addUser(user):
    if not user or not user.get("email") or not user.get("password"):
       return 400
    if not userCollection:
       setUpDBCollections()
    if userCollection.find_one({"email" : user["email"]}):
       return 304
    userInfo = {}
    userInfo["email"] = user["email"]
    userInfo["password_hash"] = bcrypt.generate_password_hash(user["password"])
    userInfo["user_type"] = user["type"]
    insertId = userCollection.insert_one(userInfo).inserted_id
    if insertId:
       return 201
    return 400
    
@app.route('/signup', methods=['POST'])
def singUp():
   userInfo = request.json
   message = "User creation failure"
   http_code = addUser(userInfo)
   if http_code == 400:
      abort(400)
   elif http_code == 304:
      message = "User exists"
   elif http_code == 201:
      message = "User created successfully"
   return make_response(jsonify({"message" : message}),http_code)

@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'message' : 'Bad Request'}),400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def main():
   setUpDBCollections()
   app.run(debug=True)


if __name__ == "__main__":
   main()

