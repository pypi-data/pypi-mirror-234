from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="saludador",
    version="0.0.5",
    description="Paquete de pruebas para subir a PyPi",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/jaimefeldman/saludador",
    author="Jaime Andrés Feldman",
    author_email="jaimefel@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "rich>= 13.5.3",
        "progress>=1.6",
        "requests >=2.31.0",
        "cursor >=1.3.5",
        "readchar >=4.0.5"

    ],

    entry_points={
        'console_scripts': [
            'saluda = saludador.launcher.__main__:main',
        ]
    },
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10"

)
