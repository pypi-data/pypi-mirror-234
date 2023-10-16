# Download Latest

`download-latest` requires [Python >=3.7](https://www.python.org/downloads/).
[cURL](https://curl.se/download.html) will also be used if available.

## Install Guide

Instructions for installing cURL, Python 3 and Pip.

### Debian / Ubuntu

```sh
sudo apt update
sudo apt install -y curl python3 python3-pip
```

### Fedora / RHEL

```sh
sudo dnf install -y curl python3 python3-pip
```

### Arch

```sh
sudo pacman -Syy
sudo pacman -Su --needed --noconfirm curl python python-pip
```

### Alpine

```sh
sudo apk add curl python3 py3-pip
```

### FreeBSD

```sh
pkg install -y curl python3
pkg install -xy '^py3.+-pip$'
```

### OpenBSD

```sh
doas pkg_add -z curl python3 py3-pip
```
