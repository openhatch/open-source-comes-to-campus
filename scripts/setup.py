from setuptools import setup

setup(
    name='CloneGithubIssues',
    version='0.01',
    install_requires=[
        'sh',
        'requests',
        ],
    packages=[
        'clone_github_issues',
        ]
    )
