from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='gerenciamento_mysql',
    version='0.0.1',
    license='MIT License',
    author='George Júnior',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ctt.georgejr@gmail.com',
    keywords='gerenciamento mysql',
    description=u'Gerenciador de MYSQL',
    packages=['gerenciamento_mysql'],
    install_requires=['mysql-connector-python'],)
