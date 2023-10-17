import os


def load_secrets():
    """Load secrets from /run/secrets into the environment"""
    if os.path.exists("/run/secrets"):
        for secret in os.scandir("/run/secrets"):
            if secret.is_dir():
                return
            with open(secret.path, "r", encoding="utf-8") as secret_file:
                file_contents = secret_file.read()
            os.environ[secret.name] = file_contents
