PYPROJECT_TEMPLATE = """
[tool.poetry]
name = "{project_id}"
version = "0.1.0"
description = ""
authors = ["user <user@yunzhangfang.com>"]
packages = [{ include = "{project_id}" }]

[tool.poetry.dependencies]
python = "^3.11"
httpx = "^0.24.1"
fastapi = "^0.103.1"
uvicorn = "^0.23.2"
requests = "^2.28.1"
psutil = "^5.9.4"
tencentcloud-sdk-python = "^3.0.979"
pytest = "^7.4.2"
sandbox-func = "^0.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s [%(levelname)5s] %(name)s:%(filename)s:%(lineno)s - %(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"

[[tool.poetry.source]]
name = "custom"
url = "https://pypi.org/simple"
default = true
"""