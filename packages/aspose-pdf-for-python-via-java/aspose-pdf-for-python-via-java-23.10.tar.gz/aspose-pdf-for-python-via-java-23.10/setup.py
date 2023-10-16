from setuptools import setup

NAME = "aspose-pdf-for-python-via-java"
VERSION = "23.10"
REQUIRES = ["JPype1==1.4.1"]

setup(
    name=NAME,
    version=VERSION,
    author="Aspose",
    description="PDF generation and recognition component. It allows developers to quickly and easily work with creation, edit and conversion functionality to their Python applications.",
    author_email="marat.khazin@aspose.com",
    keywords=["aspose", "pdf", "java"],
    install_requires=REQUIRES,
    packages=['asposepdf'],
    include_package_data=True,
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: Other/Proprietary License'
    ],
    python_requires='>=3.6',
)