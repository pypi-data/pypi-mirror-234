from setuptools import setup, find_packages

setup(
    name="spanishweather",
    version="0.1.5",
    description="Una aplicación para obtener datos meteorológicos de la AEMET.",
    author="Miguel Blaya",
    author_email="miguel.blaya@gmail.com",
    url="https://github.com/Miguel-bc/spanishweather.git",
    packages=find_packages(),
    install_requires=[
        # Lista de dependencias de tu proyecto
        "requests",
    ],
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)