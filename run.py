"""run.py"""

import os

from dotenv import load_dotenv
from application import create_app

# Load environment variables
load_dotenv(dotenv_path=".env") 

print(f"FLASK_ENV after load_dotenv: {os.getenv('FLASK_ENV')}")

env = os.environ.get("FLASK_ENV", "production").lower()

# print(f"run.py env: {env}")

if env == "development":
    config_class = "config.DevConfig"
elif env == "testing":
    config_class = "config.TestConfig"
else:
    config_class = "config.ProdConfig"

print(f"[run.py] config_class: {config_class}")


# This line is needed in this place outside 'main' for Gunicorn while deploying
app = create_app(config_class=config_class)

print(f"[run.py]: {app}")

def main():
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))


if __name__ == "__main__":
    main()