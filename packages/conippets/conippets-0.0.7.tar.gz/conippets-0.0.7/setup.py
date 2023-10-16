from setuptools import setup, find_packages

setup(
    name = 'conippets',
    packages = find_packages(exclude=['examples']),
    version = '0.0.7',
    license='MIT',
    description = 'conippets',
    author = 'JiauZhang',
    author_email = 'jiauzhang@163.com',
    url = 'https://github.com/JiauZhang/conippets',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = 'text/markdown',
    keywords = [
    ],
    install_requires=[
        'lxml',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires=">=3.8",
)