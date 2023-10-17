from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as fr:
    return fr.read()

setup(
  name='log_wizard',
  version='1.1.0',
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  author='izharus',
  author_email='ruslan.izhakovskij@gmail.com',
  description='Siple logging for porject with multiple modules',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/izharus/log_wizard',
  install_requires=[],
  keywords='python logging',
  project_urls={},
  python_requires='>=3'
)