from setuptools import setup, find_packages
import os
import io

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

with open('src/swmonkey/main.py', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'")
            break

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

print('version: ', version)
setup(
    name='swmonkey',
    version=version,
    packages=find_packages(where='src'),
    author='Li Saifei',
    author_email='waltermitty121906@gmail.com',
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='A tool for monkey test on Linux GUI',
    entry_points={
        'console_scripts': [
            'swmonkey = swmonkey.main:swmonkey',
            'swmonkey_runner = swmonkey.runner:main'
        ]
    },
    install_requires=[
        'pyautogui',
        'psutil',
        'pywinctl'
    ]
)
