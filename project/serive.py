from flask import Flask
from flask_cors import CORS
from flask import request
from config import config
from flask import request
from DataProcessor import DataProcessor
from PCAWrapper import PCAWrapper


class Service(config):
	def __init__(self):
		app = Flask(__name__)
		CORS(app)

		@app.route("/test")
		def test():
		  return "test!"


		@app.route("/hello")
		def hello():
		  return "Hello, cross-origin-world!"

		@app.route("/models")
		def models():
		  return 'LinearRegression\tLasso'

		@app.route("/graphs")
		def graphs():
			models = request.args.get('models')
			testSize = request.args.get('testSize')
			dp = DataProcessor()
			r = dp.regression_results(models,testSize)
			return r

		@app.route("/pca")
		def pca():
			comp_no = int(request.args.get('comp_no'))
			p = PCAWrapper()
			return p.pca_results(comp_no)

		app.run()


service = Service()	