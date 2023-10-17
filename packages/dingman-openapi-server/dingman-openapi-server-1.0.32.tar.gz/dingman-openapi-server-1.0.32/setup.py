import setuptools

api_version_file = "openapi_version"
api_version = "1.0.0"

try:
    with open(api_version_file, 'r') as f:
        val = f.readline().split()
        api_version = ".".join(val)
except OSError:
    print('openapi version file not found')

openapi_modules = setuptools.find_packages("openapi_server")
# provide full path for the modules
openapi_modules = ["openapi_server." + module for module in openapi_modules]
openapi_modules.append("openapi_server")
print(f"setup.py modules to upload: {openapi_modules}")

setuptools.setup(
    name="dingman-openapi-server",
    version=api_version,
    author="BD Data Sys IE CDN",
    description="CDN DMS Open API",
    url="https://code.byted.org/savanna/dingman_api_server",
    packages=openapi_modules,
    include_package_data=True,
    python_requires=">=3.7",
    install_requires = [
        "flask",
        "Flask-Testing"
    ],
)