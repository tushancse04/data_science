from config import config
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.linear_model import Lasso

class Regression(config):
	def __init__(self):
		config.__init__(self)

	def run(self,df,fields):
		X = df[fields]
		y = df[self.y_field]
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
		model = Lasso()
		model.fit(X_train,y_train)
		p = model.predict(X_test.values)
		return model.score(X_test,y_test)

