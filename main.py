import os

structure = {
    "auth-service": {
        "app": {
            "core": [
                "config.py",
                "database.py",
                "redis.py",
                "jwt.py",
                "security.py",
                "dependencies.py",
                "logging.py",
                "__init__.py",
            ],
            "models": ["models.py", "__init__.py"],
            "schemas": ["schemas.py", "__init__.py"],
            "services": ["auth_service.py", "__init__.py"],
            "routers": ["auth.py", "__init__.py"],
            "tasks": ["worker.py", "__init__.py"],
            "middleware": ["rate_limit.py", "__init__.py"],
            "_files": ["main.py", "__init__.py"],
        },
        "alembic": {
            "versions": [],
            "_files": ["env.py"],
        },
        "tests": ["conftest.py", "test_auth.py", "__init__.py"],
        "_files": [
            ".env.example",
            "Dockerfile",
            "docker-compose.yml",
            "requirements.txt",
        ],
    }
}


def create_structure(base_path, tree):
    for name, content in tree.items():
        if name == "_files":
            # Plain files at this level
            for filename in content:
                filepath = os.path.join(base_path, filename)
                open(filepath, "w").close()
                print(f"  created file: {filepath}")
        elif isinstance(content, list):
            # A folder whose value is just a list of files
            folder = os.path.join(base_path, name)
            os.makedirs(folder, exist_ok=True)
            print(f"created dir:  {folder}")
            for filename in content:
                filepath = os.path.join(folder, filename)
                open(filepath, "w").close()
                print(f"  created file: {filepath}")
        elif isinstance(content, dict):
            # A folder with nested structure
            folder = os.path.join(base_path, name)
            os.makedirs(folder, exist_ok=True)
            print(f"created dir:  {folder}")
            create_structure(folder, content)


if __name__ == "__main__":
    create_structure(".", structure)
    print("\nDone. Project scaffold created.")