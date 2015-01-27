import yaml
import argparse
from pprint import pprint

DEBUG = True

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="""
		This module generates input file based on the raw input.""")

	parser.add_argument('-r', '--raw', help="""
		provide your raw input yaml file. this is required.""",
        required=True)
	
	args = vars(parser.parse_args())

	raw = args["raw"]

	try:
		stream = open(raw)
	except Exception, e:
		print 'unable to open ' + raw
		raise e

	try:
		data = yaml.load(stream)
	except Exception, e:
		print 'unable to parse raw yaml'
		raise e

	if DEBUG:
		pprint(data)

	result = ''

	for summary in data['summary']: