from argparse import ArgumentParser

def arg_parser(arg_length):
	if arg_length <= 3:
		parser = ArgumentParser()
		parser.add_argument('infile', action='store', type=str, help='Please enter a path')
		parser.add_argument('-f', '--full', action='store_true')
		return parser.parse_args()
	else:
		parser = ArgumentParser()
		mode_1 = parser.add_mutually_exclusive_group()
		mode_2 = parser.add_mutually_exclusive_group()
		parser.add_argument('infile', action='store', type=str, help='Please enter a path')
		parser.add_argument('-t', '--tag', type=str, required=True, help='Digest of the file you want a proof of')
		# add arguments for proof mode
		mode_1.add_argument('-p', '--proof', action='store_true')
		mode_1.add_argument('-i' '--input', type=str, help='Input file of the proof')
		# add arguments for verification mode
		mode_2.add_argument('-v', '--verify', action='store_true')
		mode_2.add_argument('-o' '--output', type=str, help='Output file for the proof')
		return parser.parse_args()