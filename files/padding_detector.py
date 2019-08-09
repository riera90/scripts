#!/usr/bin/python3
import getopt, sys, os
from pprint import pprint

input_file = None
PADDINGSIZE = 0x50

def usage():
    print("usage:")
    print("   -h --help\t\t\tprints this help.")
    print("   -f --file <file>\t\tfile to search paddings into.")
    print("   -s --size <size_of_padding>\tsets the minimum size of the paddign in\n\t\t\t\t\thex (default is 0x50).")

try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:s:", ["help", "file=", "size="])
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
    elif o in ("-s", "--size"):
        PADDINGSIZE = int(a, 16)
        print("changing padding size to",hex(PADDINGSIZE))
        
    else:
        assert False, "unhandled option"


if input_file is None:
    print("you must specify a input file.")
    usage()
    sys.exit(3)

file = open(input_file,"rb")
content = file.read()
file.close()


f = 0
zero = 0
padding = "none"
 
print("\nfile size:", hex(os.path.getsize(input_file)), "\n")

for i, byte in enumerate(content):
    memdir = hex(i)
    memend = hex(i - 0x01)
    if byte == 0xff: # f
        if f is 0:
            memstart = memdir
        f += 1
    else:
        f = 0

    if byte == 0x0:
        if zero is 0:
            memstart = memdir
        zero += 1
    else:
        zero = 0

    if f > PADDINGSIZE:
        padding = 0xff

    if zero > PADDINGSIZE:
        padding = 0x0

    if padding is 0xff and f is 0:
        print("0xff padding from", memstart, "to", memend)
        padding = "none"

    if padding is 0x0 and zero is 0:
        print("0x00 padding from", memstart, "to", memend)
        padding = "none"
        
    
if padding is 0xff:
    print("0xff padding from", memstart, "to", memend, "(EOF)")

if padding is 0x0:
    print("0x00 padding from", memstart, "to", memend, "(EOF)")

