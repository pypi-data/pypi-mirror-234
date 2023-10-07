from setuptools import find_packages, setup


def get_version() -> str:
    rel_path = "src/huggingface_hub/__init__.py"
    with open(rel_path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


install_requires = [
    "filelock",
    "fsspec>=2023.5.0",
    "requests",
    "tqdm>=4.42.1",
    "pyyaml>=5.1",
    "typing-extensions>=3.7.4.3",  # to be able to import TypeAlias
    "packaging>=20.9",
]

extras = {}

extras["cli"] = [
    "InquirerPy==0.3.4",
    # Note: installs `prompt-toolkit` in the background
]

extras["inference"] = [
    "aiohttp",  # for AsyncInferenceClient
    "pydantic<2.0",  # for text-generation-inference
]

extras["torch"] = [
    "torch",
]

extras["fastai"] = [
    "toml",
    "fastai>=2.4",
    "fastcore>=1.3.27",
]

extras["tensorflow"] = ["tensorflow", "pydot", "graphviz"]


extras["testing"] = (
    extras["cli"]
    + extras["inference"]
    + [
        "jedi",
        "Jinja2",
        "pytest",
        "pytest-cov",
        "pytest-env",
        "pytest-xdist",
        "pytest-vcr",  # to mock Inference
        "pytest-asyncio",  # for AsyncInferenceClient
        "urllib3<2.0",  # VCR.py broken with urllib3 2.0 (see https://urllib3.readthedocs.io/en/stable/v2-migration-guide.html)
        "soundfile",
        "Pillow",
        "gradio",  # to test webhooks
        "numpy",  # for embeddings
    ]
)

# Typing extra dependencies list is duplicated in `.pre-commit-config.yaml`
# Please make sure to update the list there when adding a new typing dependency.
extras["typing"] = [
    "types-PyYAML",
    "types-requests",
    "types-simplejson",
    "types-toml",
    "types-tqdm",
    "types-urllib3",
    "pydantic<2.0",  # for text-generation dataclasses
]

extras["quality"] = [
    "black==23.7",
    "ruff>=0.0.241",
    "mypy==1.5.1",
]

extras["all"] = extras["testing"] + extras["quality"] + extras["typing"]

extras["dev"] = extras["all"]

extras["docs"] = extras["all"] + [
    "hf-doc-builder",
    "watchdog",
]


setup(
    name="huggingface_hub",
    version=get_version(),
    author="Hugging Face, Inc.",
    author_email="julien@huggingface.co",
    description="Client library to download and publish models, datasets and other repos on the huggingface.co hub",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="model-hub machine-learning models natural-language-processing deep-learning pytorch pretrained-models",
    license="Apache",
    url="https://github.com/huggingface/huggingface_hub",
    package_dir={"": "src"},
    packages=find_packages("src"),
    extras_require=extras,
    entry_points={
        "console_scripts": ["huggingface-cli=huggingface_hub.commands.huggingface_cli:main"],
        "fsspec.specs": "hf=huggingface_hub.HfFileSystem",
    },
    python_requires=">=3.8.0",
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    include_package_data=True,
)
