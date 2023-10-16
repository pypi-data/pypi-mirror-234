from setuptools import setup

setup(
    name='yeref',
    version='0.5.37',
    description='desc-f',
    author='john smith',
    packages=['yeref'],
    # install_requires=[
    #       "httplib2>=0.20.4",
    #       "moviepy>=1.0.3",
    #       "Pillow>=9.2.0",
    #       "aiogram>=2.22.1",
    #       "loguru>=0.6.0",
    #       "oauth2client>=4.1.3",
    #       "google-api-python-client>=2.61.0",
    #       "telegraph>=2.1.0",
    #       "setuptools>=65.3.0",
    # ]
)

# region misc
# from distutils.core import setup
# from setuptools import setup, find_packages
# setup(
#       name='yeref',
#       version='0.0.1',
#       description='desc-f',
#       author='john smith',
#       py_modules=['yeref'],
#       packages=find_packages(),
#       scripts=['yeref.py']
# )
#
# python setup.py sdist
# python setup.py install
# python setup.py develop
#
# python setup.py bdist_wheel
# pypi-
# python -m build; twine upload --username fsitner.ya --password c dist/* ; python3 -m pip install --upgrade yeref ; python3 -m pip install --upgrade yeref
# twine upload --repository PROJECT_NAME --username __token__ --password pypi- dist/*
# twine upload dist/*
# endregion

# python -m build; twine upload --repository yeref dist/*; python3 -m pip install --upgrade yeref ; python3 -m pip install --upgrade yeref
# python3 -m pip install --upgrade yeref

# python3 -m pip install --force-reinstall /Users/mark/PycharmProjects/AUTOBOT/yeref/dist/yeref-0.1.99-py3-none-any.whl
# pip install --force-reinstall -v "yeref==0.1.30"
# pip install --force-reinstall -v "pydantic[dotenv]==1.10.12"
# pip install aiogram==3.0.0b8
# pip install https://github.com/aiogram/aiogram/archive/refs/heads/dev-3.x.zip
# pip show aiogram
# ARCHFLAGS="-arch x86_64" pip install pycurl
