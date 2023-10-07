import setuptools
# Each Python project should have pyproject.toml or setup.py
# TODO: Please create pyproject.toml instead of setup.py (delete the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away from needing to generate a setup.py file to enable editable installs - We might able to delete this file in the near future

PACKAGE_NAME = "location_profile_local"
package_dir = PACKAGE_NAME.replace("-", "_")


setuptools.setup(
    name='location-profile-local',
    version='0.0.45',  # https://pypi.org/project/location-profile-local/
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles location-profile-local Local Python",
    long_description="This is a package for sharing common functions of operational hours CRUD to location_profile database used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
    install_requires=[
        'database-without-orm-local>=0.0.78',
        'logger-local>=0.0.46'
    ],
)
