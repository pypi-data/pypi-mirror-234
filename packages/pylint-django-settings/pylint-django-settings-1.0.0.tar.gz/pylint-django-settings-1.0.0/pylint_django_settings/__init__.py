import setuptools

INSTALLED_APPS = list(filter(lambda p:'.' not in p,setuptools.find_packages()))

