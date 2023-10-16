from setuptools import setup

setup(
    name='FormalMethodsVLSI',
    version='0.0.4',    
    description='VLSI circuits analysis using Formal methods',
    url='https://github.com/SaiCharanMarrivada/FormalMethodsVLSI',
    author='Sai Charan Marrivada',
    author_email='saicharanmarrivada0@gmail.com',
    license='BSD 2-clause',
    packages=['Formal_methods',
              'Formal_methods.SAT',
              'Formal_methods.BDD'],
    install_requires=['z3-solver',
                      'dd',                     
                      'networkx',
                      'tqdm'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
    ],
)

