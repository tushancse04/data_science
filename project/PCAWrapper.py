from sklearn.decomposition import PCA
from config import config
from DataProcessor import DataProcessor
import numpy as np
from Regression import Regression
from sklearn.linear_model import LogisticRegression,LinearRegression
import json
from sklearn.model_selection import train_test_split
import pandas as pd
from random import shuffle

class PCAWrapper(config):
	def __init__(self):
		config.__init__(self)

	def pca_results(self,comp_no):
		dp = DataProcessor()
		c = [i for i in range(len(dp.fp.fields))]
		fields = dp.fp.get_fields(c)
		X = dp.df[fields]
		pca = PCA(n_components=comp_no)
		x = pca.fit_transform(X)
		y = dp.df[self.y_field]
		X_train, X_test, y_train, y_test = train_test_split(pd.DataFrame(x), pd.DataFrame(y),test_size=.2, shuffle=True)

		model = LinearRegression()
		model.fit(X_train,y_train)
		model.fit(X_test,y_test)
		score = model.score(X_test,y_test)
		d = []
		d.append({'component':str(comp_no),'score':score})
		d = json.dumps(d)
		return d



