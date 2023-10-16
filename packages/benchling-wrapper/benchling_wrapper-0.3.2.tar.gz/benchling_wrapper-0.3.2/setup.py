from setuptools import setup, find_packages


setup(
    name='benchling_wrapper',
    version='0.3.2',
    license='MIT',
    author="Ivan Ivanov",
    author_email='300899@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://bitbucket.org/egor-yatsishin/benchling-wrapper',
    keywords='benchling wrapper',
    description='To make integrations with Benchling easier we prepared a wrapper with the most used API functions.',
    install_requires=[
        'oauth2client',
        'oauthlib',
        'benchling-sdk==1.4.1',
        'httpx==0.22.0',
        'pandas==2.1.1'
    ],
    python_requires='>=3.10',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

)
