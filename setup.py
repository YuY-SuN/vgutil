
from setuptools import setup, find_packages

setup(
    name='vgutil',
    version='0.1',
    url='https://github.com/YuY-SuN/vgutil',
    author='YuY-SuN',
    author_email='yusunagawa1987@gmail.com',
    description='collection of wrapper functions designed to simplify the usage of vector Db and Generate AI for personal use.',
    packages=find_packages(),    
    install_requires=['openai', 'chromadb'], # ライブラリの依存関係
)
