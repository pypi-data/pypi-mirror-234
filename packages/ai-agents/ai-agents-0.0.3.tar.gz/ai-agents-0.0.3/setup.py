import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai-agents", 
    version="0.0.3",
    author="AIWaves",
    author_email="contact@aiwaves.cn",
    description="An Open-source Framework for Autonomous Language Agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aiwaves-cn/agents",
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages = ['agents'],
    python_requires='>=3.6',
    license='Apache License 2.0',
    install_requires=[
        'beautifulsoup4',
        'fastapi',
        'google_api_python_client',
        'google_auth_oauthlib',
        'gradio==3.39.0',
        'langchain==0.0.308',
        'numpy',
        'openai',
        'pandas',
        'Pillow',
        'protobuf',
        'psutil',
        'PyYAML',
        'Requests',
        'selenium',
        'sentence_transformers',
        'setuptools',
        'text2vec',
        'torch',
        'tqdm',
        'uvicorn',
        'pydantic==1.10.9',
        'typing_extensions==4.5.0',
        'serpapi'
    ]
)

"""
python3 setup.py sdist bdist_wheel
"""