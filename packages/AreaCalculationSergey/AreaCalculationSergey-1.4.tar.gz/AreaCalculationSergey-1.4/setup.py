from setuptools import setup

def readme():
  with open('readme.md', 'r') as f:
    return f.read()

setup(name='AreaCalculationSergey',
      version='1.4',
      description='Area calculation of diferent figures.',
      # long_description=readme(),
      long_description_content_type='text/markdown',
      packages=['AreaCalculationSergey'],
      author_email='worldad20@gmail.com',
      zip_safe=False)

