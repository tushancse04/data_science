from sklearn import linear_model
from config import config

class Regression(config):
	def __init__(self):
		config.__init__(self)

	def run(self,df,fields):
		X = df[fields]
		y = df[self.y_field]
		model = linear_model.LinearRegression()
		model.fit(X,y)
		return model.score(X,y)