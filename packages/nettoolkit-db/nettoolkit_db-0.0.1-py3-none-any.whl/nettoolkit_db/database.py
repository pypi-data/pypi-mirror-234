"""
database operations

class, method,  function  defining the excel database write/read operations.

index:
	* read_xl = to read file
	* append_to_xl = to append to an existing file.
	* write_to_xl = to create a new file and write.
"""
# ------------------------------------------------------------------------------
from collections import OrderedDict
import os
import pandas as pd
# ------------------------------------------------------------------------------


def read_xl(file):
	"""reads Excel file and return object XL_READ

	Args:
		file (str): input excel filename

	Returns:
		XL_READ: XL_READ object (pandas DataFrame parent)
	"""    	
	xlrd = XL_READ(file)
	xlrd.read_sheets()
	return xlrd


def get_merged_DataFrame_of_file(file):
	"""returns merged DataFrame after clubbing all tabs of file

	Args:
		file (str): Excel file name

	Returns:
		pandas DataFrame: merged database
	"""	
	xlr = read_xl(file)
	df = pd.DataFrame()
	for k, v in xlr:
		v = v.fillna("")
		df = pd.concat([v,df])
	return df

def append_to_xl(file, df_dict, overwrite=True, index_label=""):
	"""appends dictionary of dataframes to an Excel file
	overwrite: will append data to existing file, else create a copy and 
	adds data to it

	Args:
		file (str): input excel filename
		df_dict (dict): dictionary of key:DataFrame format
		overwrite (bool, optional): overwrite or append. Defaults to True.
		index_label (str, optional): index label for each tab
	"""    	
	try:
		xlrd = read_xl(file)
		prev_dict = xlrd.df_dict
	except:
		prev_dict = {}
	prev_dict.update(df_dict)
	if overwrite:
		try:
			os.remove(file)
		except: pass
	write_to_xl(file, prev_dict, overwrite=overwrite, index_label=index_label)

def write_to_xl(file, df_dict, index=False, overwrite=False, index_label=""):
	"""Create a new Excel file with provided dictionary of dataframes
	overwrite: removes existing file, else create a copy if file exist.	

	Args:
		file (str): input excel filename
		df_dict (dict): dictionary of key:DataFrame format
		index (bool, optional): keep index column. Defaults to False.
		overwrite (bool, optional): overwrite or create a new file. Defaults to False.
		index_label (str, optional): index label for each tab
	"""
	XL_WRITE(file, df_dict=df_dict, index=index, overwrite=overwrite, index_label=index_label)
# ------------------------------------------------------------------------------

class XL_READ:
	"""reads an existing Excel file provide absolute path along with filename as xl
	provide sheet_name in order to read only a particular sheet only. otherwise
	all sheets will be read and stored under `df_dict` attribute.

	Returns:
		self: XL_READ object

	Yields:
		sheet, DataFrame: sheet by sheet data
	"""    	

	def __init__(self, xl, sheet_name=None):
		"""Create object by providing Excel file name, if sheet_name is provided only
		particular sheet will be read else all.

		Args:
			xl (str): excel file name
			sheet_name (str, optional): sheet name to be read. Defaults to None.
		"""    		
		self.df_dict = OrderedDict()
		self.sheet_name = sheet_name
		self.xl = pd.ExcelFile(xl)
		self.sheet_names = self.xl.sheet_names

	def __len__(self): return len(self.df_dict)
	def __iter__(self):
		for sheet, dataframe in self.df_dict.items(): yield (sheet, dataframe)		
	def __getitem__(self, key): return self.df_dict[key]
	def __setitem__(self, key, value): self.df_dict[key] = value

	def read_sheets(self):
		"""method to start reading the sheet(s) and putting them in self database
		"""    		
		if self.sheet_name:
			self[self.sheet_name] = self.xl.parse(sheet_name)
		else:
			for sheet_name in self.sheet_names:
				self[sheet_name] = self.xl.parse(sheet_name)

# ------------------------------------------------------------------------------
class XL_WRITE():
	"""write to an Excel file

	Returns:
		self: XL_WRITE object
	"""
	def __init__(self, name, df_dict, index=False, overwrite=False, index_label=""):
		"""initialize an object by providing name of excel and dictionary of dataframes 

		Args:
			name (str): file name with absolute path and extension
			df_dict (dict): dictionary of dataframes
			index (bool, optional): write index column or not. Defaults to False.
			overwrite (bool, optional): overwrite the file (if exist) or not. Defaults to False.
		"""    		
		self.write(name, df_dict, index, index_label, overwrite)

	def write(self, name, df_dict, index, index_label, overwrite):
		"""method to start write to file.  by default it will run while initialize of object

		Args:
			name (str): file name with absolute path and extension
			df_dict (dict): dictionary of dataframes
			index (bool, optional): write index column or not. Defaults to False.
			index_label (str, optional): index label
			overwrite (bool, optional): overwrite the file (if exist) or not. Defaults to False.
		"""    		
		fileName = name if overwrite else self.get_valid_file_name(name)
		with pd.ExcelWriter(fileName) as writer_file:
			for sht_name, df in df_dict.items():
				try:
					df.to_excel(writer_file, sheet_name=sht_name, index=index, index_label=index_label)
				except:
					try:
						print(f"writing data for {fileName} sheet {sht_name} ...failed!!!, length of sheet name = {len(sht_name)}")
						df.to_excel(writer_file, sheet_name=sht_name[:31], index=index, index_label=index_label)
						print(f"instead data for {fileName} sheet {sht_name[:31]} - trunked ...done!")
					except:
						print(f"writing data for {fileName} sheet {sht_name[:31]} - trunked ...failed!!!")

	def copy_of_file(self, file, n):
		"""return a valid next available file name.

		Args:
			file (str): name of file
			n (int): name suffix

		Returns:
			str: available filename to make a new copy of file.
		"""    		
		spl_file =  file.split(".")
		name = ".".join(spl_file[:-1])
		extn = spl_file[-1]
		next_num = f'' if n == 1 else f' ({str(n)})'
		return f'{name} - Copy{next_num}.{extn}'

	def get_valid_file_name(self, file):
		"""gets a valid next available filename and create a copy of provided file.

		Args:
			file (str): name of file

		Returns:
			str: next available file name (after coping file)
		"""    		
		n = 0
		file_name = file
		while True:
			try:
				XL_READ(file)
				n += 1
				file = self.copy_of_file(file_name, n)
			except:
				break
		return file

# ------------------------------------------------------------------------------

# __all__ = ['read_xl', 'get_merged_DataFrame_of_file', 'append_to_xl', 'write_to_xl']
# # ------------------------------------------------------------------------------
