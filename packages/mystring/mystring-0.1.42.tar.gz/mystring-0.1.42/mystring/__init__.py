import os,sys,re,importlib.machinery,types
class string(str):
	def equals(self,*args):
		for arg in args:
			if self == arg:
				return True
		return False

	def replace(self,x,y):
		return string(super().replace(x,y))

	def rep(self,substring):
		self = self.replace(substring,'')
		return self

	def repsies(self,*args):
		for arg in args:
			self = self.rep(arg)
		return self

	def rep_end(self, substring):
		if self.endswith(substring):
			self = string(self[:-1 * len(substring)])
		return self
	
	def repsies_end(self,*args):
		for arg in args:
			self = self.rep_end(arg)
		return self
	
	def rep_fromend(self, substring):
		#From https://stackoverflow.com/questions/3675318/how-to-replace-some-characters-from-the-end-of-a-string
		head, _sep, tail = self.rpartition(substring)
		self = string(head + tail)
		return self
	
	def repsies_fromend(self,*args):
		for arg in args:
			self = self.rep_fromend(arg)
		return self
	
	def exec(self, display=True, lines=False):
		import subprocess

		output_contents = ""
		if display:
			print(self)
		process = subprocess.Popen(self,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=1,encoding='utf-8', universal_newlines=True, close_fds=True)
		while True:
			out = process.stdout.readline()
			if out == '' and process.poll() != None:
				break
			if out != '':
				if display:
					sys.stdout.write(out)
				output_contents += out
				sys.stdout.flush()
		
		if not lines:
			return string(output_contents)
		else:
			return lyst([string(x) for x in output_contents.split('\n') if not string(x).empty])

	@property
	def isvalidpy(self):
		import ast
		output = False
		try:
			ast.parse(str(self))
			output = True
		except:
			pass
		return output

	def eval(self):
		if self.isvalidpy:
			eval(self)

	@property
	def irregularstrip(self):
		#for arg in ['.','(',')','[',']','-',',','/','"',"'","’","#",]:
		#	self = self.rep(arg)
		self = string(re.sub(r'\W+', '', self))
		return self
	
	@property
	def deplete(self):
		self = self.trim.irregularstrip.trim
		if self.empty or self.equals("None", "none", "Null", "null", "NaN", "nan"):
			self = None
		return self

	def ad(self, value):
		self = string(self + getattr(self, 'delim', "")  + value)
		return self

	def delim(self, value):
		self.delim = value

	def pre(self, value):
		self = string(value + getattr(self, 'delim', "")  + self)
		return self

	def pres(self, *args):
		for arg in args:
			self = self.pre(arg)
		return self

	def startswiths(self, *args):
		for arg in args:
			if self.startswith(arg):
				return True
		return False

	@property
	def trim(self):
		self = string(self.strip())
		if self == '':
			self = None
		return self

	@property
	def empty(self):
		if obj is None:
			return True

		return any([
			str(obj).strip().lower() == x for x in [
				'nan', 'none', 'null'
			]
		]) or self.deplete is None

	@property
	def notempty(self):
		return not self.empty

	def format(self, numstyle='06'):
		return format(int(self),numstyle)

	def splitsies(self,*args,joiner=":"):
		output_list = []
		for splitter_itr, splitter in enumerate(args):
			if splitter_itr == 0:
				output_list = self.split(splitter)
			else:
				temp_list = string(joiner.join(output_list)).splitsies(splitter,joiner=joiner)
				output_list = []
				for temp_item in temp_list:
					for temp_split_item in temp_item.split(joiner):
						output_list.append(temp_split_item)

		return [string(x) for x in output_list]

	def tohash(self, hash_type='sha512', encoding='utf-8'):
		import hashlib
		return string(getattr(hashlib, hash_type)(self.encode(encoding)).hexdigest())

	def tobase64(self, encoding='utf-8', prefix=False):
		import base64
		return "b64:" if prefix else "" +string(base64.b64encode(self.encode(encoding)).decode(encoding))

	@staticmethod
	def frombase64(strang, encoding='utf-8'):
		import base64
		return string(base64.b64decode(strang.encode(encoding)).decode(encoding))

	@staticmethod
	def of(strung):
		if strung == None:
			strung = ""

		strung = str(strung)

		if strung.startswith('b64:'):
			return string.frombase64(strung.replace('b64:','',1))

		try:
			return string.frombase64(strung)
		except:
			pass

		return string(strung)

	def matches(self, regex:str, at_most:int=-1) -> bool:
		try:
			grps = [
				match.group() for idx,match in enumerate(regex.finditer(str(self)))
			]
			return (at_most > -1 and len(grps) <= at_most) or (at_most == -1 and len(grps) > 0)
		except Exception as e:
			print("Error grabbing regex: {0}".format(e))
			return False

	@property
	def isfile(self):
		return os.path.isfile(self)

	@property
	def isdir(self):
		return os.path.isdir(self)

	@property
	def file_name(self):
		file_name, file_ext = os.path.splitext(self)
		return os.path.basename(file_name)

	@property
	def filedir_name(self):
		file_name, file_ext = os.path.splitext(self)
		return file_name

	@property
	def ext(self):
		file_name, file_ext = os.path.splitext(self)
		return file_ext

	def aspy(self):
		#https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3#answer-19011259
		loader = importlib.machinery.SourceFileLoader(self.file_name, os.path.abspath(self))
		mod = types.ModuleType(loader.name)
		loader.exec_module(mod)
		return mod

	def progLangName(self, upper:bool=False):
		for rawName, cleanName in {
			"#":"Sharp",
			"+":"Plus",
			"*":"Asterik",
			".":"Dot",
			"-":"Dash",
			"_":"underscore",
			"/":"Slash",
			"\\":"Slash",
		}.items():
			self = self.replace(rawName, cleanName.upper() if upper else cleanName)

		return string(self)

	def deepClean(self, perma:bool=False):
		self = self.trim
		valid_kar = lambda kar: (ord('0') <= ord(kar) and ord(kar) <= ord('9')) or (ord('A') <= ord(kar) and ord(kar) <= ord('z'))
		output = None
		if perma:
			output = ''.join([i for i in self if valid_kar(i)])
		else:
			output = self.replace(' ', '\ ').replace('&','\&')

		self = string(string(output).trim)
		return self
	
	def shellPrep(self,prefix="/usr/bin/env python3 -c"):
		return string.of("{prefix} \"import base64;exec(base64.b64decode('{cmd}').decode())\"".format(prefix=prefix, cmd=self.tobase64()))
	
	def noNewLine(self, replaceWith=""):
		return string(self.replace("\r\n","\n").replace("\n", replaceWith))
	
	def escapeTab(self, replaceWith=""):
		return string(self.replace("\t",replaceWith))

