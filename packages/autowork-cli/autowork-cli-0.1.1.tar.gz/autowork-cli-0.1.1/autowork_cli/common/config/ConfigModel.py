class EnvModel:
    API_KEY: str


class GlobalConfigModel:
    ENV: str
    DEV_APPS: str
    DEBUG: bool


class ConfigModel:
    GLOBAL_CONFIG: GlobalConfigModel
    DEV: EnvModel
    BETA: EnvModel
    PROD: EnvModel
