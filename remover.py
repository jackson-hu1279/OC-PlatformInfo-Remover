#!/usr/bin/env python3

import os
import argparse
import plistlib

# Define default plist file name to load
PLIST_FILE_NAME = "config.plist"

# Define sensitive keys and replaced value
DEFAULT_VALUE = "**REQUIRED**"
KEYS_TO_REMOVE = ["SystemProductName", "MLB", "SystemSerialNumber", "SystemUUID"]

# Control debug log print
DEBUG = False


# Load the given plist file
def load_plist_file(file_name):
    try:
        with open(file_name, "rb") as fp:
            plist_data = plistlib.load(fp)
    except FileNotFoundError:
        print(f"Error: Cannot find the file '{file_name}'")
        exit(-1)
    except Exception as e:
        print(f"An error occurred when loading the file '{file_name}'")
        if DEBUG:
            print(f"Error message: {e}")
        exit(-1)

    return plist_data


# Remove sensitive PlatformInfo values
def remove_platform_values(plist_data):
    # Retrieve original PlatformInfo values
    platforminfo_dict = plist_data["PlatformInfo"]["Generic"]

    # Remove sensitive PlatformInfo values
    # Original values will be replaced with default value
    for key in KEYS_TO_REMOVE:
        if key in platforminfo_dict.keys():
            if DEBUG:
                print(f"Found match key: {key}")
                print(f"Value to remove: {platforminfo_dict[key]}\n")
            platforminfo_dict[key] = DEFAULT_VALUE

    plist_data["PlatformInfo"]["Generic"] = platforminfo_dict
    plist_data_updated = plist_data

    return plist_data_updated


# Save plist data as a new file
def save_new_plist_file(original_file_name, plist_data):
    file_new_name = original_file_name.split(".")[0] + "_modified.plist"
    with open(file_new_name, "wb") as fp:
        plistlib.dump(plist_data, fp)


# List all files in a directory
def list_files(directory):
    try:
        # Keep only plist files
        file_list = os.listdir(directory)
        files = [
            file
            for file in file_list
            if os.path.isfile(os.path.join(directory, file)) and file.endswith(".plist")
        ]

        if DEBUG:
            print(f"Plist files found in directory: '{files}'")

        return files
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' does not exist")
    except PermissionError:
        print(f"Error: Permission denied to access the directory '{directory}'")
    except Exception as e:
        print(f"An error occurred when listing files in '{directory}'")
        if DEBUG:
            print(f"Error message: {e}")


# Process a single plist file
def process_plist_file(file_name):
    # Load the given plist file
    plist_data = load_plist_file(file_name)

    # Remove sensitive PlatformInfo values
    plist_data_updated = remove_platform_values(plist_data)

    # Save the modified plist as a new file
    save_new_plist_file(original_file_name=file_name, plist_data=plist_data_updated)


def main(args):
    global DEBUG

    # Check parsed args
    file_name = args.file if args.file else PLIST_FILE_NAME
    dir_path = args.dir
    DEBUG = args.verbose

    if DEBUG:
        print(f"File name: '{args.file}'")
        print(f"Directory path: '{args.dir}'")
        print(f"Verbose mode: '{args.verbose}'")

    # Enter batch processing mode if given dir path
    if dir_path:
        file_name_lst = list_files(dir_path)
        for file_name in file_name_lst:
            process_plist_file(dir_path + "/" + file_name)

    # Otherwise only process single plist file
    else:
        process_plist_file(file_name)


if __name__ == "__main__":
    # Create the parser
    arg_parser = argparse.ArgumentParser(description="A flag with a value")
    arg_parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="Plist file name",
    )
    arg_parser.add_argument(
        "-d",
        "--dir",
        type=str,
        default=None,
        help="Path of directory with all plist files",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=False,
        help="Verbose mode with debug logs",
    )
    args = arg_parser.parse_args()

    # Execute main logic
    main(args)
