import pandas
from config import config
from FieldProcessor import FieldProcessor
import numpy as np
from pandas import ExcelWriter
import os
from comb import comb
from Regression import Regression
import math
import numpy

class DataProcessor(config):
	def __init__(self):
		config.__init__(self)
		self.fp = FieldProcessor()

		df = None
		if os.path.exists(self.new_data_file):
			df = pandas.read_csv(self.new_data_file)
		else:
			df = pandas.read_excel(self.data_file)
			self.update_year_values(df)
			self.replace_column_by_binary_columns(df)
		self.df = df
		self.fp.set_fields(self.df)
		return
		#self.update_nan_values()
		#self.df.to_csv(self.new_data_file, sep=',')
		max_score = 0
		opt_flds = []
		opt_c = []
		while True:
			score,c,flds = self.get_opt_fields(opt_flds,opt_c)
			if score > max_score:
				self.fp.pop_fields(c)
				opt_flds = flds
				opt_c += c
				max_score = score
			else:
				break
			print(max_score,c)

		print(opt_c,max_score)


	def regression_results(self,models,testSize):
		model = Regression()
		c = [i for i in range(len(self.fp.fields))]
		fields = self.fp.get_fields(c)
		return model.get_data(self.df,fields,models,testSize)

	def run_for_all_fields(self):
		model = Regression()
		c = [i for i in range(len(self.fp.fields))]
		fields = self.fp.get_fields(c)
		score = model.get_data(self.df,fields,'Lasso',10)
	


	def get_opt_fields(self,prev_opt_flds,prev_opt_c):
		c = comb()
		combinations = c.get_combinations(len(self.fp.fields),2,2)
		model = Regression()
		opt_fields = None
		opt_c = None
		max_score = 0
		for i,c in enumerate(combinations):
			fields = self.fp.get_fields(c) + prev_opt_flds
			score = model.run(self.df,fields)
			if score > max_score:
				max_score = score
				opt_fields = fields
				opt_c = c
		return max_score,opt_c,opt_fields

	def replace_column_by_binary_columns(self,df):
		ftm = self.fp.field_type_map

		for f in ftm:
			if f  not in df.columns:
				continue
			if f == 'PID':
				continue
			if ftm[f] in ['Ordinal','Nominal']:
				vals = df[f].unique()
				for i,row in df.iterrows():
					for j in range(len(vals)):
						df.loc[i,f+'_'+str(j)] = (1 if row[f] == vals[j] else 0)


		df.to_csv(self.new_data_file, sep=',')

	def update_year_values(self,df):
		for yf in self.fp.year_fields:
			mn,mx = min(df[yf]) - 1,max(df[yf])
			df[yf] = df[yf] - mn
		for yf in self.fp.year_fields:
			for i,row in df.iterrows():
				if pandas.isnull(row[yf]):
					df.loc[i,yf] = 0


	def update_nan_values(self):
		for f in self.fp.fields:
			if len(f) > 1:
				continue
			f = f[0]
			for i,row in self.df.iterrows():
				if pandas.isnull(row[f]):
					self.df.loc[i,f] = 0

