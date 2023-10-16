import setuptools

with open("README.md", "r") as fh:
    long_description = None

setuptools.setup(
    name="easy-kubeflow",  # Replace with your own name
    version="0.1.2",
    author="CrazyBean",
    author_email="liuweibin@stonewise.cn",
    description="sdk help users for a better use of kubeflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.stonewise.cn/mlsys/easy-kubeflow.git",
    install_requires=[
        'docker>=4.2.1',
        'kfp==1.3.0',
        'pandas>=1.1.5',
        'tqdm>=4.56.0',
        'simplejson>=3.17.5'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
