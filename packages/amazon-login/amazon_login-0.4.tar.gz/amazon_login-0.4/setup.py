from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open("requirements.txt", "r", encoding="utf-16") as f:
    requirements = f.read().splitlines()


setup(
    name="amazon_login",
    version="0.4",
    packages=find_packages(),
    include_package_data=True,
    url="http://danielguardado.com",
    python_requires=">=3.9",
    license="MIT",
    author="Daniel Guardado",
    author_email="danguardado217@gmail.com",
    description="Log into amazon seller central or vendor central using selenium.",
    install_requires=requirements,
    classifiers=[
        # these specify the development status, audience, and license of your package
        # see this for more classifiers: https://pypi.org/classifiers/
    ],
)
