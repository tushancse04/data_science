from config import config
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.linear_model import Lasso,LassoLars,BayesianRidge
import json
import importlib
from sklearn.cross_decomposition import PLSRegression
import time
from sklearn import metrics
from sklearn.decomposition import PCA
import pandas as pd



class Regression(config):
	def __init__(self):
		config.__init__(self)

	def pca_results(self,i,X,y,test_size):
		s = time.time()
		pca = PCA(n_components=i)
		x = pca.fit_transform(X)
		X_train, X_test, y_train, y_test = train_test_split(pd.DataFrame(x), y,test_size=test_size, shuffle=False)
		model = LinearRegression()
		model.fit(X_train,y_train)
		p = model.predict(X_test)
		score = model.score(X_test,y_test)
		return p,score,time.time()-s

	def get_data(self,df,fields,models,testSize):
		xm = 'PCA'
		testSize = float(testSize)
		X = df[fields]
		print(len(X.columns.values))
		y = df[self.y_field]
		l = df.shape[0]
		test_size = testSize/l
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=True)
		X = pd.concat([X_train,X_test])
		y = pd.concat([y_train,y_test])

		pca_p,pca_score,pca_time = self.pca_results(30,X,y,test_size)
		models = models.split(',')
		results = {}
		times = {}
		scores = {}
		err = {}
		for m in models:
			if m == xm:
				continue
			s = time.time()
			m = m.strip()
			model = getattr(importlib.import_module("sklearn.linear_model"), m)()
			model.fit(X_train,y_train)
			p = model.predict(X_test.values)
			results[m] = p
			scores[m] =  model.score(X_test,y_test)
			times[m] = time.time() - s
			err[m] = metrics.mean_squared_error(y_test,p)

		if xm in models:
			times[xm] = pca_time 
			scores[xm] = pca_score
			err[xm] = metrics.mean_squared_error(y_test,pca_p)
			results[xm] = pca_p



		rv = []
		rm = []
		m = 0
		for x in err:
			if err[x] > m:
				m = err[x]
		for x in err:
			err[x] = err[x]/m


		m = 0
		for x in times:
			if times[x] > m:
				m = times[x]

		for x in times:
			times[x] = times[x]/m

		for i in range(len(y_test.values)):
			p = 'Point ' + str(i+1)
			values = []
			values.append({'model':'Orig','value':float(y_test.values[i])})
			for j,m in enumerate(models):
				m = m.strip()
				values.append({'model':m,'value':results[m][i]})
			rv.append({'categorie':p,'values':values})

		values_t = []
		values_s = []
		values_e = []
		for m in models:
			values_t.append({'model':m,'value':times[m]})
			values_s.append({'model':m,'value':scores[m]})
			values_e.append({'model':m,'value':err[m]})
		rm.append({'categorie':'score','values':values_s})
		rm.append({'categorie':'time','values':values_t})
		rm.append({'categorie':'error','values':values_e})


		r = {}
		r['v'] = rv
		r['m'] = rm
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

