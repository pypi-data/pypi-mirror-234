from setuptools import setup, find_packages

setup(name='hivesda', # 패키지 명

version='0.0.3.2',

description='Test Package',

author='Jae',

author_email='jjkjy@nate.com',

url='',

license='MIT', # MIT에서 정한 표준 라이센스 따른다

python_requires='>=3',

install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

packages=['hivesda','hivesda/datasets','hivesda/engines','hivesda/losses','hivesda/models','hivesda/utils'] # 패키지가 들어있는 폴더들

)