import shelve
from collections.abc import MutableMapping
import os
import pickle

class DirDict(MutableMapping):
	def __init__(self,directory):
		try:
			os.mkdir(directory)
		except FileExistsError:...
		self.directory = directory
	def _validate(path):
		return path == os.path.basename(path)

	def __getitem__(self,key):
		if not DirDict._validate(key):
			raise KeyError()
		try:
			with open(os.path.join(self.directory,key),'rb') as file:
				return pickle.load(file)
		except IOError as e:
			raise KeyError
	def __setitem__(self,key,value):
		if not DirDict._validate(key):
			raise KeyError("Only valid filenames can be keys.")
		with open(os.path.join(self.directory,key),'wb') as file:
			pickle.dump(value,file)
	def __delitem__(self,key):
		if not DirDict._validate(key):
			raise IndexError()
		os.rm(os.path.join(self.directory,key))
	def __iter__(self):
		return os.listdir(self.directory).__iter__()
	def __len__(self):
		return len(os.listdir(self.directory))

	def sync(self):...
	def close(self):...

class DictList:
	def __init__(self,backing):
		self.backing = backing
		if not 'length' in self.backing:
			self.backing['length'] = 0
			self.backing.sync()
	def __getitem__(self,key):
		try:
			if isinstance(key,slice):
				return [ 
					self.backing[str(index)]
					for index
					in range(*key.indices(len(self)))
				]
			elif isinstance(key,int):
				if key < 0:
					key = len(self)+key
				return self.backing[str(key)]
			else:
				raise TypeError
		except KeyError as e:
			raise IndexError('index out of range')
	def __len__(self):
		return self.backing['length']
	def append(self,element):
		length = len(self)
		self.backing['length'] += 1 # not therad safe
		self.backing[str(length)] = element
		self.backing.sync()
	def close(self):
		self.backing.close()
