from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='xtcalc',
  version='1.2.1',
  author='xsvebmx',
  author_email='m1rza.ismailov@yandex.ru',
  description='Simple calculator',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
)