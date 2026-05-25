import os

folders = [
    "app/core",
    "app/services/auth",
    "app/services/pdf",
    "app/services/chat",
    "app/services/billing",
    "app/services/email",
    "app/db",
    "app/tests",
]

files = [
    "app/main.py",
    "app/core/config.py",
    "app/core/security.py",
    "app/core/dependencies.py",
    "app/services/auth/router.py",
    "app/services/auth/schemas.py",
    "app/services/auth/models.py",
    "app/services/auth/service.py",
    "app/services/pdf/__init__.py",
    "app/services/chat/__init__.py",
    "app/services/billing/__init__.py",
    "app/services/email/__init__.py",
    "app/db/postgres.py",
    "app/db/redis.py",
    "app/tests/__init__.py",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"📁 Created folder: {folder}")

for file in files:
    with open(file, "w") as f:
        f.write(f"# {file}\n")
    print(f"   📄 Created file: {file}")

print("\n✅ Project structure generated successfully!")