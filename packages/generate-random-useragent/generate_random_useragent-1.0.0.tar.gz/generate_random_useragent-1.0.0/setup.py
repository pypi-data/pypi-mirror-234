from setuptools import setup, find_packages

setup(
    name='generate_random_useragent',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/yanteams/generate_random_ua',
    license='',
    author='Jasson Nguyen',
    author_email='admin@taocuaba.com',
    description='Random Useragent',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 4 - Beta',
         'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
                'Programming Language :: Python'
    ],
    keywords=['Generate Random Useragent', 'generate_random_ua_yan']
)