# type: ignore

"""The setup script."""

from pathlib import Path
import sys
from setuptools import find_packages, setup


# add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from roxbot.version import get_version  # noqa: E402


# please keep this lean and mean. Add dev requirements to .devcontainer/requirments.txt
requirements = [
    "click",
    "coloredlogs",
    "orjson",
    "pydantic",
    "pymap3d",
    "pynmea2",
    "pyserial-asyncio",
    "websockets",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="ROX Autmation",
    author_email="dev@roxautomation.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    description="KISS robootics framework",
    install_requires=requirements,
    include_package_data=True,
    keywords="",
    name="roxbot",
    package_dir={"": "src"},
    packages=find_packages("src"),
    test_suite="tests",
    tests_require=test_requirements,
    url="",
    version=get_version(),
    zip_safe=False,
    package_data={"roxbot": ["py.typed"]},
    entry_points={"console_scripts": ["roxbot=roxbot.cli:cli"]},
)
