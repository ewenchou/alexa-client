from setuptools import setup

setup(name='alexa_client',
      version='0.5',
      description="Python client for Amazon's Alexa Voice Service",
      url='',
      author='Ewen Chou',
      author_email='ewenchou@gmail.com',
      license='Apache 2.0',
      packages=['alexa_client'],
      install_requires=['requests_futures'],
      zip_safe=False)
