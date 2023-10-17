# Sound Designer Wireless Demo

This repository contains a Python-based wireless demo app using the Sound Designer SDK on Windows. It uses the amazing [Textual](https://textual.textualize.io/) framework to provide a console-based GUI.

# Installation

The easiest and cleanest way to install this demo is with [pipx](https://pypa.github.io/pipx/):

`pipx install sd-wireless-demo`

You can also install with pip (but it will install a bunch of dependencies directly into your Python environment):

`pip install sd-wireless-demo`

Either way, you will now have a `wireless_demo` command on your path, which you can run in a terminal:

```
$ wireless_demo -h
usage: wireless_demo [-h] [--sdk-root SDK_ROOT] [--noahlink-driver-path NOAHLINK_DRIVER_PATH] [--programmer {RSL10,NOAHLink}] [--com-port COM_PORT] [--debug] [--delete-bonds]

options:
  -h, --help            show this help message and exit
  --sdk-root SDK_ROOT   Path to the Sound Designer SDK root folder (or set "SD_SDK_ROOT" in your environment)
  --noahlink-driver-path NOAHLINK_DRIVER_PATH
                        Path to the NOAHLink Wireless drivers (when using NOAHLink wireless)
  --programmer {RSL10,NOAHLink}
                        The type of wireless programmer to use
  --com-port COM_PORT   The COM port to use when using the RSL10 dongle
  --debug               Log additional debug information to app_debug.log
  --delete-bonds        Delete the bond table in the wireless programmer
```

# Usage

This demo requires the Sound Designer SDK, which you can point to via the `--sdk-root` command line argument. It also requires a wireless programmer. Currently supported devices are the RSL10 dongle from [onsemi](https://onsemi.com), or the NOAHLink Wireless.

Here is an example of what it looks like when connected to a pair of binaural hearing aids:

![image](https://user-images.githubusercontent.com/131784346/236912316-75bde160-c14f-46ad-a679-74a2bedf73ee.png)
