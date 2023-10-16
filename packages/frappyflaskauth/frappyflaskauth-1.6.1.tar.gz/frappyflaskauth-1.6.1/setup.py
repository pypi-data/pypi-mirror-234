from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappyflaskauth",
      version="1.6.1",
      description="Flask endpoints for user management and authentication.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-flask-authentication",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappyflaskauth"
      ],
      install_requires=[
            "flask",
            "pbu>=1.1.4"
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
