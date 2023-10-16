from setuptools import setup, find_packages

META_DATA = dict(
    name="nobi-near-api-py",
    version="0.1.2", # forked_version -> "0.1.0",
    license="MIT",

    author="NEAR Inc",

    url="https://github.com/nobbennob/nobi-near-api-py",# main_repo -> "https://github.com/near/near-api-py",

    packages=find_packages(),

    install_requires=["requests", "base58", "ed25519"]
)

if __name__ == "__main__":
    setup(**META_DATA)
