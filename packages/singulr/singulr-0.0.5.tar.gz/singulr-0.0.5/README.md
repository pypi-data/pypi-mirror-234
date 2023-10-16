[//]: # (# How to configure generative AI application for singular tracing)

[//]: # ( Following environment variables need to be set)

[//]: # (    LANGCHAIN_TRACING_V2="true")

[//]: # (    LANGCHAIN_ENDPOINT="http://0.0.0.0:8001/" # this is trace server &#40;run using apis/trace_api.py&#41;)

[//]: # (    LANGCHAIN_API_KEY="f9bc967894c04049b37031e9a6955728c7371cae" # this is the API key, can be anything for now)

[//]: # (    LANGCHAIN_PROJECT="madan" # project name )

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # ( # Changes in Langchain library , you should have 0.0.249 version)

[//]: # (    replace env.py file in langchain library via singulr_client/library/langchain/env.py)

[//]: # ()
[//]: # (# Langsmith library , you should have  0.0.16 version)

[//]: # (    replace utils.py file in langchain library via singulr_client/library/langsmith/utils.py)

# Create a wheel file and push into repository:
# Install Twine:
    Ensure you have twine installed, which is a tool for securely uploading packages to PyPI. You can install it with pip:
# Build you package:
    python setup.py sdist bdist_wheel

# Development Testing
    pip install dist/singulr*.whl

# Production Testing
# Upload pypi 
    twine upload --repository-url https://upload.pypi.org/legacy/ -u __token__ -p <token> dist/*
# Install package
    pip install singulr

# Apply isort using following command
isort -w singulr-client/
