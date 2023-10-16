from setuptools import setup


setup(
    name="hotreloader",
    packages=["."],
    requires=["pandas", "numpy", "pydantic"],
    
    version="0.2.0",
    description="A hot-reload framework can watch files and handle it when file is edited.",
    url="https://github.com/fswair/PyReloader",
    author="Mert Sırakaya",
    author_email="usirakaya@ogr.iu.edu.tr",
    keywords=["hot-reload", "file-watching", "reloader"],
    classifiers=[]
)