import os


def get_klu_env():
    return os.getenv("KLU_ENV", "prod")


def get_api_url():
    env = get_klu_env()
    return "http://localhost:4000/v1" if env == "dev" else "https://api.klu.ai/v1"
