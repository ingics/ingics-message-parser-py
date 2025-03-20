### Bluepy (Bluetooth LE interface for Python)
[https://ianharvey.github.io/bluepy-doc/]

Install library which bluepy required
```
sudo apt install libglib2.0-dev
```

Suggest to create Python virtual env for test
```
pip -m venv .venv
. .venv/bin/active
```

Install bluepy package
```
pip install bluepy
```

### Set Permission for non-Root User for Bluepy
If you install the bluepy in global mode and plan to test the script as Root. You can skip this section.

Install necessary tool
```
sudo apt-get install libcap2-bin
```

Set bluepy-helper has permission to run.
```
sudo setcap 'cap_net_raw,cap_net_admin+eip' `find .venv -name bluepy-helper`
```

### Install Parser
Install parser package from GitHub
```
pip install git+https://github.com/ingics/ingics-message-parser-py
```

### Run example
Modify the iBSXX MAC addresses in scan.py, then
```
sudo python scan.py
```

