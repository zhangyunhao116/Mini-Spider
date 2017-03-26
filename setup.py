from setuptools import setup, find_packages

project_name = 'mini-spider'
module_name = 'minispider'

setup(
    name='mini-spider',
    version='0.0.1',

    author='ZYunH',
    author_email='workvl@163.com',

    description='Simple way to create your spider.',
    long_description='None.',

    url='https://github.com/ZYunH/Mini-Spider',
    license='MIT Licence',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'mini-spider = minispider:main'
        ]
    }

)
