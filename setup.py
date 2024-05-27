from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='compare_packages',
      version='0.1',
      description='Solution the test task',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3.9',
      ],
      url='https://github.com/berg96/rdb_altlinux_testtask_bazalt',
      author='Berg1005',
      author_email='chigar2010@yandex.ru',
      packages=['mymodule'],
      install_requires=[
          'aiohttp',
          'SQLAlchemy',
          'tqdm',
      ],
      entry_points={
          'console_scripts': ['compare_packages=mymodule.compare_packages:main'],
      })
