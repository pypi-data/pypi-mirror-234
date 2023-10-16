from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='pgstoragelogger',
  version='1.0',
  author='le.kazankin',
  author_email='lkazankin@yandex.ru',
  description='Like Python logger, but partiotioned PostgreSQL tables are used for saving.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/le-kazankin/PGStorageLogger',
  packages=find_packages(),
  install_requires=['psycopg2-binary>=2.9.8'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='logging python logger postgres pgsql postgresql logs log',
  project_urls={
    'GitHub Readme': 'https://github.com/le-kazankin/PGStorageLogger/blob/main/README.md',
    'example':'https://github.com/le-kazankin/PGStorageLogger/blob/main/example/example.py'
  },
  python_requires='>=3.6'
)