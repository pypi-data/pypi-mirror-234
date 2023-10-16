# Installation and update

There are several ways to install the software.

For Linux/Mac, install the software using the automatic installation
scripts provided (see below).

For Windows, we recommend installing the software using the prepackaged executable (see below).

In addition, we provide a general Python based installation through PIP.

## Releases

All releases are listed under
[Releases](https://gitlab.com/iocbio/gel/-/releases). Releases are
distributed as executables (for Windows) and through The Python Package
Index (PyPI).

## Linux/Mac

To use the automatic installation script for Linux/Mac, first make sure that you have the
latest `pip` installed by running:

```
python3 -m pip install --user --upgrade pip
```

Then, open a terminal and go to the folder where you would like to install the program.
Then, run the following command:

```
curl https://gitlab.com/iocbio/gel/-/raw/main/install.sh | bash
```

or

```
wget -qO - https://gitlab.com/iocbio/gel/-/raw/main/install.sh | bash
```
and run by
```
iocbio-gel/bin/iocbio-gel
```

## Windows

For Windows, there are two ways to install the software. We recommend using the packed executable. However, it is also possible to use the automatic installation script through Python.

### Packed executable

For Windows, we provide an executable that is available under
[Releases](https://gitlab.com/iocbio/gel/-/releases). This is the
recommended way to install in Windows.

To install, select the release under
[Releases](https://gitlab.com/iocbio/gel/-/releases), download Windows
executable packaged as a ZIP. Unpack the ZIP into any location on your PC and
start the application by running `gel.bat` in the extracted folder.

### Installation script

To install IOCBIO Gel software using automatic installation script
make sure that you have Python installed. More information about
installing Python in Windows see [Python for
Beginners](https://docs.microsoft.com/en-us/windows/python/beginners).
In addition, install Microsoft Visual C++ Redistributable for Visual
Studio 2015, 2017 and 2019. Respective installer can be found
[here](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-160).

When Python is installed open PowerShell and make first sure that
[Get-ExecutionPolicy](https://go.microsoft.com/fwlink/?LinkID=135170)
is not Restricted. We suggest using `Bypass` to bypass the policy to
get things installed or `AllSigned` for quite a bit more
security. First, run `Get-ExecutionPolicy` in PowerShell. In case, it
returns `Restricted`, then run `Set-ExecutionPolicy AllSigned` or
`Set-ExecutionPolicy Bypass -Scope Process`.  When this is all set you
can install the program by running following command:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://gitlab.com/iocbio/gel/-/raw/main/install.ps1'))
```


## pip with virtual environment

Sometimes packages for different applications can cause
incompatibilities. To avoid it, you could use virtual environment for
the software installation. To create virtual python environment, run

```
python -m venv iocbio-gel
```

This will create folder `iocbio-gel` and install scripts, such as
`pip`, into it. To use the environment, call `pip` from that folder
and install iocbio-gel dependencies and application into it. It is
recommended to install dependencies using
[requirements.txt](https://gitlab.com/iocbio/gel/-/raw/main/requirements.txt)

```
iocbio-gel/bin/pip install -r requirements.txt
iocbio-gel/bin/pip install iocbio.gel
```
and run by
```
iocbio-gel/bin/iocbio-gel
```

For Windows, adjust the commands above.

### pip

If not available in the system, you can replace `pip3` command
below with `python3 -m pip`.

To install the published version after installation of the
[requirements](https://gitlab.com/iocbio/gel/-/raw/main/requirements.txt),
run

```
pip3 install --user -r requirements.txt
pip3 install --user iocbio.gel
```
This will install all dependencies and it is expected to add a command `iocbio-gel` into your `PATH`.
If the command is missing after installation, check whether the default location
of `pip3` installation is in your path. For Linux, it should be `~/.local/bin`.

Its possible to install from Git repository directly:
```
pip3 install --user git+https://gitlab.com/iocbio/gel
```

For development, use

```
pip3 install --user -e .
```

in the source directory. To install the current version from the source, use

```
pip3 install --user .
```

Note that `--user` is recommended to avoid messing up the system
packages. Keep an eye the dependencies are installed as specified in
the
[requirements](https://gitlab.com/iocbio/gel/-/raw/main/requirements.txt).
