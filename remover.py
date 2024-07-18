import plistlib

# Read the given plist file
file_name = "config.plist"
with open(file_name, "rb") as fp:
    plist_data = plistlib.load(fp)

# Retrieve original PlatformInfo values
platforminfo_dict = plist_data["PlatformInfo"]["Generic"]

# Define key names of sensitive info
keys_to_remove = [
    "SystemProductName",
    "MLB",
    "SystemSerialNumber",
    "SystemUUID"
]

# Remove sensitive PlatformInfo values
# Original values will be replaced as "**REQUIRED**"
for key in keys_to_remove:
    if key in platforminfo_dict.keys():
        platforminfo_dict[key] = "**REQUIRED**"

plist_data["PlatformInfo"]["Generic"] = platforminfo_dict

# Save the modified plist as a new file
file_new_name = "config_modified.plist"
with open(file_new_name, "wb") as fp:
    plistlib.dump(plist_data, fp)