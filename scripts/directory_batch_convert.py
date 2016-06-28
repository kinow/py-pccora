import os
import sys
import re
from pathlib import Path

import argparse

from convert2netcdf4 import parseandconvert

parser = argparse.ArgumentParser(description='Recursively batch convert Vaisala old-binary format to NetCDF files. Keeps directory structure.')
parser.add_argument('--from', dest='fromdir', help='Input directory', required=True)
parser.add_argument('--to', dest='todir', help='Output directory. Created if not exists. Files will be overwritten.', required=True)

EXTENSION_REGEX = r'.*\.edt$|.*\.[0-9]{2}e$'

def main():
    args = parser.parse_args()

    from_dir = Path(args.fromdir)
    to_dir = Path(args.todir)

    for dirpath, dirnames, files in os.walk(from_dir.as_posix()):
        for name in files:
            #if name.lower().endswith(extension):
            if re.match(EXTENSION_REGEX, name.lower(), re.M|re.I):
                input_file = os.path.join(dirpath, name)
                input_path = Path(input_file)

                diff = input_path.relative_to(from_dir)
                output_path = to_dir.joinpath(diff)
                extension = output_path.suffix
                output_file = output_path.as_posix()
                output_file = output_file.replace(extension, '.nc')

                if not output_path.parent.exists():
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                #print(output_file)
                try:
                    parseandconvert(input_file, output_file)
                except:
                    print("### %s" % (output_file))


if __name__ == '__main__':
    main()

    sys.exit(0)