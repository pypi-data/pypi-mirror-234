from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["PropBank/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-PropBank-Cy',
    version='1.0.14',
    packages=['PropBank', 'PropBank.data'],
    package_data={'PropBank': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'PropBank.data': ['*.xml']},
    url='https://github.com/StarlangSoftware/TurkishPropbank-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish PropBank',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
