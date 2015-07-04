from setuptools import setup, find_packages


def read(f):
    with open(f) as in_:
        return in_.read()


setup(
    name="game_of_scones",
    version="0.0.1",
    author="FinalInitialSolutions",
    description="Quiz using data sourced from various Government sources",
    license="BSD",
    keywords="quiz abs bottle govhack",
    url="https://hackerspace.govhack.org/content/austat",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=read("requirements.txt").splitlines(),
    tests_require=read('test_requirements.txt').splitlines(),
    setup_requires=['nose>=1.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Bottle",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7"
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'console_scripts':
        ['austat=austat:main.start']
    }
)
