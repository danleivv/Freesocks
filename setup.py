from setuptools import setup, find_packages

setup(
    name = 'freesocks',
    version = '0.1.0',
    license = 'SATA',
    description = 'free way to get through the GFW based on Shadowsocks, just for myself',
    author = 'danlei',
    author_email = 'jne0915@gmail.com',
    url = 'https://github.com/jne0915/freesocks',
    package = find_packages(),
    install_requires = ['shadowsocks'],
    entry_point = """
    [console_script]
    freesocks = freesocks.myss:main
    """,
)
