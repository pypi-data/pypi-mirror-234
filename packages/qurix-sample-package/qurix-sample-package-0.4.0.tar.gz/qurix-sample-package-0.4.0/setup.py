from setuptools import setup, find_namespace_packages
from pathlib import Path

actual_path = Path(__file__).parent.resolve()

long_description = (actual_path / "README.md").read_text(encoding="utf-8")

main_ns = {}
with open("qurix/sample/package/__version__.py", "r") as file_handler:
    exec(file_handler.read(), main_ns)

setup(
    name="qurix-sample-package",
    version=main_ns["VERSION"],
    author="qurix Technology",
    license_files=("LICENSE"),
    description="qurix Package Template for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qurixtechnology/qurix-sample-package",
    packages=find_namespace_packages(),
    install_requires=[
    ],
    extras_require=dict(
        dev=[
            "pytest==7.3.1",
            "flake8==6.0.0",
            "pytest-flake8==1.1.1",
            "pytest-cov==4.0.0",
            "wheel==0.40.0",
            "twine==4.0.2",
            "typer==0.9.0"
        ]
    ),
    python_requires=">=3.10, <4",
    keywords=["python"],
)
