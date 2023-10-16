from setuptools import setup, find_packages
import version

setup(
    name="support-toolbox",
    version=version.__version__,
    description="A suite of CLI tools for the data.world support team",
    author="Jack Compton",
    author_email="jack.compton@data.world",
    url="https://github.com/datadotworld/support-toolbox/tree/main",
    packages=find_packages(),
    install_requires=[
        "certifi==2023.7.22",
        "charset-normalizer==3.2.0",
        "defusedxml==0.7.1",
        "idna==3.4",
        "jira==3.5.2",
        "oauthlib==3.2.2",
        "packaging==23.1",
        "requests==2.31.0",
        "requests-oauthlib==1.3.1",
        "requests-toolbelt==1.0.0",
        "typing_extensions==4.7.1",
        "urllib3==2.0.4"
    ],
    entry_points={
        "console_scripts": [
            "support-toolbox = support_toolbox.main:main"
        ]
    },
)
