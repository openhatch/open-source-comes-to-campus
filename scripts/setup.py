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
        ],
    entry_points={
        'console_scripts':
            ['setup_practicing_git = clone_github_issues:main',
             ]
        }
)
