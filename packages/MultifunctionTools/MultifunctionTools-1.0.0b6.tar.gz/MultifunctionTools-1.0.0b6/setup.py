from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'MultifunctionTools',         # How you named your package folder (MyLib)
  packages = ['MultifunctionTools', 'MultifunctionTools.Cipher', 'MultifunctionTools.Convert', 'MultifunctionTools.Exceptions', 'MultifunctionTools.Hash'],
  version = '1.0.0b6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The MultifunctionTools library is a comprehensive collection of handy utilities and tools designed to enhance your Python coding experience.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'veHRz',                   # Type in your name
  author_email = 'vehrzyt@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/veHRz/MultifunctionTools',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/veHRz/MultifunctionTools/archive/refs/tags/1.0.0b6.tar.gz',
  keywords = ['TOOLS', 'CIPHER', 'HASH', 'CONVERT', 'MULTI-USAGE', 'MULTI'],   # Keywords that define your package best
  install_requires=[
          'pycryptodomex',
          'cryptography',
          'argon2-cffi',
          'pillow'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
    'Topic :: Other/Nonlisted Topic',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3 :: Only',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13'
  ],
)