from setuptools import setup, find_packages

APP_NAME = "pyrateshield"

# will load the __version__ variable
# Update version number in version.py
# https://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
with open('pyrateshield/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            _, _, __version__ = line.replace("'", '').split()
            break

APP_SCRIPT_NAME = "%s.py" % APP_NAME.lower()


# How to publish to pypi
# 0. pip install twine pandoc
# 1. Update pyrateshield/version.py
# 2. Remove build and dist folder (if present)
# 3. Create source distribution: 'python setup.py sdist'
# 4. 'pip install twine' (if not installed)
# 5. Upload to pypi: 'twine upload dist/*'


# How to build  and publish executable
# 1. pip install pyinstaller
# 2. pyinstaller app.spec
# 3. rename executabke to pyrateshield_1-0-4.exe (update 1-0-4 to match version)
# 4. zip the exe
# 5. upload to the downloads section of bitbucket


try:
    # convert to rst to add readme.md to rst since pypi doesnt 
    # support markdown. Images still lacking at pypi atm.
    # https://stackoverflow.com/questions/26737222/how-to-make-pypi-description-markdown-work
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
    
setup(name='pyrateShield',
      python_requires='>=3.8',
      version=__version__, # loaded from version.py see above
      description='Generate radiation-dose maps',
      long_description_content_type='text/markdown',
      long_description=long_description,
      keywords='pyrateShield radiation radiology nuclear medicine',
      url='https://bitbucket.org/MedPhysNL/pyrateShield',
      author='Marcel Segbers, Rob van Rooij',
      author_email='msegbers@gmail.com',
      license='GNU GPLv3',
      packages=find_packages(),

      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pyqt5',
          'pynrrd',
          'pyyaml',
          'scikit-image',
          'imageio',
          'pandas',
          'psutil',
          'xlsxwriter',
          'xlrd',
          'qtawesome',
          'pyperclip'],

      entry_points={
          'console_scripts': ['pyrateshield=pyrateshield.app:main'],
      },
      include_package_data=True,
      zip_safe=False)
