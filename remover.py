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


# Helper function to handle errors
def handle_error(error_print, error_details=None):
    print(error_print)
    if DEBUG and error_details:
        print(f"Error message: {error_details}")
    exit(-1)


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
        handle_error(f"Error: Directory '{directory}' does not exist")
    except PermissionError:
        handle_error(f"Error: Permission denied to access the directory '{directory}'")
    except Exception as e:
        handle_error(f"An error occurred when listing files in '{directory}'", e)


# Load the given plist file
def load_plist_file(file_name):
    try:
        with open(file_name, "rb") as fp:
            plist_data = plistlib.load(fp)
    except FileNotFoundError:
        handle_error(f"Error: Cannot find the file '{file_name}'")
    except Exception as e:
        handle_error(f"An error occurred when loading the file '{file_name}'", e)

    return plist_data


# Save plist data as a new file
def save_new_plist_file(original_file_name, plist_data):
    file_new_name = original_file_name.split(".")[0] + "_modified.plist"

    try:
        with open(file_new_name, "wb") as fp:
            plistlib.dump(plist_data, fp)
            if DEBUG:
                print(f"Modified file saved as '{file_new_name}'")
    except Exception as e:
        handle_error(f"An error occurred when saving the file '{file_new_name}'", e)


# Remove sensitive PlatformInfo values
def remove_platform_values(plist_data):
    # Retrieve original PlatformInfo values
    platforminfo_dict = plist_data["PlatformInfo"]["Generic"]

    # Remove sensitive PlatformInfo values
    # Original values will be replaced with default value
    for key in KEYS_TO_REMOVE:
        if key in platforminfo_dict.keys():
            platforminfo_dict[key] = DEFAULT_VALUE

    plist_data["PlatformInfo"]["Generic"] = platforminfo_dict
    plist_data_updated = plist_data

    return plist_data_updated


# Process a single plist file
def process_plist_file(file_name):
    if DEBUG:
        print("=== Processing ===")
        print(f"Processing file: {file_name}")

    # Load the given plist file
    plist_data = load_plist_file(file_name)

    # Remove sensitive PlatformInfo values
    plist_data_updated = remove_platform_values(plist_data)

    # Save the modified plist as a new file
    save_new_plist_file(original_file_name=file_name, plist_data=plist_data_updated)


# Execution of main logic
def main(args):
    global DEBUG

    # Check parsed args
    file_name = args.file if args.file else PLIST_FILE_NAME
    dir_path = args.dir
    DEBUG = args.verbose

    if DEBUG:
        print("====== Args ======")
        print(f"Args - File name: '{args.file}'")
        print(f"Args - Directory path: '{args.dir}'")
        print(f"Args - Verbose mode: '{args.verbose}'")

    # Enter batch processing mode if given dir path
    if dir_path:
        if DEBUG:
            print("=== Batch Mode ===")
        file_name_lst = list_files(dir_path)
        for file_name in file_name_lst:
            process_plist_file(dir_path + "/" + file_name)

    # Otherwise only process single plist file
    else:
        process_plist_file(file_name)


if __name__ == "__main__":
    # Define the argument parser
    arg_parser = argparse.ArgumentParser(description="A script to remove sensitive PlatformInfo values in OC config files")
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
        action="store_true",
        help="Verbose mode with debug logs",
    )
    args = arg_parser.parse_args()

    # Execute main logic
    main(args)
