import base64

class FlexBytes(bytes):
    """
    Convenience type for dealing with bytes and json documents, as it 
    automatically converts to bytes numerical arrays and base64 encoded 
    strings.
    """
    
    __built_in_schema = [
        {
            'type': 'string',
            'contentMediaType': 'application/octet-stream',
            'contentEncoding': 'base64'
        }, 
        {
            'type': 'array', 
            'items': {
                'type': 'integer', 
                'minimum': 0,
                'exclusiveMaximum': 256
            }
        }
    ]

    @classmethod
    def __modify_schema__(cls, field_schema):
        if 'type' in field_schema:
            del field_schema['type']

        if 'format' in field_schema:
            del field_schema['format']
        
        if 'anyOf' not in field_schema:            
            field_schema.update(anyOf = cls.__built_in_schema)
        
    @classmethod
    def validate(cls, v):
        if isinstance(v, bytes):
            return cls(v)
        
        elif isinstance(v, list):
            in_range = all([d>=0 and d<256 for d in v])
            if not in_range:
                raise ValueError("List must contain numerical values ge than 0 and lt 256")
            return cls(bytes(v))

        elif isinstance(v, str):
            return cls(base64.b64decode(v.encode('ascii'), validate=True))
        
        raise ValueError(f'Unable to validate FlexBytes with type [{type(v)}] and value [{v}]')
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    def __str__(self) -> str:
        return base64.b64encode(self).decode('ascii')

