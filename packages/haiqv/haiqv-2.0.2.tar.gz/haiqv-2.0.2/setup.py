from setuptools import setup, find_packages

setup(
    name='haiqv',
    version='2.0.2',
    description='HAiQV AI Platform SDK for MLOps',
    author='haiqv',
    author_email='haiqv.ai@hanwha.com',    
    install_requires=['requests', 'python-dotenv', 'pyyaml', 'psutil'],
    packages=find_packages(exclude=['.env.develop']),
    include_package_data=True,
    keywords=['haiqv', 'haiqvml'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[        
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
)
