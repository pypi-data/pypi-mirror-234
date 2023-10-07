# from ...widgets import Widget, AttributeNames
# from ....model import Collection
# from ..contexts import (
#     FilteringContext,
#     TemporalContext
# )
#
#
# class SequenceList(Widget):
#     def __init__(self,
#                  collection: Collection,
#                  title: str = None,
#                  temporal_context: TemporalContext = None,
#                  filtering_context: FilteringContext = None,
#                  **additional):
#         super().__init__(self.__class__.__name__,
#                          **additional)
#         self.collection = collection
#         self.title = title
#         self.temporal_context = temporal_context
#         self.filtering_context = filtering_context
#         temporal_context_id = None
#         if self.temporal_context:
#             temporal_context_id = self.temporal_context.context_id
#             self.temporal_context.widgets.append(self.widget_id)
#         filtering_context_id = None
#         if self.filtering_context:
#             filtering_context_id = filtering_context.context_id
#             filtering_context.output_widgets.append(self.widget_id)
#         self.temporal_context = temporal_context_id
#         self.filtering_context = filtering_context_id
#
#     def to_dict_widget(self):
#         sequences_list_dict = super().to_dict_widget()
#         if self.title is not None:
#             if isinstance(self.title, str):
#                 sequences_list_dict[AttributeNames.PROPERTIES.value].update({
#                     AttributeNames.TITLE.value: self.title
#                 })
#
#         if self.collection:
#             if isinstance(self.collection, Collection):
#                 sequences_list_dict[AttributeNames.PROPERTIES.value].update({
#                     AttributeNames.COLLECTION_ID.value: self.collection.collection_id
#                 })
#
#         return sequences_list_dict
