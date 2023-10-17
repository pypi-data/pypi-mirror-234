from setuptools import setup

setup(
    name='dansplotcore',
    version='5.4.0',
    description='low-latency interactive plots',
    long_description="Dan's Plot Core is a minimal library that adds plots with low-latency interactivity to Python.",
    url='http://github.com/dansgithubuser/dansplotcore',
    author='danspypiuser',
    author_email='dansonlinepresence@gmail.com',
    license='MIT',
    packages=['dansplotcore'],
    install_requires=[
        'pyglet>=1.5,<2',
    ],
)