def ofBoolean(obj:any) -> bool:
	obj = string.of(obj)

	if obj.empty:
		return False

	return obj.trim.lower() in ["true", 1, "1", "active", "high"]

class integer(int):

	@staticmethod
	def of(obj:any, default:int = -1) -> int:
		obj = string.of(obj)

		if obj.empty:
			return integer(default)
		
		try:
			return int(obj)
		except:
			return integer(default)

class obj(object):
	#https://python-patterns.guide/gang-of-four/decorator-pattern/
	#https://stackoverflow.com/questions/1957780/how-to-override-the-operator-in-python
	def __iter__(self):
		return self.__iter__()

	def __next__(self):
		return self.__next__()

	def __getattr__(self, attr):
		if attr in self.__dict__:
			return getattr(self, attr)
		return None

	def __setattr__(self, name, value):
		setattr(self.__dict__, name, value)

	def __delattr__(self, name):
		if name in self.__dict__:
			delattr(self.__dict__, name)

	def __getitem__(self, key):
		if isinstance(key, str):
			return self.__getattr__(key)
		return super.__getitem__(key)
	
	def __setitem__(self,key,value):
		if isinstance(key, str):
			return self.__getattr__(key)
		else:
			super.__setattr__(key,value)
	
	def __delitem__(self,key):
		if isinstance(key, str):
			return self.__getattr__(key)
		else:
			super.__delitem__(key)


