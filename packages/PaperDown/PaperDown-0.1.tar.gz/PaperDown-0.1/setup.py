from setuptools import setup, find_packages

setup(
    name="PaperDown",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'  # 我假设 bs4 是 beautifulsoup4，如果不是，请替换为正确的包名
    ],
)
