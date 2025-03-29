from setuptools import setup, find_packages

setup(
    name="rag_app",
    version="0.1.0",
    description="RAG application with chat functionality",
    author="Arnav Jain",
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
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)