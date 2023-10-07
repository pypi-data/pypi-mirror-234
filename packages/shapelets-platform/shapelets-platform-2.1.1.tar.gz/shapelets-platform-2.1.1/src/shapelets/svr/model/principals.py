from __future__ import annotations

import base64
from typing import Optional
from pydantic import BaseModel
from ..utils import FlexBytes

class PrincipalId(BaseModel):
    """
    This is the representation of a principal which has been validated 
    by an authentication protocol
    """
    
    scope: str 
    """
    Principal scope (Azure AD, Google, LinkedIn, Generic OpenID, etc...)
    """
    
    id: str 
    """
    User unique id in the context of the authentication protocol.
    """
    
    
class GCPrincipalId(PrincipalId):
    """
    A GC signed principal
    """
    signature: FlexBytes
    
    class Config:
        json_encoders = {
            FlexBytes: lambda v: str(v) 
        }       

    
class ResolvedPrincipalId(PrincipalId):
    """
    This is a representation of a principal resolved to a user id 
    in Shapelets.
    """
    
    userId: int 
    """
    The user associated with this principal
    """

class SignedPrincipalId(ResolvedPrincipalId):
    """
    This is a certified and resolved principal which can be used to 
    interact with the system.
    """
    
    signature: bytes
    """
    Cryptographic signature
    """
    
    def to_token(self) -> str:
        """
        Compact token representation.
        
        It is a base64 string, which comprises of 4 parts, separated 
        by a semicolon, in order:
        
            - scope: the authentication protocol used
            - id: unique identifier in the context of the scope
            - userId: unique identifier in the context of Shapelets
            - signature: cryptographic signature that protects against 
              tampering and ensures integrity.
        """
        encoded = base64.b64encode(self.signature).decode('ascii')
        plain =  f'{self.scope}:{self.id}:{self.userId}:{encoded}'
        return base64.b64encode(plain.encode('ascii')).decode('ascii')
    
    @staticmethod
    def from_token(token: str) -> Optional[SignedPrincipalId]:
        plain = base64.b64decode(token).decode('ascii')
        parts = plain.split(":")
        if len(parts) != 4:
            return None 
            
        return SignedPrincipalId(
            scope = str(parts[0]), id = str(parts[1]), 
            userId=int(parts[2]), 
            signature= base64.b64decode(str(parts[3]).encode('ascii')))     
