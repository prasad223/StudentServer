#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import json

app = Flask(__name__)

@app.route('/')
def index():
   return make_response(jsonify({ "greeting" :"Welcome! This is just a greeting"}),201)

@app.route('/signin', methods=['POST'])
def signIn():
   print request
   if not request.json or not 'username' in request.json or not 'password' in request.json:
     abort(400)
   print request.json, type(request.json)
   userInfo = request.json
   message = "Invalid User"
   if userInfo['username'] == "abc" and userInfo['password'] == "xyz":
      message = "Success"
   return make_response(jsonify({ 'Message': message}),201)

@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error' : 'Bad Request'}),400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
   app.run(debug=True)

