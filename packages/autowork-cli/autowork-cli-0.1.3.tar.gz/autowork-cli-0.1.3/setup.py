from setuptools import setup, find_packages

setup(
    name="autowork-cli",
    version="0.1.3",
    description="沙盒函数自动工具",
    packages=find_packages(),
    python_requires='>=3.6',
    entry_points={
      'console_scripts': ['autowork=autowork_cli.__main__:run'],
    },
)
