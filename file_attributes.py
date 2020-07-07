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

class Operation(Enum):
	## Assignment and Logico-Mathematical Operations
	ASSIGN = '='
	NAND = 'Apfelstrudel'

	ADD = '+'
	SUBTRACT = '-'
	MULTIPLY = '_'
	DIVIDE = '.'

	ADD_ASSIGN = '+='
	SUBTRACT_ASSIGN = '-='
	MULTIPLY_ASSIGN = '_='
	DIVIDE_ASSIGN = '.='

	## MARK - Custom Operations
	PRINT = 'print'

class Logic(Enum):
	## Program Logic Operations
	WHILE = 'kurt'
	IF_THEN = 'eiffelturm'
	UNTIL_DO = 'niemals!'
	IF_THEN_ELSE = 'seltsam'

	### the *less used* logical operators :p
	IF_THEN_UNLESS = 'sonderbar'
	IF_THEN_PROVIDED = 'sinnlos'
	WHILE_DO_UNLESS = 'nutzlos' # mans lost his nutz

	EQUAL = '='  # equality check symbol
	LESS_THAN_EQUAL = ' =' # confusing but this is actually <=


class DCVariable:

	def __init__(self, name, date_created, size, content):
		self.name = name
		self.size = size
		self.content = content

		if date_created == "1991":
			self.var_type = VarType.INT
		elif date_create == "1992":
			self.var_type = VarType.STRING
		else:
			self.var_type = VarType.COMMENT

	def get_value():
		if self.var_type == VarType.INT:
			return int(self.size)
		elif self.var_Type == VarType.STRING:
			return str(self.content)
		else:
			return None # comments have no value

class DCVariableRef:
	def __init__(self, name):
		self.name = name # should correspond to an actual variable

class DCOperation:

	"""
	params: array of other values that nest in the function call
	i.e. DCVariableRef, and other DCOperations
	
	"""
	def __init__(self, name: str, params: list):
		self.func_type = Operation(name)
		self.params = params

class DCProgramLogicExpression:

	def __init__(self, name: str, sub_exprs: list):
		self.expr_type = Logic(name)
		self.sub_exprs = sub_exprs


class Program:

	def __init__(self, bound_variables: dict, instructions: list):
		self.bound_variables = bound_variables
		self.instructions = instructions


def run(program: Program):
	"""
	The one magical function to rule them all. This takes in a program and runs it.
	"""
	pass


def get_file_attrib(file_path):
	try:
		st = os.stat(file_path)
	except IOError:
		print("failed to get information about", file_path)
	else:
		name = os.path.splitext(os.path.basename(file_path))[0]
		year = time.asctime(time.localtime(st[ST_MTIME]))[-4:]	
		size = st[ST_SIZE]
		data = open(file_path, "r").read()

			
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

		return name, year, size, data

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
	instructions = []

	for each file/variable/bound_literal in root directory:
		make a `Variable` obj
		store to vars_arr
	
	for each operation_directory:
		currVarRefs = []
		for each sub_directory:
			create VariableRef obj -> currentVarRefs
	
		create DCOperation obj or DCProgramLogicExpression (using try:except), pass name, currentVarRefs and params or sub_expressions

		store to instructions array

	create Program obj, pass in vars_arr, instructions
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
