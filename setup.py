from setuptools import setup


setup(
    name='flaskage',
    version='0.3',
    url='https://github.com/fgimian/flaskage',
    license='MIT',
    author='Fotis Gimian',
    author_email='fgimiansoftware@gmail.com',
    description=(
        'A complete and carefully designed template for use with the Flask '
        'web framework.'
    ),
    packages=['flaskage'],
    entry_points={
        'console_scripts': [
            'flaskage = flaskage.main:main',
        ]
    },
    zip_safe=False,
    install_requires=[
        'Jinja2>=2.7'
    ],
    setup_requires=[
        'nose',
        'coverage',
        'mock',
        'flake8'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
