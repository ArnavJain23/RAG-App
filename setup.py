from setuptools import setup, find_packages

setup(
    name="rag_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "llama-index",
        "python-dotenv",
        "anthropic",
        "sentence-transformers",  # Required for HuggingFaceEmbedding
    ],
    entry_points={
        "console_scripts": [
            "rag-app=src.app:main",
        ],
    },
)