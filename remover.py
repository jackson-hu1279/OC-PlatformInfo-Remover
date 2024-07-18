import plistlib

# Read the given plist file
file_name = "config.plist"
with open(file_name, "rb") as fp:
    plist_data = plistlib.load(fp)

# Retrieve original PlatformInfo values
platforminfo_dict = plist_data["PlatformInfo"]["Generic"]
print(platforminfo_dict)

# Define key names of sensitive info
keys_to_remove = [
    "SystemProductName",
    "MLB",
    "SystemSerialNumber",
    "SystemUUID"
]
