from setuptools import Extension, setup

ext = Extension(
    name='webgl2',
    sources=['./webgl2.c'],
)

setup(
    name='webgl2',
    version='0.2.0',
    ext_modules=[ext],
)
