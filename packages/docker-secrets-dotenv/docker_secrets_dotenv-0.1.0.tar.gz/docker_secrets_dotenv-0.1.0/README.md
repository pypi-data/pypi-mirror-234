# docker-secrets-dotenv

docker-secrets-dotenv takes all your docker secrets files, and sets them up in the environment.

## Getting Started

`pip install docker-secrets-dotenv`

To use docker-secrets-dotenv in your project run `load_secrets` as the start of your application:

```python
from docker_secrets import load_secrets

load_secrets() 
# This will load all secret files found in /run/secrets into the running environment
```

`load_secrets` will take the name of each secret file to set as the variable key and read the file contents as the value. It will overwrite existing environment variables.
