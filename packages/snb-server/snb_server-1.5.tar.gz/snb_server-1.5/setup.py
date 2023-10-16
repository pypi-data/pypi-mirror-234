from setuptools import setup, find_packages
#from Cython.Build import cythonize

# from setuptools import find_packages
# from distutils.core import setup
#print(find_packages())
setup(
    name="snb_server",
    version="1.5",
    author="wang xin yi",
    author_email="wangxinyi@smartnotebook.tech",
    description="smart-notebook server",
    url="http://smartnotebook.tech/",
    packages=find_packages(),
    package_data={'pytransform': ['_pytransform.so'],
                  'snb_server':['ascii_logo.txt'],
                  'init_data':['*.*']
                  }

    #ext_modules=cythonize(["./snb_server/**.py"]   )
)