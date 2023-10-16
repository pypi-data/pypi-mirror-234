import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hscan",
    version="3.0.2",
    author="jyanghe",
    author_email="jyanghe1023@gmail.com",
    description="A python framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jyangHe/hscan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.0',
    install_requires=[
        'httpx[http2]==0.24.1',
        'aiofiles==0.7.0',
        'aio-pika==6.8.0',
        'beautifulsoup4==4.9.3',
        'aioredis==2.0.0',
        'motor==2.5.1',
        'Brotli==1.0.9',
        'pymongo==3.12.0',
        'chardet==4.0.0',
        'asyncpg==0.26.0',
        'aiokafka==0.8.0',
        'oss2==2.15.0',
        'boto3==1.28.29',
        'aiomysql==0.1.1',
        'curl-cffi==0.5.9'
    ]
)