from dateutil.parser import parse
import datetime 
class timestamp(datetime.datetime):

	@staticmethod
	def of(obj:any):
		obj = string.of(obj)

		if obj.empty:
			return None

		try:
			return timestamp(datetime.fromisoformat(obj))
		except: pass

		try:
			return timestamp(parse(obj))
		except:
			return None

	def toIso(self):
		tz = self.astimezone()
		return string(tz.isoformat())

	@staticmethod
	def now():
		return datetime.datetime.now(datetime.timezone.utc)

try:
	import pandas as pd
	import sqlite3
	class frame(pd.DataFrame):
		def __init__(self,*args,**kwargs):
			super(frame,self).__init__(*args,**kwargs)

		def col_exists(self,column):
			return column in self.columns

		def col_no_exists(self,column):
			return not(self.col_exists(column))

		def column_decimal_to_percent(self,column):
			self[column] = round(round(
				(self[column]),2
			) * 100,0).astype(int).astype(str).replace('.0','') + "%"
			return self

		def move_column(self, column, position):
			if self.col_no_exists(column):
				return
			colz = [col for col in self.columns if col != column]
			colz.insert(position, column)
			self = frame(self[colz])
			return self

		def rename_column(self, columnfrom, columnto):
			if self.col_no_exists(columnfrom):
				return
			self.rename(columns={columnfrom: columnto},inplace=True)
			return self

		def rename_columns(self, dyct):
			for key,value in dyct.items():
				if self.col_exists(key):
					self.rename(columns={key: value},inplace=True)
			return self

		def rename_value_in_column(self, column, fromname, fromto):
			if self.col_no_exists(column):
				return
			self[column] = self[column].str.replace(fromname, fromto)
			return self

		def drop_value_in_column(self, column, value,isstring=True):
			if self.col_no_exists(column):
				return
			self = frame(self.query("{0} != {1}".format(column, 
				"'" + value + "'" if isstring else value
			)))
			return self

		def cast_column(self, column, klass):
			if self.col_no_exists(column):
				return
			self[column] = self[column].astype(klass)
			return self
	
		def search(self, string):
			return frame(self.query(string))
	
		def arr(self):
			self_arr = self.to_dict('records')
			return self_arr

		def add_confusion_matrix(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN', use_percent:bool=False):
			prep = lambda x:frame.percent(x, 100) if use_percent else x

			self['Precision_PPV'] = prep(self[TP]/(self[TP]+self[FP]))
			self['Recall'] = prep(self[TP]/(self[TP]+self[FN]))
			self['Specificity_TNR'] = prep(self[TN]/(self[TN]+self[FP]))
			self['FNR'] = prep(self[FN]/(self[FN]+self[TP]))
			self['FPR'] = prep(self[FP]/(self[FP]+self[TN]))
			self['FDR'] = prep(self[FP]/(self[FP]+self[TP]))
			self['FOR'] = prep(self[FN]/(self[FN]+self[TN]))
			self['TS'] = prep(self[TP]/(self[TP]+self[FP]+self[FN]))
			self['Accuracy'] = prep((self[TP]+self[TN])/(self[TP]+self[FP]+self[TN]+self[FN]))
			self['PPCR'] = prep((self[TP]+self[FP])/(self[TP]+self[FP]+self[TN]+self[FN]))
			self['F1'] = prep(2 * ((self['Precision_PPV'] * self['Recall'])/(self['Precision_PPV'] + self['Recall'])))

			return self
		
		def confusion_matrix_sum(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
			return (self[TP].sum() + self[TN].sum() + self[FN].sum())  

		def verify_confusion_matrix_bool(self,TotalCases:int=0,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
			return TotalCases == self.confusion_matrix_sum(TP=TP,FP=FP,TN=TN,FN=FN)

		def verify_confusion_matrix(self,TotalCases:int=0, TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
			return "Total Cases {0} sum(TP,TN,FN)".format(
				"===" if self.verify_confusion_matrix_bool(TotalCases=TotalCases,TP=TP,FP=FP,TN=TN,FN=FN) else "=/="
			) 

		@staticmethod
		def percent(x,y):
			return ("{0:.2f}").format(100 * (x / float(y)))

		@staticmethod
		def from_csv(string):
			return frame(pd.read_csv(string, low_memory=False))

		@staticmethod
		def from_json(string):
			return frame(pd.read_json(string))

		@staticmethod
		def from_arr(arr):
			def dictionaries_to_pandas_helper(raw_dyct,deepcopy:bool=True):
				from copy import deepcopy as dc
				dyct = dc(raw_dyct) if deepcopy else raw_dyct
				for key in list(raw_dyct.keys()):
					dyct[key] = [dyct[key]]
				return pd.DataFrame.from_dict(dyct)

			return frame(
				pd.concat( list(map( dictionaries_to_pandas_helper,arr )), ignore_index=True )
			)
		
		@staticmethod
		def from_dbhub_query(query:str, dbhub_apikey, dbhub_owner, dbhub_name):
			from ephfile import ephfile
			import pydbhub.dbhub as dbhub
			with ephfile("config.ini") as eph:
				eph += f"""[dbhub]
	api_key = {dbhub_apikey}
	db_owner = {dbhub_owner}
	db_name = {dbhub_name}
			"""
				try:
					db = dbhub.Dbhub(config_file=eph())

					r, err = db.Query(
						dbhub_owner,
						dbhub_name,
						query
					)
					if err is not None:
						print(f"[ERROR] {err}")
						sys.exit(1)
					return frame.from_arr(r)
				except Exception as e:
					print(e)
		
		@staticmethod
		def from_dbhub_table(table_name, dbhub_apikey, dbhub_owner, dbhub_name):
			return frame.from_dbhub_query(
				'''
				SELECT * 
				FROM {0}
				'''.format(table_name),
				dbhub_apikey, dbhub_owner, dbhub_name
			)

		@property
		def roll(self):
			class SubSeries(pd.Series):
				def setindexdata(self, index, data):
					self.custom__index = index
					self.custom__data = data
					return self

				def __setitem__(self, key, value):
					super(SubSeries, self).__setitem__(key, value)
					self.custom__data.at[self.custom__index,key] = value

			self.current_index=0
			while self.current_index < self.shape[0]:
				x = SubSeries(self.iloc[self.current_index]).setindexdata(self.current_index, self)

				self.current_index += 1
				yield x

		@property
		def readRoll(self):
			self.current_index=0
			while self.current_index < self.shape[0]:
				x = obj(self.iloc[self.current_index]).setindexdata(self.current_index, self)
				self.current_index += 1
				yield x

		def tobase64(self, encoding='utf-8'):
			import base64
			return base64.b64encode(self.to_json().encode(encoding)).decode(encoding)

		@staticmethod
		def frombase64(string, encoding='utf-8'):
			import base64
			return frame.from_json(base64.b64decode(string.encode(encoding)).decode(encoding))
		
		def quick_heatmap(self,cmap ='viridis',properties={'font-size': '20px'}):
			return self.style.background_gradient(cmap=cmap).set_properties(**properties) 

		def heatmap(self, columns,x_label='',y_label='',title=''):
			import seaborn as sns
			import matplotlib.pyplot as plt
			sns.set()
			SMALL_SIZE = 15
			MEDIUM_SIZE = 20
			BIGGER_SIZE = 25

			plt.rc('font', size=MEDIUM_SIZE)		  # controls default text sizes
			plt.rc('axes', titlesize=MEDIUM_SIZE)	 # fontsize of the axes title
			plt.rc('axes', labelsize=MEDIUM_SIZE)	# fontsize of the x and y labels
			plt.rc('xtick', labelsize=SMALL_SIZE)	# fontsize of the tick labels
			plt.rc('ytick', labelsize=SMALL_SIZE)	# fontsize of the tick labels
			plt.rc('legend', fontsize=SMALL_SIZE)	# legend fontsize
			plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

			temp_frame = self.copy()
			mask = temp_frame.columns.isin(columns)

			temp_frame.loc[:, ~mask] = 0
			vmin, vmax = 0,0

			for col in columns:
				vmax = max(vmax, self[col].max())

			sns.heatmap(temp_frame, annot=True, fmt="d", vmin=vmin, vmax=vmax, cmap="Blues")
			plt.xlabel(x_label) 
			plt.ylabel(y_label) 

			# displaying the title
			plt.title(title)
			plt.rcParams["figure.figsize"] = (40,30)

			if False:
				plt.savefig(
					'get_size.png',
					format='png',
					dpi=height/fig.get_size_inches()[1]
				)
			plt.show()
		
		@property
		def df(self):
			from copy import deepcopy as dc
			return pd.DataFrame(dc(self))
		
		def dup(self):
			from copy import deepcopy as dc
			return frame(dc(self))
		
		@staticmethod
		def dupof(dataframe):
			from copy import deepcopy as dc
			return frame(dc(dataframe))
		
		@property
		def dummies(self):
			return pd.get_dummies(data = self)

		@property
		def kolz(self):
			return lyst(self.columns.tolist())
		
		def enumerate_kol(self):
			for column_itr, column in enumerate(self.kolz):
				self.rename_column(column, str(column_itr)+"_"+column)
			return self

		@staticmethod
		def from_sqlite(file="out.sqlite", table_name="main"):
			output = pd.DataFrame()

			if not os.path.exists(file):
				return frame(output)

			connection = sqlite3.connect(file)
			table_names, found = [], False
			current_cursor = connection.cursor()

			current_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
			for name in current_cursor.fetchall():
				table_names += [name[0]]
				if table_name == name[0]:
					output = pd.read_sql_query("SELECT * FROM {0}".format(name[0]), connection)
					found = True
					break

			if not found:
				print("table {0} not within [{1}]".format(table_name, ', '.join(table_names)))

			current_cursor = None
			connection.close()

			return frame(output)

		def to_sqlite(self, file="out.sqlite", table_name="default"):
			from sqlalchemy import create_engine
			with create_engine('sqlite://{0}'.format(file), echo=False).begin() as connection:
				self.to_sql(table_name, con=connection, if_exists='replace')
			return file

		def to_sqlcreate(self, file="out.sql", name="temp", number_columnz = False, every_x_rows=-1):
			working = self.dup()

			if number_columnz:
				working.enumerate_kol()
				#columns = working.kolz
				#for column_itr, column in enumerate(columns):
				#	working.rename_column(column, str(column_itr)+"_"+column)

			if every_x_rows is None or every_x_rows == -1:
				#https://stackoverflow.com/questions/31071952/generate-sql-statements-from-a-pandas-dataframe
				with open(file,"w+") as writer:
					writer.write(pd.io.sql.get_schema(working.reset_index(), name))
					writer.write("\n\n")
					for index, row in working.iterrows():
						writer.write('INSERT INTO '+name+' ('+ str(', '.join(working.columns))+ ') VALUES '+ str(tuple(row.values)))
						writer.write("\n")
			else:
				#https://stackoverflow.com/questions/31071952/generate-sql-statements-from-a-pandas-dataframe
				ktr = 0
				nu_file = file.replace('.sql', '_' + str(ktr).zfill(5) + '.sql')

				with open(nu_file,"w+") as writer:
					writer.write(pd.io.sql.get_schema(working.reset_index(), name))
					writer.write("\n\n")

				for index, row in working.iterrows():
					if index % every_x_rows == 0:
						ktr = ktr + 1
						nu_file = file.replace('.sql', '_' + str(ktr).zfill(5) + '.sql')

					with open(nu_file,"a+" if os.path.exists(nu_file) else "w+") as writer:
						writer.write("\n")
						writer.write('INSERT INTO '+name+' ('+ str(', '.join(working.columns))+ ') VALUES '+ str(tuple(row.values)))
						writer.write("\n")

		def ofQuery(self, query:str):
			return frame(self.query(query))

except:
	pass

class lyst(list):
	def __init__(self,*args,**kwargs):
		super(lyst,self).__init__(*args,**kwargs)
	
	def trims(self, filterlambda=None):
		to_drop = []

		for x_itr,x in enumerate(self):
			if(
				(filterlambda != None and filterlambda(x))
				or
				(filterlambda == None and x == None)
			):
				to_drop += [x_itr]
		
		to_drop.reverse()
		for to_drop_itr in to_drop:
			self.pop(to_drop_itr)
		
		return self
	
	@property
	def length(self):
		return len(self)

	def roll(self, kast=None,filter_lambda = None):
		for item in self:
			if kast:
				item = kast(item)

			if filter_lambda==None or filter_lambda(item):
				yield item
	
	def joins(self,on=","):
		return on.join(self)
	
	def execs(self):
		return [string(x).exec() for x in self if isinstance(x, str)]

	@staticmethod
	def of(obj: object, functor=None) -> list:
		if not functor or functor is None:
			def functor(x):
				return x

		if isinstance(obj, list):
			return lyst([functor(x) for x in obj])
		else:
			return lyst([functor(obj)])

import multiprocessing
import time
class timeout(object):
	"""
	with mystring.timeout(6*10, func=callr.pull) as exe:
	if not exe.timeout:
		resultr = exe.output
	"""
	#https://stackoverflow.com/questions/10415028/how-to-get-the-return-value-of-a-function-passed-to-multiprocessing-process/10415215#10415215
	#https://stackoverflow.com/questions/492519/timeout-on-a-function-call
	def __init__(self, number_of_seconds, func, *args, **kwargs):
		self.queue = multiprocessing.Queue()
		self.num_sec = number_of_seconds
		self.proc = multiprocessing.Process(target=self._wrapper, args=[func, self.queue, args, kwargs])
		
		self.exe = False
		self.timeout = False
		self.output = None

	@staticmethod
	def _wrapper(func, queue, args, kwargs):
		ret = func(*args, **kwargs)
		queue.put(ret)
	
	def run(self):
		if not self.exe and self.proc is not None:
			print("Processing")
			self.exe = True
			self.proc.start()
			self.proc.join(self.num_sec)
			self.timeout = self.proc.is_alive()

			if self.timeout:
				# or self.proc.terminate() for safely killing thread
				self.proc.kill()
				self.proc.join()
			else:
				self.output = self.queue.get()
				try:
					import pandas as pd
					if isinstance(self.output, pd.DataFrame):
						self.output = frame(self.output)
				except:
					pass
				if isinstance(self.output, list):
					self.output = lyst(self.output)
				elif isinstance(self.output, str):
					self.output = string(self.output)
	
	def __enter__(self):
		self.run()
		return self
	
	def __exit__(self, type, value, traceback):
		return

import hashlib,base64,json
from fileinput import FileInput as finput
class foil(object):
	def __init__(self, path, preload=False):
		self.path = path
		if preload:
			with open(self.path, "r") as reader:
				self._content = lyst([string(x) for x in reader.readlines()])
		else:
			self._content = lyst([])

	def __enter__(self, append=False):
		self._content = lyst([])
		yield finput(self.path, inplace=True)
	
	def __exit__(self,type, value, traceback):
		return
	
	@property
	def content(self):
		if self._content.length == 0:
			with open(self.path, "r") as reader:
				self._content = lyst([string(x) for x in reader.readlines()])
		return self._content
	
	def reload(self):
		self._content = lyst([])
		return self.content

	def hash_content(self,hashtype=hashlib.sha512, encoding="utf-8"):
		hashing = hashtype()
		with open(self.path, 'rb') as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hashing.update(chunk)
		return hashing.hexdigest()

	def b64_content(self, encoding="utf-8"):
		return base64.b64encode(self.content.joins("\n").encode(encoding)).decode(encoding)

	def tob64(self):
		newName = self.path+".64"
		with open(self.path, 'rb') as fin, open(newName, 'w') as fout:
			base64.encode(fin, fout)
		return newName

	@staticmethod
	def fromb64(path):
		newName = path.replace(".64",'')
		with open(self.path, 'rb') as fin, open(newName, 'w') as fout:
			base64.decode(fin, fout)
		return foil(newName)

	def structured(self):
		return str(json.dumps({
			'header':False,
			'file':self.path,
			'hash':self.hash_content(),
			'base64':self.b64_content()
		}))
	
	@staticmethod
	def is_bin(foil):
		#https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
		textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
		is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
		return is_binary_string(open(foil, 'rb').read(1024))

	@staticmethod
	def loadJson(foil):
		if not foil.isJson(foil):
			return None
		import json
		with open(foil, 'r') as reader:
			return json.load(reader)

	@staticmethod
	def getExt(path:str):
		import pathlib
		return pathlib.Path(path).suffix

	@staticmethod
	def isJson(path:str):
		return any([foil.getExt(path) == x for x in [
			".json"
		]])

	@staticmethod
	def isJava(path:str):
		return any([foil.getExt(path) == x for x in [
			".java",".jsp"
		]])

	@staticmethod
	def isScala(path:str):
		return any([foil.getExt(path) == x for x in [
			".scala"
		]])

	@staticmethod
	def isPython(path:str):
		return any([foil.getExt(path) == x for x in [
			".py",".pyi"
		]])

	@staticmethod
	def isRust(path:str):
		return any([foil.getExt(path) == x for x in [
			".rs"
		]])

	@staticmethod
	def isJs(path:str):
		return any([foil.getExt(path) == x for x in [
			".js"
		]])

class foldentre(object):
	def __init__(self,new_path:str,ini_path:str = os.path.abspath(os.curdir)):
		self.ini_path = ini_path
		self.new_path = new_path
	
	def __enter__(self):
		os.chdir(self.new_path)
		return self
	
	def __exit__(self,type, value, traceback):
		os.chdir(ini_path)
		return self

def from_b64(contents,file=None):
	string_contents = string.frombase64(contents)
	if file:
		with open(file,'w+') as writer:
			writer.write(string_contents)
		return foil(file)
	else:
		return string_contents

class wrapper:
	def __init__(self, *, typing, default, b64=False):
		self._typing = typing
		self._default = default
		self._b64=b64

	def __set_name__(self, owner, name):
		self._name = "_" + name

	def __get__(self, obj, type):
		if obj is None:
			return self._default

		value = self.typing(getattr(obj, self._name, self._default))
		if self._b64:
			value = mystring.from_b64(value)
		return value

	def __set__(self, obj, value):
		if not obj.isEmpty(value):
			if self._b64:
				value = mystring.string(value).tobase64()
			setattr(obj, self._name, self._typing(value))

	def __type__(self):
		return self._typing

class obj:
	@staticmethod
	def isEmpty(obj:object):
		if obj is None:
			return True
		return string(obj).empty

	@staticmethod
	def safe_get_check(obj, attr, default=None):
		if hasattr(obj,attr) and getattr(obj,attr) is not None and getattr(obj,attr).strip().lower() not in ['','none','na']:
			return getattr(obj,attr)
		else:
			return default

import datetime,time
class Timer(object):
	def __init__(self):
		self.start_datetime = None
		self.end_datetime = None
	
	def __enter__(self):
		self.start_datetime = datetime.datetime.now(datetime.timezone.utc)
		self.start_datetime = self.start_datetime.replace(tzinfo=datetime.timezone.utc).timestamp()
		return self
	
	def __exit__(self,type, value, traceback):
		self.end_datetime = datetime.datetime.now(datetime.timezone.utc)
		self.end_datetime = self.end_datetime.replace(tzinfo=datetime.timezone.utc).timestamp()
		return self
	
	def __dict__(self):
		return {
			"start_datetime_UTC": self.start_datetime,
			"end_datetime_UTC": self.end_datetime,
			"durationS": (self.end_datetime - self.start_datetime).seconds,
			"durationMS": (self.end_datetime - self.start_datetime).microseconds,
		}

import threading, queue, time
from typing import Dict, List, Union, Callable
class MyThread(threading.Thread):
	def __init__(self, func, threadLimiter=None, group=None, target=None, name=None,args=(), kwargs=None):
		super(MyThread,self).__init__(group=group, target=target, name=name)
		self.func = func
		self.threadLimiter = threadLimiter
		self.args = args
		self.kwargs = kwargs
		return

	def run(self): 
		if self.threadLimiter:
			self.threadLimiter.acquire() 
		try: 
			self.func() 
		finally: 
			if self.threadLimiter:
				self.threadLimiter.release() 

class MyThreads(object):
	def __init__(self, num_threads):
		self.num_threads = num_threads
		self.threadLimiter = threading.BoundedSemaphore(self.num_threads)
		self.threads = queue.Queue()

	def __iadd__(self, obj: Union[Callable]):
		if isinstance(obj, Callable):
			obj = MyThread(obj, self.threadLimiter)
		
		if not isinstance(obj, MyThread):
			print("Cannot add a-none function")
			return self
		
		self.threads.put(obj)
		obj.start()
		return self
	
	@property
	def complete(self):
		if self.threads.qsize() > 0:
			for tread in iter(self.threads.get, None):
				if tread != None and tread.isAlive():
					return False
		return True

	def wait_until_done(self, printout=False):
		if printout:
			print("[",end='',flush=True)

		while not self.complete:
			time.sleep(1)
			if printout:
				print(".",end='',flush=True)

		if printout:
			print("]",flush=True)

class grading(object):
	"""
	https://github.com/microsoft/pybryt/tree/1e87fbe06e3e190bab075dab1064cfe275044f75
	https://github.com/microsoft/pybryt/
	advance: http://aka.ms/advancedpybryt
	"""
	def __init__(self, reference:str):
		import pybryt
		self.ref = pybryt.ReferenceImplementation.compile(reference)
		self.subs = {}


	def __iadd__(self, value:str):
		import pybryt
		if value.endswith(".py"):
			from . import py2nb
			import ephfile
			with ephfile.ephfile(value.replace(".py",".ipynb")) as eph:
				py2nb.convert(value)
				studentImpl = pybryt.StudentImplementation(eph())
		else:
			studentImpl = pybryt.StudentImplementation(value)

		self.subs[f"Sub_{len(self.subs.keys())}"] = {
			"Implementation":studentImpl
		}
		return self


	def grade(self):
		results = []
		for key, value in self.subs.items():
			value['Result'] = value["Implementation"].check(self.ref)
			results += [value['Result']]
		return results


	def __call__(self, *args, **kwargs):
		self.grade()
		return results


	def __enter__(self):
		return self


	def __exit__(self, type, value, traceback):
		return


	def val(self, value:object, on_success:str, on_failure:str):
		import pybryt
		return pybryt.Value(value, success_message=on_success, failure_message=on_failure)


	@staticmethod
	def value(value:object, on_success:str, on_failure:str):
		import pybryt
		return pybryt.Value(value, success_message=on_success, failure_message=on_failure)

class session(object):
	def __init__(self, lock, onCall=None, onOpen=None, onClose=None):
		self.lock = lock
		self.onCall = onCall
		self.onOpen = onOpen
		self.onClose = onClose

	def __enter__(self):
		self.lock.acquire()

		if self.onOpen:
			self.onOpen()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.onClose:
			self.onClose()

		self.lock.release()

	def __call__(self, string: object):
		if self.onCall:
			return self.onCall(string)
		else:
			return string

def walker(path:str=".", eachFile=None, eachFolder=None):
	import os
	for root, dirnames, fnames in os.walk(path):
		for dirname in dirnames:
			if eachFolder is not None:
				eachFolder(os.path.join(root,dirname))

		for fname in fnames:
			if eachFile is not None:
				eachFile(os.path.join(root,fname))