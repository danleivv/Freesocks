# Freesocks

A free way to get through the GFW based on Shadowsocks.<br>
Thanks to the trial accounts on [socks163.com](http://socks163.com/), who seems not happy T_T<br>
Special thanks to SHADOWSOCKS.

## Installation
```bash
python setup.py install
```

## Usage
```bash
freesocks [OPTION]...
```

Options:
```
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -l LOCAL_PORT  local binding port, default: 1080
  -t TIMEOUT     timeout in seconds, default: 300
```
Freesocks launches a socks5 agent on a local port.

## License

Freesocks uses [SATA License](LICENSE.txt) (Star And Thank Author License) by [zTrix](https://github.com/zTrix), so you have to star this project before using. Read the [license](LICENSE.txt) carefully.

## Update Info

### 0.1.5
* remove `-r` option
* fix severe bugs
* use free account on [socks163.com](http://socks163.com/)

### 0.1.4
* use free account on [ishadowsocks.com](http://www.ishadowsocks.com/)
* test the proxy and reconnect automatically when 'Broken Pipe' occurs in every 5 sec

### 0.1.3
* add option parser
* use args in command line when invoking `sslocal` instead of making json file
* customized refresh interval is supported

### 0.1.2
* add exception handler to reconnect automatically when network interrupts.
* change the license to SATA

### 0.1.1
* fix some bugs and add entry point in script

### 0.1.0
* primary post
