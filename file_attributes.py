import os, time
from stat import *  # ST_SIZE etc
from enum import Enum, auto
import glob

# abstract base class. DO NOT INSTANTIATE

# .: -> DotCol -> DC


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
	WHILE_DO_UNLESS = 'nutzlos'  # mans lost his nutz

	EQUAL = '='  # equality check symbol
	LESS_THAN_EQUAL = ' ='  # confusing but this is actually <=


class RunState(Enum):
	RUNNING = auto()
	TERMINATED = auto()
	ERROR = auto()

class DCVariable:
	def __init__(self, name, date_created, size, content):
		self.name = name
		self.size = size
		self.content = content

		if date_created == "1991":
			self.var_type = VarType.INT
		elif date_created == "1992":
			self.var_type = VarType.STRING
		else:
			self.var_type = VarType.COMMENT

	def get_value(self):
		if self.var_type == VarType.INT:
			return int(self.size)
		elif self.var_Type == VarType.STRING:
			return str(self.content)
		else:
			return None  # comments have no value

	def __repr__(self):
		return 'DCVariable {' + 'type: {}, value: {}'.format(
			self.var_type, self.get_value()) + '}'


class DCVariableRef:
	def __init__(self, name):
		self.name = name  # should correspond to an actual variable


class DCOperation:
	"""
	params: array of other values that nest in the function call
	i.e. DCVariableRef, and other DCOperations
	"""

	def __init__(self, prefix: str, name: str, params: list):
		self.prefix = prefix
		self.func_type = Operation(name)
		self.params = params



class ProgramDirStructure:
	def __init__(self, bound_variables: dict, expressions: list):
		self.bound_variables = bound_variables # Dict[str, DCVariable]
		self.expressions = expressions



"""
Operation {
	func_type: {
		ADD, SUBTRACT, MUL, ...
	},
	params: {
		VariableRef,
		Operation
	}
}
"""

class Runner:

	def __init__(self, program: ProgramDirStructure):
		self.current_expr = None
		self.program = program
		self.cycle_count = 0
		self.run_state = RunState.RUNNING

	def eval(self, expr):
		if type(expr) == DCOperation:
			pass
		elif type(expr) == DCVariableRef:
			return self.program.bound_variables[expr.name]  # returns a DCVariable
		elif type(expr) == DCVariable:
			return expr.get_value()  # returns raw value
		else:
			self.run_state = RunState.ERROR
			return None  # signals an error


	def run(self):		
		# assuming instructions 
		for expr in self.program.expressions:
			self.current_expr = expr
			if type(expr) == DCOperation:
				pass
			elif type(expr) == DCVariableRef:
				pass
			elif type(expr) == DCVariable:
				pass
			else:
				self.run_state = RunState.ERROR
				break
			
			self.cycle_count += 1
		
		


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
	vars_dict = {}
	# instructions = []
	
	for root, dirs, files in os.walk(root_path, topdown=True):
		print("ROOT: ", root)
		print("DIRS: ", dirs)
		print("FILES: ", files)
		# technically, there are an arbitrary num of vars possible
		# however there is a constant num of logical operations and expressions
		operations = [list(Operation.__members__.keys())]
		logic = [list(Logic.__members__.keys())]
		for d in dirs:
			if (os.path.basename(d).partition(".")[2] in operations):
				print(get_dir_attrib(d))
		print('..............................')
		print([get_dir_attrib(os.path.join(root, d)) for d in dirs])
		if len(files) > 0:
			print(files)
			for f in files:
				vars_dict.update({os.path.splitext(os.path.basename(os.path.join(root, f)))[0]: DCVariable(*get_file_attrib(os.path.join(root, f)))})
		# vars_dict.update({os.path.splitext(os.path.basename(os.path.join(root, f)))[0]: [DCVariable(*get_file_attrib(os.path.join(root, f))) for f in files]})
		print("------------------------------")
		# for name in dirs:
		# 	print(os.path.join(root, name))
	# print(vars_dict)
	# print(os.listdir(root_path))
	
	# DCOperation(*get_dir_attrib(d), )

	return "BRUH"

	

# for filename in glob.iglob(root_path + '**/**', recursive=True):

"""

>>>
program directory structure (not program itself)

fileObj := {name, date_created, content, size}
literals := any fileObjs not at root

bound_values := list of filesObjs at root

subdirectory :=
	directory with:
	* 0 or more subdirectories
	* 0 or more literals
	* name

<<<

>>>
Then, we translate ProgramDirStructure -> AbstractSyntaxTree (AST)

variables := bound_values  # simple translation

def parse(programDirStructure) -> AST:
	for each directory in ROOT_DIR:
		pass

def parse(programDirStructure) -> AST:
	for each directory in ROOT_DIR:
		pass

<<<

>>>
Psuedocode for creating program

for each file/variable/bound_literal in root directory:
	make a `DCVariable` obj
	store to vars_arr

for each operation_directory:
	currVarRefs = []
	for each sub_directory:
		create VariableRef obj -> currentVarRefs

	create DCOperation obj or DCProgramLogicExpression (using try:except), pass name, currentVarRefs and params or sub_expressions

	store to instructions array

create Program obj, pass in vars_arr, instructions

<<<

>>>
# this should iterate over the root program directory
# and be a 'tree' like object of directories and files
# this will represent the AST of the program.

# pertinent objects: file -> variable
#					directory -> operation
# program: tree of directories, with files as leafs

# then, a single function will consume the result of `program_directory_structure` and run it as a program
<<<

>>>
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
<<<
"""
