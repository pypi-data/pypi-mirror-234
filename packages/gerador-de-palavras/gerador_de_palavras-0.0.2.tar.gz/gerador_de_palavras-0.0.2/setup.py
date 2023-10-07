from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='gerador_de_palavras',
    version='0.0.2',
    url='',
    license='MIT License',
    author='Let lima',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lwtferr@gmail.com',
    keywords='Pacote',
    description='Pacote python para gerar palavras aleatórias',
    packages=['gerador', 'base'],
    install_requires=['numpy'],)