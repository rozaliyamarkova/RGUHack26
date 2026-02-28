

## Setting up

### Chrome extension

Visit chrome://extensions, enable developer mode (top right)

Click Load unpacked, navigate to the repository folder, choose the "chrome-extension" folder and select it.

It should now be in chrome extensions

### Server

From top level do 
```
python3 -m venv venv
```

```
source venv/bin/activate
pip install -r requirements.txt
```