import os
import sys
import getopt

replace_to = ""
to_replace = "."  # remove the dot's by default
customer_folders_path = os.getcwd()

try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:r:v:", [
                               "help", "replace=", "value="])
except getopt.GetoptError:
    print('Incorrect input format: use -h or --help for instructions')
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print('\
------------------------------------------------------\n\
Default args: -t [working directory] -r "." -v ""\n\n\
Options:\tArgument\t\tDescription\n\n\
 -h/--help \t\t\t\tShow this menu\n\
 -t/--target\t[folder path] \t\tthe folder in which to replace the files\n\
 -r/--replace\t[value to change from] \tif not specified, only get\'s rid of the dots in the filename\n\
 -v/--value\t[value to change to] \tif not specified it\'s blank\n\
            ')
        sys.exit()
    elif opt in ("-t", "--target"):
        customer_folders_path = arg
    elif opt in ("-r", "-replace"):
        to_replace = arg
    elif opt in ("-v", "-value"):
        replace_to = arg

if __name__ == "__main__":
    for directname, directnames, files in os.walk(customer_folders_path):
        for f in files:
            # Split the file into the filename and the extension, saving
            # as separate variables
            filename, ext = os.path.splitext(f)
            if to_replace in filename:
                # If a '.' is in the name, rename, appending the suffix
                # to the new file
                # new_name = filename.replace(".", " ")
                new_name = filename.replace(str(to_replace), replace_to)
                print(filename, " => ", new_name)
                os.rename(
                    os.path.join(directname, f),
                    os.path.join(directname, new_name + ext))
