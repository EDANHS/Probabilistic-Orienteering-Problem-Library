from setuptools import setup, find_packages
import platform

# Cargar dependencias desde requirements.txt, ignorando vacíos y comentarios
def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]
    return lines

# Cargar requerimientos base
requirements = parse_requirements("requirements.txt")

# Si estamos en Windows, agregar pywin32 (si es necesario)
if platform.system() == "Windows":
    requirements.append("pywin32>=300")

setup(
    name="probabilistic_orienteering_problem_library",
    version="1.0.0",
    description=(
        "This library provides tools and algorithms to represent orienteering instances "
        "with uncertain rewards or travel times, enabling research and development in "
        "stochastic optimization and routing problems. It includes data structures, "
        "benchmark instances, solvers, and utilities to facilitate experimentation and reproducibility."
    ),
    author="Thomas Molina, Rodrigo Araos, Vicente Mercado",
    author_email="thomas.molina@pucv.cl, rodrigo.araos.q@mail.pucv.cl, vicente.mercado.m@mail.pucv.cl",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
)
