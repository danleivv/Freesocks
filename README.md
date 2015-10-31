# Freesocks (under building)

A free way to get through the GFW based on Shadowsocks.<br>
Thanks to the trial accounts on [socks163.com](http://www.socks163.com/).<br>
Special thanks to SHADOWSOCKS.

## Installation
```bash
python setup.py install
```

## Usage
```bash
freesocks [<local_port>]
```
Freesocks launches a socks5 agent on a local port (1080 for default).

## License

Freesocks uses [SATA License](LICENSE.txt) (Star And Thank Author License) by [zTrix](https://github.com/zTrix), so you have to star this project before using. Read the [license](LICENSE.txt) carefully.

## Update Info

### 0.1.3
* add option parser
* use args in command line when invoking `sslocal` instead of making json file

### 0.1.2
* add exception handler to reconnect automatically when network interrupts.
* change the license to SATA

### 0.1.1
* fix some bugs and add entry point in script

### 0.1.0
* primary post
