from setuptools import setup, find_packages

project_name = 'mini-spider'
module_name = 'minispider'

setup(
    name='mini-spider',
    version='0.0.1',

    author='ZhangYunHao',
    author_email='workvl@163.com',

    description='Simple way to create your spider.',
    long_description='None.',
    keywords="python spider tool package",

    url='https://github.com/ZYunH/Mini-Spider',
    license='MIT Licence',
    platforms='any',

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'mini-spider = minispider.__main__:main'
        ]
    }

)
