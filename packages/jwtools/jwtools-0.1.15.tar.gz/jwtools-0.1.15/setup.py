from setuptools import setup, find_packages

setup(
    name='jwtools',
    version='0.1.15',
    description="It is a micro-toolbox that includes various common operations and will continue to be improved in the future.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='jinghewang',
    author_email='jinghewang@163.com',
    license='MIT License',
    url=' https://gitee.com/jiwei-data/python-jwtools.git',
    packages=find_packages(),
    excluded_packages=['tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[''],
    entry_points={
        'console_scripts': [''],
    },

)
