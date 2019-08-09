#!/usr/bin/python3
import getopt, sys, os
from pprint import pprint

input_file = None
output_file = None
start_dir = None
end_dir = None

def usage():
    print("usage:")
    print("   -h --help\t\t\tprints this help.")
    print("   -f --file <file>\t\tfile to trimm from.")
    print("   -s --start <dir>\tsets the starting mem dir.")
    print("   -e --end <dir>\tsets the end fo the mem dir.")
    print("   -w --write <dir>\tsets the output file.")

try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:s:e:w:", ["help", "file=", "start=", "end=", "write="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(str(err))
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-f", "--file"):
        input_file = a
    elif o in ("-s", "--start"):
        start_dir = int(a, 16)
    elif o in ("-e", "--end"):
        end_dir = int(a, 16)
    elif o in ("-w", "--write"):
        output_file = a
        
    else:
        assert False, "unhandled option"


if input_file is None:
    print("you must specify a input file.")
    usage()
    sys.exit(3)
    
if start_dir is None:
    print("you must specify a starting memdir.")
    usage()
    sys.exit(3)
    
if end_dir is None:
    print("you must specify an ending memdir.")
    usage()
    sys.exit(3)

if output_file is None:
    print("you must specify an output file.")
    usage()
    sys.exit(3)

if start_dir >= end_dir:
    print("the end_dir must be greater than the start_dir")
    sys.exit(4)
    
if end_dir > os.path.getsize(input_file):
    print("the end_dir must be inside the file itself")
    sys.exit(5)
    


input = open(input_file, "rb")
content = input.read()
input.close()

content_output = content[start_dir:end_dir]

output = open(output_file, "wb")
output.write(content_output)
output.close()