import os, time, sys
from stat import *  # ST_SIZE etc
from enum import Enum, auto
import glob
from functools import reduce

# abstract base class. DO NOT INSTANTIATE

# .: -> DotCol -> DC
"""
We might need this
sys.setrecursionlimit(1500)
"""


class DCException(Exception):
	def __init__(self, reason):
		super.__init__(reason)


class VarType(Enum):
	INT = "1991"
	STRING = "1992"
	COMMENT = ""


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
	LESS_THAN_EQUAL = ' ='  # confusing but this is actually <= (_=)


class RunState(Enum):
	RUNNING = auto()
	TERMINATED = auto()
	ERROR = auto()


class DCVariable:
	def __init__(self, name, date_created, size, content, is_literal=False):
		self.name = name
		self.size = size
		self.content = content
		self.is_literal = is_literal

		if date_created == "1991":
			self.var_type = VarType.INT
		elif date_created == "1992":
			self.var_type = VarType.STRING
		else:
			self.var_type = VarType.COMMENT

	@staticmethod
	def make_literal(data):

		if type(data) == int:
			return DCVariable('', VarType.INT.value, data, '?' * data, True)
		elif type(data) == str:
			return DCVariable('', VarType.STRING.value, len(data), data, True)
		else:
			raise DCException(
				'ok dude, you really had to make a literal out of: {}, when you know it has to be a string or int. smh my head dude'
				.format(data))

	def get_value(self):
		if self.var_type == VarType.INT:
			return int(self.size)
		elif self.var_Type == VarType.STRING:
			return str(self.content)
		else:
			return None  # comments have no value

	def set_value(self, new_value):
		if self.is_literal:
			raise DCException(
				'hey u dumbass you tried to rebind a constant  to another constant. wtf is wrong with you.'
			)
		else:
			if type(new_value) == int:
				self.size = new_value
			elif type(new_value) == str:
				self.content = new_value
				self.size = len(new_value)
			else:
				raise DCException(
					'hey what kinda dumbass data: ({}) are you giving me you hoe'
					.format(str(new_value)))

	def __repr__(self):
		return 'DCVariable {' + 'type: {}, value: {}'.format(
			self.var_type, self.get_value()) + '}'


class DCVariableRef:
	def __init__(self, name):
		self.name = name  # should correspond to an actual variable

	def __repr__(self):
		return 'DCVariableRef {' + 'name: {}'.format(self.name) + '}'


class DCExpression:
	"""
	params: array of other values that nest in the function call
	i.e. DCVariableRef, and other DCExpressions
	"""

	def __init__(self, name: str, params: list):
		self.name = name  # string of operation name
		self.params = params  # literals and varRefs and other DCExpressions within expression

	@property
	def is_control_flow(self):
		try:
			Logic(self.name)
			return True
		except:
			return False


