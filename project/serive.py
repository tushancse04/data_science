from flask import Flask
from flask_cors import CORS


class Service:
	def __init__(self):
		app = Flask(__name__)
		CORS(app)

		@app.route("/test")
		def test():
		  return "test!"


		@app.route("/hello")
		def hello():
		  return "Hello, cross-origin-world!"

		app.run()


service = Service()	