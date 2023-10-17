from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'SOSPy',
    version = '0.2.1',
    packages = find_packages(),
    install_requires = [
    'numpy', 
    'scipy', 
    'pandas', 
    'sympy',
    'cvxpy'
    ],
    author = 'James Anderson, Leonardo Felipe Toso, Zhe Mo',
    author_email = 'sospypython@gmail.com',
    description = 'Python version of MATLAB SOSTOOLS, a toolbox for sum-of-squares optimization',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/zm2404/SOSPy',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires = '>=3.10',
    keywords='Sum of Square Optimization, SOSTOOLS'
)
    
