from pydantic import BaseModel


class ModelBrowserRequestHeaders(BaseModel):
    Sec_GPC: int
    Connection: str = 'Keep-Alive'
    Upgrade_Insecure_Requests: bool = True
    Sec_Fetch_Dest: str = 'document'
    Sec_Fetch_Mode: str
    Sec_Fetch_Site: str = 'cross-site'
