from setuptools import setup

setup(
    name='python_course_by_ty',
    version='0.1.0',    
    description='A package for testing student answers to project questions.',
    url='https://github.com/TyGriffiths/python_course_by_ty',
    author='Ty Griffiths',
    author_email='griffiths.ty@yahoo.com',
    license='GNU General Public License v3.0',
    packages=['python_course_by_ty'],
    install_requires=['pandas',
                      'numpy',
                      'requests',
                      'bs4',
                      'omdb',
                      ],

    classifiers=[
        'Intended Audience :: Education', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)