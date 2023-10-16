from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='muiscaenergy_comun',
        version='0.0.5',
        url='https://pypi.org/project/',
        author='Jairo Hernando Cervantes Garcia',
        emai='muiscaenergy@gmail.com',
        description='common functions for muiscaenergy projects',
        license='MIT license',
        long_description=open('README.md', 'r').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        classifiers=['Development Status :: 1 - Planning',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Programming Language :: Python :: 3.8',
                     ],
        zip_safe=False,
        install_requires=['timezonefinder >= 6.2.0',
                          'pandas >= 1.5.3',
                          ],
        extras_require={
            'dev': ["pytest >= 7.0",
                    "twine >= 4.0.2",
                    ],
        },
        python_requires='>=3.10',
    )
