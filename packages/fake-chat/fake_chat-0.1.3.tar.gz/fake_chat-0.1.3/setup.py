from setuptools import setup

from src.fake_chat import __version__

URL = 'https://github.com/Aurorax-own/fake_chat'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fake_chat',
    version=__version__,
    packages=['src.fake_chat'],
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Aurorax-own',
    author_email='15047150695@163.com',
    include_package_data=True,
    install_requires=[
        'pandora-chatgpt==1.3.0',
        'requests==2.31.0'
    ],
    project_urls={
        'Source': URL,
        'Tracker': f'{URL}/issues',
    },
)
