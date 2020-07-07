import os, time
from stat import * # ST_SIZE etc
from enum import Enum, auto
import glob

# abstract base class. DO NOT INSTANTIATE

# .: -> DotCol -. DC

class VarType(Enum):
	INT = 0
	STRING = 1
	COMMENT = 2

class Operations(Enum):
	ASSIGN = '='
	NAND = 'Apfelstrudel'

	ADD = '+'
	SUBTRACT = '-'
	MULTIPLY = '_'
	DIVIDE = '.'

	ADD_ASSIGN = '+='
	SUBTRACT_ASSIGN = '-'
	MULTIPLY_ASSIGN = '_'
	DIVIDE_ASSIGN = '.'


class Logic(Enum):
	WHILE = 'kurt'
	IF_THEN = 'eiffelturm'
	UNTIL_DO = 'niemals!'
	IF_THEN_ELSE = 'seltsam'

	# the *less used 
	IF_THEN_UNLESS = 'sonderbar'
	IF_THEN_PROVIDED = 'sinnlos'
	WHILE_DO_UNLESS = 'nutzlos' # mans lost his nutz


class Variable:

	def __init__(self, name, var_type, size, content):
		self.name = name
		self.var_type = var_type
		self.size = size
		self.content = content

	def get_value():
		if self.var_type == VarType.INT:
			return int(self.size)
		elif self.var_Type == VarType.STRING:
			return str(self.content)
		else:
			return None # comments have no value

class VariableRef:
	def __init__(self, name):
		self.name = name

class DCFunctionCall:

	"""
	objects: array of other values that nest in the function call
	i.e. DCString, DCInteger, DCComment, and other DCFunctionCalls
	
	"""
	def __init__(self, name, var_type, size, content):
		self.func_type = Operation[name]

class Program:

	def __init__(self, bound_variables: dict, function_calls: list):
		self.bound_variables = bound_variables
		self.function_calls

def get_file_attrib(file_path):
	try:
		st = os.stat(file_path)
	except IOError:
		print("failed to get information about", file_path)
	else:
		year = time.asctime(time.localtime(st[ST_MTIME]))[-4:]
		name = os.path.splitext(os.path.basename(file_path))[0]
		size = st[ST_SIZE]
		data = open(file_path, "r").read()
		# data = os.read(file_path)

		if year == "1991":
			var_type = VarType.INT
		elif year == "1992":
			var_type = VarType.STRING
		else:
			var_type = VarType.COMMENT
			
		# print("prefix:", prefix)
		# print("file name:", name)
		# print("var type:", var_type)
		# print("file size:", size)
		# print("file content:", data)

		# file name -> variable
		# file size -> content of variable
		# file creation date -> data type
			# 1991 -> int
			# 1992 -> string
			# Files with creation dates outside [1991,1992] are ignored and can be used as comments.

		return name, var_type, size, data

def get_dir_attrib(dir_path):
	filename = os.path.splitext(os.path.basename(dir_path))
	prefix = filename[0]
	dir_name = filename[1]
	return prefix, dir_name

def get_program_directory_structure(root_path):
	# this should iterate over the root program directory
	# and be a 'tree' like object of directories and files
	# this will represent the AST of the program.

	# pertinent objects: file -> variable
	#                    directory -> operation
	# program: tree of directories, with files as leafs

	# then, a single function will consume the result of `program_directory_structure` and run it as a program

	"""
	COLLAPSE {
		Root {
			FileA
			FileB
			FileC
			DirectoryOp {
				DirectoryOp {
					DirectoryRef {}
					DirectoryRef {}
				}
				
			}
			DirectoryOp {
				DirectoryRef {}
			}
		}
		=>
		Program {
			VarA
			VarB
			VarC
			Operation {
				Operation {
					VarA 
					VarB
				}
				VarC
			}
			Operation {
				VarB
			}
		}
		def run(program)
	}
	"""
	# for filename in glob.iglob(root_path + '**/**', recursive=True):


	"""
	Psuedocode for creating program
	
	vars_arr = []
	functionCallsArr = p[]

	for each file/variable/bound_literal in root directory:
		make a `Variable` obj
		store to vars_arr
	
	for each operation_directory:
		currVarRefs = []
		for each sub_directory:
			create VariableRef obj -> currentVarRefs
	
		create FunctionCall obj, pass currentVarRefs and related info

		store to functionCallsArr

	create Program obj, pass in vars_arr, functionCallsArr
	"""

	for root, dirs, files in os.walk(root_path, topdown=True):
		print(root)
		print([get_dir_attrib(os.path.join(root, d)) for d in dirs])
		print([get_file_attrib(os.path.join(root, f)) for f in files])
		print("--")
		for name in files:
			print(os.path.join(root, name))
	for name in dirs:
		print(os.path.join(root, name))
		
	print(os.listdir(root_path))
	return 
	


# fp = open("file.dat")
# st = os.fstat(fp.fileno())
