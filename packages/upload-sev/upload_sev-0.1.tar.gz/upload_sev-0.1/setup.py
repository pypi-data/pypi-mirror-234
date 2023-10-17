from setuptools import setup, find_packages

setup(
    name="upload_sev",
    version="0.1",
    packages=find_packages(),
    description="A simple file upload server based on FastAPI",
    author="Geek Ricardo",
    author_email="GeekRicardozzZ@gmail.com",
    url="https://github.com/GeekRicardo/upload_server",  
    install_requires=["fastapi", "uvicorn", "python-multipart"],  
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
