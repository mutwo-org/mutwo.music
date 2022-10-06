import setuptools  # type: ignore

version = {}
with open("mutwo/music_version/__init__.py") as fp:
    exec(fp.read(), version)

VERSION = version["VERSION"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extras_require = {
    "testing": ["nose", "coveralls", "mutwo.common>=0.9.0, <1.0.0"]
}

setuptools.setup(
    name="mutwo.music",
    version=VERSION,
    license="GPL",
    description="music extension for event based framework for generative art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Levin Eric Zimmermann",
    author_email="levin.eric.zimmermann@posteo.eu",
    url="https://github.com/mutwo-org/mutwo.ext-music",
    project_urls={"Documentation": "https://mutwo.readthedocs.io/en/latest/"},
    packages=[
        package
        for package in setuptools.find_namespace_packages(
            include=["mutwo.*", "mutwo_third_party.*"]
        )
        if package[:5] != "tests"
    ],
    setup_requires=[],
    install_requires=[
        "mutwo.core>=0.61.2, <0.62.0",
        "phonemizer>=3.1.1, <4.0.0",
        "gradient-free-optimizers>=1.0.7, <2.0.0",
    ],
    extras_require=extras_require,
    python_requires=">=3.9, <4",
)
