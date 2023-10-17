import setuptools
from setuptools import find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="m2aia",
    version="0.5.1",
    author="Jonas Cordes",
    author_email="j.cordes@hs-mannheim.de",
    description="Provide interfaces for M2aia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://m2aia.github.io/m2aia",
    # cmdclass={'bdist_wheel': bdist_wheel},
    project_urls={
        "Bug Tracker": "https://github.com/m2aia/pym2aia/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Development Status :: 3 - Alpha"
    ],
    packages=find_namespace_packages(where='src'),
    package_dir={"": "src"},
    # include_package_data=True,
    package_data={
        "m2aia.bin": ["*"],
        },
    python_requires=">=3.8",
    install_requires=[
          'wheel',
          'numpy',
          'SimpleITK',
          'wget'
      ],
    
)
