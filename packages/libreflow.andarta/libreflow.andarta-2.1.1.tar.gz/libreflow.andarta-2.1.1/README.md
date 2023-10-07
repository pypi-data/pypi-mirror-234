# Libreflow.andarta

This project defines a flow dedicated to Andarta Pictures productions.

## How to install

- Requirements:
    - `pip`
    - `poetry`
    - Define environment variables in GPO

- Env variables:
    - LF_CLUSTER_NAME: Used to define a group of people within the same workgroup thant can access the same project. Don't change it otherwise you won't access existing projects.
    - LF_SITE_NAME: Necessary when setting the multisite options ON
    - MONGO_URI: For connect to a MongoDB deployment
    - REDIS_DB: The redis index db. It's recommanded to set it to the default (0)
    - REDIS_HOST: The host url/ip of your redis instance
    - REDIS_PASSWORD: If your redis instance is password protected
    - REDIS_PORT: The port of the redis instance
    - TECH_DIR: Directory where the install script are stored on your computer or local network

- Installation script are stored in `install` folder
- Execute in a terminal with `python backend_libreflow.py --install` command
- After installation is complete, you can start Libreflow with the `.bat ` exectuable