from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello world'

#Skill drill 9.4.3
@app.route('/')
def welcome_home():
	return 'Welcome Home'
