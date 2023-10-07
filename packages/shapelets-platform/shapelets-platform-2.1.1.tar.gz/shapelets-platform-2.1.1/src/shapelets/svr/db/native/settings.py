from typing import Optional
from typing_extensions import Literal

from pydantic import BaseModel, PositiveInt, ByteSize


class DatabaseSettings(BaseModel):
    """
    Database settings
    """

    path: Optional[str] = None
    """
    Where data is to be stored
    """

    temp_directory: Optional[str] = None
    """
    Temporal directory where offload result sets from memory
    """

    db_schema: str = 'shapelets'
    """
    Default schema where data is persisted
    """

    collation: Optional[str] = None
    """
    Locale (two character code) that determines the collation.
    
    List of possible codes:
    
    ```
        'af', 'am', 'ar', 'ar_sa', 'as', 'az', 'be', 'bg', 'bn', 'bo', 
        'br', 'bs', 'ca', 'ceb', 'chr', 'cs', 'cy', 'da', 'de', 'de_at', 
        'dsb', 'dz', 'ee', 'el', 'en', 'en_us', 'eo', 'es', 'et', 'fa', 
        'fa_af', 'ff', 'fi', 'fil', 'fo', 'fr', 'fr_ca', 'ga', 'gl', 
        'gu', 'ha', 'haw', 'he', 'he_il', 'hi', 'hr', 'hsb', 'hu', 
        'hy', 'id', 'id_id', 'ig', 'is', 'it', 'ja', 'ka', 'kk', 'kl', 
        'km', 'kn', 'ko', 'kok', 'ku', 'ky', 'lb', 'lkt', 'ln', 'lo', 
        'lt', 'lv', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'nb', 
        'nb_no', 'ne', 'nfc', 'nl', 'nn', 'om', 'or', 'pa', 'pa_in', 
        'pl', 'ps', 'pt', 'ro', 'ru', 'sa', 'se', 'si', 'sk', 'sl', 
        'smn', 'sq', 'sr', 'sr_ba', 'sr_me', 'sr_rs', 'sv', 'sw', 'ta', 
        'te', 'th', 'tk', 'to', 'tr', 'ug', 'uk', 'ur', 'uz', 'vi', 
        'wae', 'wo', 'xh', 'yi', 'yo', 'yue', 'yue_cn', 'zh', 'zh_cn', 
        'zh_hk', 'zh_mo', 'zh_sg', 'zh_tw', 'zu',
        'noaccent', 'nocase', 
    ```
    
    """

    memory_limit: Optional[ByteSize] = None
    """
    Maximum use of memory 
    """

    threads: Optional[PositiveInt] = None
    """
    Maximum number of threads
    """

    order: Optional[Literal['ASC', 'DESC']] = None
    """
    Should order operations be ascending or descending when no explicit 
    criteria is provided.
    """

    null_order: Optional[Literal['FIRST', 'LAST']] = None
    """
    Should nulls appear first or last during sort operations 
    """

    object_cache: Optional[bool] = None
    """
    Cache schemas and other artifacts.
    """
