import requests
import setuptools
import sys, os
dev_pkg_name = "dingman-openapi-server-dev"
dev_version_file = "openapi_version_dev"
data = requests.get(f"https://pypi.org/pypi/{dev_pkg_name}/json").json()
latest_version = [1, 0, 0]
for version in data["releases"]:
    version_lst = [int(num) for num in version.split(".")]
    if version_lst > latest_version:
        latest_version = version_lst
new_version = latest_version
new_version[2] += 1
new_version = [str(num) for num in new_version]
with open(dev_version_file, "w") as version_file:
    version_file.write(" ".join(new_version))
new_version = ".".join(new_version)
openapi_modules = setuptools.find_packages("openapi_server")
# provide full path for the modules
openapi_modules = ["openapi_server." + module for module in openapi_modules]
openapi_modules.append("openapi_server")
# to protect the version number printed as the program output
sys.stdout = open(os.devnull, 'w')
setuptools.setup(
    name=dev_pkg_name,
    version=new_version,
    author="BD Data Sys IE CDN",
    author_email = "jiale.ning1@bytedance.com",
    description="CDN openapi development package for testing",
    url="https://code.byted.org/savanna/dingman_api_server",
    packages=openapi_modules,
    include_package_data=True,
    python_requires=">=3.7",
    install_requires = [
        "flask",
        "Flask-Testing"
    ],
)
sys.stdout = sys.__stdout__
print(new_version)