class Program:
	def __init__(self, bound_variables: dict, expressions: dict):
		self.bound_variables = bound_variables  # Dict[str, DCVariable], where key is the name of the variable
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
	def __init__(self, program: Program):
		self.current_expr = None
		self.program = program
		self.cycle_count = 0
		self.run_state = RunState.RUNNING

	def ref2var(self, ref) -> DCVariable:
		assert type(ref) == DCVariableRef or DCVariable

		if type(ref) == DCVariable:
			return ref  # not a ref, just a variable.

		if not ref.name in self.program.bound_variables:
			raise DCException(
				'hey man, unfortunately the variable you are looking for: ({}) cannot be reached at this time. please try again later.'
				.format(ref))
		else:
			return self.program.bound_variables[
				ref.name]  # going from dcvarref -> dcvar like a boss

	def eval(self, expr):
		if type(expr) == DCExpression:
			"""
			assuming disambiguate logic vs operation and cast to appropriate enum here.
			
			2. switch on expression enum, perform desired operation
				a. run eval on all params.
			3. return result.

			vait. but this will only work for "Assignment and Logico-Mathematical Operations", and not "Program Logic"
			"""
			# ASSUMING ONLY OPERATIONS!! NO LOGIC
			try:
				op = Operation(expr.name)
			except ValueError:
				return self.do_control_flow(expr)
				# raise DCException('tried to evaluate a Logic expr')

			if op == Operation.ASSIGN:
				assignee = self.ref2var(expr.params[0])
				val2assign = self.eval(expr.params[1])

				assert type(assignee) == DCVariableRef
				assert type(val2assign) == DCVariableRef or type(
					val2assign) == DCVariable

				assignee.set_value(val2assign.get_value())

				return None  # assignment doesn't return anything (i would hope)

			elif op == Operation.NAND:
				# i guess its just bitwise nand of ints
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT
				assert b.var_type == VarType.INT

				return DCVariable.make_literal(~(a.get_value & b.get_value))

			elif op == Operation.PRINT:
				# i'm going to assume the print instruction is n-ary, and print all args
				vals = map(lambda x: self.eval(x), expr.params)
				for val in vals:
					print(val.get_value())

				return None

			# i'm semi i stay automatic
			# money add then multiply

			elif op == Operation.ADD:
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT and b.var_type == VarType.INT

				return DCVariable.make_literal(a.get_value() + b.get_value())

			elif op == Operation.ADD_ASSIGN:
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT and b.var_type == VarType.INT

				a.set_value(a.get_value() + b.get_value())

				return None

			elif op == Operation.SUBTRACT:
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT and b.var_type == VarType.INT

				return DCVariable.make_literal(a.get_value - b.get_value)

			elif op == Operation.SUBTRACT_ASSIGN:
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT and b.var_type == VarType.INT

				a.set_value(a.get_value() - b.get_value())

				return None

			elif op == Operation.MULTIPLY:
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT and b.var_type == VarType.INT

				return DCVariable.make_literal(a.get_value() * b.get_value())

			elif op == Operation.MULTIPLY_ASSIGN:
				a = self.eval(expr.params[0])
				b = self.eval(expr.params[1])

				assert a.var_type == VarType.INT and b.var_type == VarType.INT

				a.set_value(a.get_value() * b.get_value())

				return None

		elif type(expr) == DCVariableRef:
			return self.ref2var(expr)  # returns a DCVariable
		elif type(expr) == DCVariable:
			return expr  # returns the variable (base case)
		else:
			raise DCException(
				'Invalid expr type of expression {}'.format(expr))

	def do_control_flow(self, expr):
		assert type(expr) == DCExpression

		try:
			logic_op = Logic(expr.name)
		except ValueError:
			return self.eval(expr)

		if logic_op == Logic.WHILE:
			pass
		# elif logic_op == Logic.IF_THEN:
			pass
		elif logic_op == Logic.UNTIL_DO:
			pass

	def run(self):

		for expr in self.program.expressions:
			self.current_expr = expr

			self.eval(expr)

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


def get_program_directory_structure(rootdir):
	"""
	Creates a nested dictionary that represents the folder structure of rootdir
	"""
	dir = {}
	rootdir = rootdir.rstrip(os.sep)
	start = rootdir.rfind(os.sep) + 1
	for path, dirs, files in os.walk(rootdir):
		folders = path[start:].split(os.sep)
		subdir = dict.fromkeys(files)
		parent = reduce(dict.get, folders[:-1], dir)
		parent[folders[-1]] = subdir

	return dir


def create_ast(prog_dir_struct):
	
	pass


"""
LMAOOOO IM DEAD :skull: :skull:
wow yes thakn you very c00l
"""


def some_fresh_bullshit(root_path):
	vars_dict = {}
	# instructions = []
	expression_names = {}
	program_dir_struct = {}
	for root, dirs, files in os.walk(root_path, topdown=True):
		program_dir_struct[root]
		print("ROOT: ", root)
		print("DIRS: ", dirs)
		# technically, there are an arbitrary num of vars possible
		# however there is a constant num of logical operations and expressions
		expressions = [e.value for e in Operation]
		expressions.extend([e.value for e in Logic])
		print("EXPRESSIONS:")
		print('..............................')

		if len(dirs) > 0:
			for d in dirs:
				if (str(d).partition(".")[2] in expressions):
					print(str(d).partition(".")[2], "is an expression")
					expression_names.update({
						str(d).partition(".")[2]: []
					})  #..
				else:
					DCVariableRef(str(d).partition(".")[0])
		print('..............................')
		print("FILES: ")
		if len(files) > 0:
			print(files)
			for f in files:
				vars_dict.update(
					{
						os.path.splitext(
							os.path.basename(os.path.join(root, f)))[0]:
						DCVariable(*get_file_attrib(os.path.join(root, f)))
					})  # check: initial pass looks ok (handling bound_vars)

		print('==============================')
	print(vars_dict)
	# print(os.listdir(root_path))

	# DCExpression(*get_dir_attrib(d), )
	# also you need to be returning a `ProgramDirStructure`, as opposed to the literal "BRUH LMAO". v00ps my bad

	return "BRUH LMAO"


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

	create DCExpression obj or DCProgramLogicExpression (using try:except), pass name, currentVarRefs and params or sub_expressions

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
