from setuptools import setup, find_packages

setup(
    name="vectorview",
    version="0.8",
    packages=find_packages(),
    install_requires=[],
    author="Vectorview",
    author_email="lukas@vectorview.ai",
    description="Vector database monitoring and analytics",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vectorview/vectorview_py",
)
