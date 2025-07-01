from setuptools import setup, find_packages

setup(
    name="ha-tools",
    version="0.1.0",
    description="Command-line tools for Home Assistant automation management and diagnostics.",
    author="Adam Prostrollo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "websockets",
        "PyYAML"
    ],
    entry_points={
        "console_scripts": [
            # Add tool entry points here, e.g.:
            # "push-automation=ha_tools.push_automation:main",
        ]
    },
    python_requires=">=3.9",
    include_package_data=True,
    license="MIT",
)
