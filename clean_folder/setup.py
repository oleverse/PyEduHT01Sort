from setuptools import setup, find_namespace_packages


setup(name="clean_folder",
      version="1.0.0",
      description="Ordering and cleaning a given folder",
      url="https://github.com/oleverse/PyEduSortTask.git",
      author="Oleksii Petrashov",
      author_email="oleksii.petrashov@gmail.com",
      license="MIT",
      packages=find_namespace_packages(),
      install_requires=[
            "py7zr"
      ],
      entry_points={"console_scripts": ["clean-folder = clean_folder.sort:do_cleaning"]}
      )