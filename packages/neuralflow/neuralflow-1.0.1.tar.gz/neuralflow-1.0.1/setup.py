import setuptools
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='neuralflow',  # module 이름
    version='1.0.1',
    description='Deep learning framework built with numpy (cupy)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sangam Lee',
    author_email='2bhambitious@gmail.com',
    url='https://github.com/augustinLib/neuralflow',
    license='MIT',
    packages=setuptools.find_packages(),
    py_modules=['pymodule'],  # 업로드할 module
    python_requires='>=3.8',  # 파이썬 버전
  # module 필요한 다른 module
    install_requires = [
        "cupy-cuda11x==11.5.0",
        "matplotlib==3.6.3",
        "matplotlib-inline==0.1.6",
        "numpy==1.24.1",
        "packaging==23.0",
        "pandas==1.5.3",
        "pickleshare==0.7.5",
        "Pillow==9.4.0",
        "tqdm==4.64.1"
    ],
    classifiers = [
                      "Programming Language :: Python :: 3",
                      "License :: OSI Approved :: MIT License",
                      "Operating System :: OS Independent"
    ]
)
