# Mac-amd-info 
Simple tool that report human readable informations about macOS supported AMD GPU's

## Requirements
* python2.7
* beautifulsoup4, lxml and requests
```bash
sudo pip install beautifulsoup4 lxml requests
```

If you don't have pip available:
```bash
sudo easy_install pip
sudo pip install beautifulsoup4 lxml requests
```
* command line developer tools
```bash
xcode-select --install
```

## Usage
* open terminal 
```bash
cd /path/to/Mac-amd-info
./mac_amd_info.py
```

* optional arguments
```bash
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  --output [FILENAME]   write output to file, default is output.md
  -f FILTERS [FILTERS ...], --filter FILTERS [FILTERS ...]
                        show kexts matching a python regex pattern, -f 2.00 shows only 2*00 series controllers
  -l                    show Legacy kexts
  -c                    show Controllers kexts
  -g                    show Graphic Accelerators kexts
  -s                    show HW Services kexts
```
* Filter examples
```bash
# show 95**Controller.kext, AMDRadeonX4000.kext and AMDRadeonX4100.kext
./mac_amd_info.py -c -g -f 95..Controller RadeonX4[0-1]00

# show AMD7000Controller.kext 
./mac_amd_info.py -f 7000
```

## Output

See [`output.md`][output.md]

[output.md]: data/output.md
