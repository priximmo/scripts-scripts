# This script is for Windows
#
import sys
import pathlib
import subprocess as sub

if len(sys.argv) < 3:
    print("{} - Make symbolic links for input's contents into output's contents"
    .format(sys.argv[0]))
    print("Usage: {} INPUT_DIRECTORY OUTPUT_DIRECTORY".format(sys.argv[0]))
    sys.exit(1)

INPUT_DIRECTORY = pathlib.Path(sys.argv[1])
OUTPUT_DIRECTORY = pathlib.Path(sys.argv[2])

try:
    for child in INPUT_DIRECTORY.iterdir():
        # child is the FQ'ed path of below variable
        current_file = child.parts[len(child.parts)-1]
        new_path = OUTPUT_DIRECTORY
        new_file = OUTPUT_DIRECTORY / current_file
        command = "MKLINK \"%s\" \"%s\"" % (new_file, child)
        ret = sub.call(command, shell=True)
        if ret != 0:
            raise OSError
        print("INPUT: {}".format(child))
        print("OUTPUT: {}".format(new_file))
except OSError:
    print("The command was not completed successfully. :(")
    sys.exit(1)
