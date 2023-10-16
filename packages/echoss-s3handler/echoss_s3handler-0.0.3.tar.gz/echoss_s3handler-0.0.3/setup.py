from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = "echoss_s3handler"

setup(
    name='echoss_s3handler',
    version='0.0.3',
    url='',
    requires=['boto3'],
    license='',
    author='incheolshin',
    author_email='incheolshin@12cm.co.kr',
    description='echoss AI Bigdata Solution - S3 handler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['echoss', 'echoss_s3handler', 's3handler', 's3_handler'],
    package_data={},
    python_requires= '>3.7',
)
