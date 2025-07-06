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
        "PyYAML",
        "GitPython"
    ],
    entry_points={
        "console_scripts": [
            "push-automation=push_automation:main",
            "get-ha-entities=get_ha_entities:main",
            "get-recent-trace-errors=get_recent_trace_errors:main",
            "generate-entity-state-doc=generate_entity_state_doc:main",
            "automation-watchdog=automation_watchdog:main",
            "decompose-automations=decompose_automations:main",
            "setup-ha-tools=setup_ha_tools:main",
            "pull-automations=pull_automations:main",
        ]
    },
    python_requires=">=3.9",
    include_package_data=True,
    license="MIT",
)
