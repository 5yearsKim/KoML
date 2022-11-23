from setuptools import setup, find_packages

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

reqs = parse_requirements('./requirements.txt')
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='koml',
    version='1.0.0',
    author='5yearsKim',
    author_email='hypothesis22@gmail.com',
    url='https://github.com/5yearsKim/KoML',
    project_url='https://pypi.org/project/koml/',
    description='누구나 쉽게 한국어챗봇을 만들 수 있게',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['examples', 'tests', 'brain_pkl', 'korean_rule_helper']),
    install_requires=reqs,
    # package_data={
    #   '': ['data/*']
    # }
)