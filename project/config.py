class config:
	def __init__(self):
		self.dataset_loc = 'dataset/'
		self.data_file = self.dataset_loc + 'AmesHousing.xls'
		self.data_doc_file = self.dataset_loc + 'DataDocumentation.txt'
		self.new_data_file = 'newdf.csv'
		self.y_field = 'SalePrice'