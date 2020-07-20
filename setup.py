from setuptools import setup

setup(
    name='pipeline',
    version='0.0.1',
    author='Everton Gago',
    author_email='everton.gjunior@gmail.com',
    license='Private Software',
    packages=['src.deea','src.deea.jobs'],
    namespace_packages=['src', 'src.deea'],
    install_requires=open('requirements.txt').readlines(),
    tests_require=['pytest'],
    zip_safe=False
)
