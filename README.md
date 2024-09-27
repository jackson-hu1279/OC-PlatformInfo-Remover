# OC-PlatformInfo-Remover

This script is designed to remove platform SMBIOS information such as serial number in the [OpenCore](https://dortania.github.io/OpenCore-Install-Guide/) `config.plist` file so that your config can be easily shared with the whole Hackintosh community without revealing your own SMBIOS details for security concerns.

## ⭐ Key Features

After executing the script on the plist file, the following entry values under `PlatformInfo -> Generic` will be replaced with a default placeholder value = `"**REQUIRED**"`. The result will be saved as `xxx_modified.plist` in the same directory.

```
PlatformInfo
└── Generic
    ├── SystemProductName
    ├── SystemSerialNumber
    ├── MLB
    └── SystemUUID
```

## ⚙️ Usage

### Single File Mode

Single file mode will only process the given file, specified with `-f` flag.

```
python remover.py -f <file_name>.plist
```

### Batch Mode

Batch mode will process all plist files within a given directory, specified with `-d` flag.

```
python remover.py -d <dir_path>
```

### Verbose Mode (Optional)

Verbose mode enables additional debug prints if `-v` flag is present.

```
python remover.py -f <file_name>.plist -v
```

## 📝 Notes

For setting up the SMBIOS information, you may use CorpNewt's [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) application to generate a set of SMBIOS details like below:

```
#######################################################
#               iMac20,1 SMBIOS Info                  #
#######################################################

Type:         iMac20,1
Serial:       C02XG0FDH7JY
Board Serial: C02839303QXH69FJA
SmUUID:       DBB364D6-44B2-4A02-B922-AB4396F16DA8
```

For more details about configuring SMBIOS details in `config.plist`, please refer to [OpenCore's Install Guide](https://dortania.github.io/OpenCore-Install-Guide/config.plist/comet-lake.html#platforminfo).
