from config import config
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.linear_model import Lasso,LassoLars,BayesianRidge
import json
import importlib
from sklearn.cross_decomposition import PLSRegression



class Regression(config):
	def __init__(self):
		config.__init__(self)

	def get_data(self,df,fields,models,testSize):
		testSize = float(testSize)
		X = df[fields]
		y = df[self.y_field]
		l = df.shape[0]
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize/l, shuffle=True)
		models = models.split(',')
		results = {}
		for m in models:
			m = m.strip()
			model = getattr(importlib.import_module("sklearn.linear_model"), m)()
			model.fit(X_train,y_train)
			p = model.predict(X_test.values)
			results[m] = p
			model.score(X_test,y_test)

		r = []
		for i in range(len(y_test.values)):
			p = 'Point ' + str(i+1)
			values = []
			values.append({'model':'Orig','value':float(y_test.values[i])})
			for j,m in enumerate(models):
				m = m.strip()
				values.append({'model':m,'value':results[m][i]})
			r.append({'categorie':p,'values':values})

		return json.dumps(r)

	def run(self,df,fields):
		X = df[fields]
		y = df[self.y_field]
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
		model = Lasso()
		model.fit(X_train,y_train)
		p = model.predict(X_test.values)
		l = df.shape[0]
		print(l)
		return model.score(X_test,y_test)

