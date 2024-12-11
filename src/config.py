import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8000")
RTMP_URL = os.getenv("RTMP_URL", "rtmp://localhost/live/stream")
CAMERAID = os.getenv("CAMERAID", "")


def update_env_variable(key, value):
    env_file = ".env"

    with open(env_file, "r") as file:
        lines = file.readlines()

    with open(env_file, "w") as file:
        for line in lines:
            if line.startswith(f"{key}="): 
                file.write(f"{key}={value}\n")
            else:
                file.write(line)

        if not any(line.startswith(f"{key}=") for line in lines):
            file.write(f"{key}={value}\n")
