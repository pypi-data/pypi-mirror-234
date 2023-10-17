import os


def load_secrets(remove_suffix: str = None):
    """Load secrets from /run/secrets into the environment

    Args:
        remove_suffix (str, optional): Remove the suffix from a secrets name. Defaults to None.
    """
    if os.path.exists("/run/secrets"):
        for secret in os.scandir("/run/secrets"):
            if secret.is_dir():
                return
            with open(secret.path, "r", encoding="utf-8") as secret_file:
                file_contents = secret_file.read()
            if remove_suffix:
                os.environ[secret.name.removesuffix(remove_suffix)] = file_contents
            else:
                os.environ[secret.name] = file_contents
