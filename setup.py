from setuptools import setup, find_packages

setup(
    name = 'freesocks',
    version = '0.1.5',
    license = 'SATA',
    description = 'free way to get through the GFW based on Shadowsocks, just for myself',
    author = 'danlei',
    author_email = 'jne0915@gmail.com',
    url = 'https://github.com/jne0915/freesocks',
    packages = find_packages(),
    install_requires = ['shadowsocks', 'requests'],
    entry_points = """
    [console_scripts]
    freesocks = freesocks.myss:main
    """,
)
