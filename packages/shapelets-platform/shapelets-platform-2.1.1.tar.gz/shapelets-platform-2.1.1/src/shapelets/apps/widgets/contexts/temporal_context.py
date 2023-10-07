from typing import List
import uuid
from ..widget import AttributeNames


class TemporalContext:
    """
    Temporal Context: Set Widgets to the same temporal context
    """

    def __init__(self,
                 name: str = None,
                 widget_ids: List[str] = None,
                 context_id: str = None):
        self.name = name
        self.context_id = context_id if context_id else str(uuid.uuid1())
        self.widgets = widget_ids

    def to_dict(self):
        temporal_context_dict = {
            AttributeNames.ID.value: self.context_id,
            AttributeNames.NAME.value: self.name,
            AttributeNames.WIDGETS.value: self.widgets
        }
        return temporal_context_dict
