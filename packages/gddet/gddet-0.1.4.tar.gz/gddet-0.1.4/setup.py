# ENV: samlabel
from setuptools import find_packages, setup


if __name__ == "__main__":
    print("Building wheel...")

    setup(
        name="gddet",
        version='0.1.4',
        author="H-AI",
        url="https://github.com/IDEA-Research/GroundingDINO",
        description="open-set object detector",
        license="Apache License V2.0",
        packages=find_packages(),
    )
