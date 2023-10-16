import setuptools

# PRODUCTION setup.py: name, version, install_requires, packages only
with open('requirements.txt', encoding="utf-8") as file:
    install_requires = file.read().splitlines()
setuptools.setup(
    name='django-command-queue',
    version='1.0.1',
    install_requires=install_requires,
    packages=setuptools.find_packages()
)
