from setuptools import setup, find_packages

setup(
    name='Mensajes-pgrillo-01',
    version='7.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pietro Grillo',
    author_email='hola@pietro.dev',
    url='',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[i.strip() for i in open("requirements.txt").readlines()], #con strip quito los espacios que sobran
    
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ]
)
