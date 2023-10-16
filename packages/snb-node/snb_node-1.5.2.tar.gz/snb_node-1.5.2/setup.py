from setuptools import setup, find_packages
#from Cython.Build import cythonize

# from setuptools import find_packages
# from distutils.core import setup
#print(find_packages())
setup(
    name="snb_node",
    version="1.5.2",
    author="wang xin yi",
    author_email="wangxinyi@smartnotebook.tech",
    description="smart-notebook node",
    url="http://smartnotebook.tech/",
    packages=find_packages(),
    package_data={
        'snb_node':['ascii_logo.txt']
        }
    #ext_modules=cythonize(["./snb_server/**.py"]   )
)