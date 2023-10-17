import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="midlife",
    version="0.0.7",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="impact of COVID-19 on mortality of midlife",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/midlife",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/midlife",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['midlife'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'midlife = midlife:main'
        ]
    },
)
