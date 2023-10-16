from setuptools import setup, find_packages
 
setup(name='kea_cfdiclient',
      version='0.2',
      url='http://kea.mx/',
      packages=find_packages(exclude=['tests']),	
      license='MIT',
      author='Daniel Hernandez',
      author_email='dhernandez@kea.mx',
      description='Client for CFDI',
      zip_safe=False)
