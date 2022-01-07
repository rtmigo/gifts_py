from pathlib import Path

from setuptools import setup, find_packages


def load_module_dict(filename: str) -> dict:
    import importlib.util as ilu
    filename = str(Path(__file__).parent / filename)
    spec = ilu.spec_from_file_location('', filename)
    module = ilu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__dict__


name = "gifts"

setup(
    name=name,
    version='0.0.0',
    author="Artёm IG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/gifts_py#readme',

    python_requires='>=3.7',
    install_requires=[],
    packages=['gifts'],


    description="",

    keywords="".split(),

    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
    ])
