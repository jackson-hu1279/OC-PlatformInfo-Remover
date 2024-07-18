import plistlib

# Read the given plist file
file_name = "Sample.plist"
with open(file_name, "rb") as fp:
    plist_data = plistlib.load(fp)

print(plist_data)
