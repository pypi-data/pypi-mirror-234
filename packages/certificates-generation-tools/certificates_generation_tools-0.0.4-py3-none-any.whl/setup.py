import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

KEYWORDS = ('')
DESCRIPTION = ''
CLASSIFIERS = []

requirements = [
    "cryptography",
    "doit",
    "schema",
    'pydantic',
    'pyaml',
    'dacite',
]

requirements_tests = [
    "freezegun",
    "pyopenssl",
]

extras = {
    'tests': requirements_tests,
}

NAME = 'certificates-generation-tools'
MODULE = NAME.replace("-", "_")
setuptools.setup(
    name=NAME,
    version="0.0.4",
    author="LeConTesteur",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/LeConTesteur/{NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/LeConTesteur/{NAME}/issues",
    },
    classifiers=CLASSIFIERS,
    package_dir={NAME: MODULE},
    packages={"": MODULE},
    python_requires=">=3.8",
    install_requires = requirements,
    tests_require = requirements_tests,
    extras_require = extras,
    keywords=KEYWORDS,
    entry_points={
        'console_scripts': [
            'certs-gen-tools = certificates_generation_tools.__main__:main',
        ]
    },
)
