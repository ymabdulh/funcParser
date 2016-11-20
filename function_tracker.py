class FunctionTracker(object):
	"""
		This class is designed to keep track of the functions parsed
		by the main cpp_func_parser file. It keeps track of each
		function and the files that have defined it. This can be used
		for a variety of things including detecting duplicate
		function definitions in multiple files.
	"""
	
	def __init__(self, arg=None):
		#super(ClassName, self).__init__()
		self.arg = arg

		# dictionary of sets indexed by [function][filename]
		# just keeps track of all the files a function is defined in
		self.matrix = {}
		self.filenames = set()

	def __iter__(self):
		self.func_names = self.matrix.keys()
		self.current_idx = -1
		return self

	def __next__(self):
		self.current_idx += 1
		if self.current_idx < len(self.func_names):
			func_name = self.func_names[self.current_idx]
			return (func_name, list(self.matrix[func_name]))
		else:
			raise StopIteration

	next = __next__

	def add(self, func_name, filename):
		'''
			add a function found in a file
		'''

		if func_name not in self.matrix:
			self.matrix[func_name] = set()

		self.matrix[func_name].add(filename)
		self.filenames.add(filename)

	def add_file(self, func_names, filename):
		'''
			add multiple functions found in a file
		'''

		for func_name in func_names:
			self.add(func_name, filename)


	def get_files(self, func_name=None):
		'''
			get a list of all files this function is defined in
		'''
		if func_name is None:
			return list(self.filenames)

		return list(self.matrix[func_name]) if func_name in self.matrix else None

	def get_funcs(self, filename=None):
		'''
			get all the functions defined in a file
		'''
		if filename is None:
			return self.matrix.keys()

		funcs_in_file = []
		if filename not in self.filenames:
			return funcs_in_file

		for func_name_key, filename_list_val in self.matrix.iteritems():
			# see if this function was defined in the target
			# filename and add to list if yes
			if filename in filename_list_val:
				funcs_in_file.append(func_name_key)
				continue # set contains filename at most once

		return funcs_in_file

	def get_duplicate_funcs(self):
		'''
			returns a list of function that are defined in multiple different files
			the list is sorted, functions defined in more files (higher duplicate count) appear first
		'''

		return sorted([x for x in self.matrix.keys() if len(self.matrix[x]) > 1], key=lambda x: len(self.matrix[x]), reverse=True)

	def get_num_duplicated(self, func_name):
		'''
			returns the number of times (files in which) a function was defined
		'''

		return len(self.matrix[func_name]) if func_name in self.matrix else 0

