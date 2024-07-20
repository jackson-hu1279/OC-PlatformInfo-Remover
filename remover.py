#!/usr/bin/env python3

import argparse
import plistlib

# Define default plist file name to load
PLIST_FILE_NAME = "config.plist"

# Define sensitive keys and replaced value
DEFAULT_VALUE = "**REQUIRED**"
KEYS_TO_REMOVE = ["SystemProductName", "MLB", "SystemSerialNumber", "SystemUUID"]

# Control debug log print
DEBUG = False


def main(args):
    # Check parsed args
    print(f"File name: '{args.file}'")
    print(f"Directory path: '{args.dir}'")
    print(f"Verbose mode: '{args.verbose}'")

    # Read the given plist file
    file_name = args.file if args.file else PLIST_FILE_NAME
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

    # Save the modified plist as a new file
    file_new_name = file_name.split(".")[0] + "_modified.plist"
    with open(file_new_name, "wb") as fp:
        plistlib.dump(plist_data, fp)


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
