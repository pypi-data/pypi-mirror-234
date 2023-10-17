from pydantic import BaseModel


class SandboxFuncRequest(BaseModel):
    appId: str
    functionId: str
    input: dict