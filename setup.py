import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='lodestone_parser',  
     version='0.0.1',
     author="Ralph Pineda",
     author_email="ralph.pineda@gmail.com",
     description="Parses FFXIV lodestone information",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cleargelnotes/ffxiv-lodestone-parser-py",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
