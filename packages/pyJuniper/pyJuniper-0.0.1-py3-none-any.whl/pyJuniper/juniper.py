
# ------------------------------------------------------------------------------
from nettoolkit_common.gpl import STR, IO
from .hierarchy import Hierarchy 
from .jset import JSet
# ------------------------------------------------------------------------------

class Juniper():
	"""Juniper configuration file related class
	"""    	

	def __init__(self, input_file, output_file=None):
		"""Initialize object by giving input file name

		Args:
			input_file (str): _description_
			output_file (str, optional): output file name. Defaults to None.
		"""    		
		self.input_file = input_file
		self.output_file = output_file

	def _get_clean_output_file_lst(self):
		output_file_lst = []
		for line in self.input_file_lst:
			if len(line.lstrip()) > 0:
				if line.lstrip()[0] == "#": continue
				output_file_lst.append(line.rstrip("\n"))
		return output_file_lst

	def remove_remarks(self, to_file=True):
		"""remove all remark lines from config

		Args:
			to_file (bool, optional): save output to file if True. Defaults to True.

		Returns:
			lst: list of output
		"""    		
		self.input_file_lst = IO.file_to_list(self.input_file)
		output_file_lst = self._get_clean_output_file_lst()
		if to_file and self.output_file:
			IO.to_file(self.output_file, output_file_lst)
		return output_file_lst

	def convert_to_set(self, to_file=True):
		"""convert configuration to set mode

		Args:
			to_file (bool, optional): save output to file if True. Defaults to True.

		Returns:
			lst: list of output
		"""    		
		J = JSet(self.input_file)
		J.to_set
		if to_file and self.output_file:
			IO.to_file(self.output_file, J.output)
		return J.output

	def convert_to_hierarchy(self, to_file=True):
		"""convert set configuration to hiearchical configuration

		Args:
			to_file (bool, optional): save output to file if True. Defaults to True.

		Returns:
			lst: list of output
		"""    		
		H = Hierarchy(self.input_file, self.output_file)
		H.convert()
		if to_file and self.output_file:
			IO.to_file(self.output_file, H.output)
		return H.output

def convert_to_set_from_captures(conf_file, output_file=None):
	with open(conf_file, 'r') as f:
		ops = f.readlines()
	toggle = False
	conflist = ""
	for line in ops:
		if line.startswith("# output for command: show configuration| no-more"):
			toggle=True
			continue
		if not toggle: continue
		if line.startswith("# output for command: "): 
			break
		conflist+=line
	with open(conf_file[:-4]+".tmp", 'w') as f:
		f.write(conflist)
	J = Juniper(conf_file[:-4]+".tmp", output_file)
	return J.convert_to_set(output_file)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
