from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gis-points-extractor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern web application for advanced geospatial analysis that extracts points within polygon boundaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gis-points-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=3.8",
            "black>=21.0",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gis-points-extractor=web_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*", "static/*"],
    },
    keywords="gis, geospatial, points, polygons, analysis, flask, geopandas",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gis-points-extractor/issues",
        "Source": "https://github.com/yourusername/gis-points-extractor",
        "Documentation": "https://github.com/yourusername/gis-points-extractor#readme",
    },
) 