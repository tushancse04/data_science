from config import config
class FieldProcessor(config):
	def __init__(self):
		config.__init__(self)
		ifile = open(self.data_doc_file,encoding="utf8", errors='ignore')
		ftypes = ['Discrete','Nominal','Ordinal','Continuous']
		field_type_map = {}
		for l in ifile:
			for t in ftypes:
				te = '(' + t + ')'
				if te in l:
					l = l.split(te)[0].strip()
					field_type_map[l] = t
		self.field_type_map = field_type_map
		self.year_fields = ['Garage Yr Blt','Yr Sold','Year Built','Year Remod/Add']

	def set_fields(self,df):
		fields = []
		ftm = self.field_type_map
		for f in ftm:
			if f  not in df.columns:
				continue
			if f == 'PID':
				continue
			if f == self.y_field:
				continue
			if f == 'Order':
				continue

			new_fields = []
			if ftm[f] in ['Ordinal','Nominal']:
				vals = df[f].unique()
				for i in range(len(vals)):
					new_fields += [f+'_'+str(i)]
			else:
				new_fields += [f]
			fields.append(new_fields)
		self.fields = fields

	def pop_fields(self,combination):
		combination.sort()
		for i in range(len(combination)-1,-1,-1):
			self.fields.pop(i)

	def get_fields(self,combination):
		flds = []

		for x in combination:
			flds += self.fields[x]
		return flds

