from typing import Optional
from pydantic import BaseModel, FilePath, SecretStr


class SSLSettings(BaseModel):
    """
    Captures SSL settings 
    """

    keyfile: FilePath
    """
    SSL key file
    """

    certfile: FilePath
    """
    SSL certificate file
    """

    keyfile_password: Optional[SecretStr] = None
    """
    Password to decrypt the ssl key
    """

    version: Optional[int] = None
    """
    SSL version to use (see stdlib ssl module's)
    """

    cert_reqs: Optional[int] = None
    """
    Whether client certificate is required
    
    Values are defined by enum `VerifyMode` in ssl module
    """

    ca_certs: Optional[FilePath] = None
    """
    CA certificates file
    """

    ciphers: Optional[str] = None
    """
    Ciphers to use (see stdlib ssl module's)
    """
