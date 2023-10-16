from setuptools import find_packages, setup


if __name__ == "__main__":
    print("Building wheel...")

    setup(
        name="gddet",
        version="0.1.1",
        author="HY",
        url="https://github.com/IDEA-Research/GroundingDINO",
        description="open-set object detector",
        license="Apache License",
        packages=find_packages(),
    )
