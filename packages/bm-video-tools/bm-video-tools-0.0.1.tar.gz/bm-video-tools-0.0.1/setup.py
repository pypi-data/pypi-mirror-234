import setuptools

with open("README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

setuptools.setup(
    name="bm-video-tools",
    version="0.0.1",
    author="galaxyeye",
    author_email="xieshengpeng@galaxyeye-tech.com",
    description="音频处理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)
