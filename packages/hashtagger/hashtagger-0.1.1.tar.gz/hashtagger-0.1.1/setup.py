from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9',
  'Programming Language :: Python :: 3.10',
  'Programming Language :: Python :: 3.11',
  'Programming Language :: Python :: 3.12',  # Hypothetical future version
]
 
setup(
  name='hashtagger',
  version='0.1.1',
  description='A hashtag generator using tensorflow and nltk',
  long_description = (open('README.rst').read() + '\n\n' +
                   open('CHANGELOG.txt').read()),
  
  url='',  
  author='Meet Jethwa',
  author_email='meetjethwa3@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='tagger', 
  packages=find_packages(),
  install_requires=[
        "opencv-python",
        "numpy",
        "tensorflow",
        "nltk",
    ] 
)
