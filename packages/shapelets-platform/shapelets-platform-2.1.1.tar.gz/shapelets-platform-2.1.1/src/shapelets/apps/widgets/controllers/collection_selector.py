#
# from ...widgets import AttributeNames, Widget
# from ....model import Collection, Sequence
#
#
# class CollectionSelector(Widget):
#     def __init__(self,
#                  default_collection: Collection = None,
#                  default_sequence: Sequence = None,
#                  name: str = None,
#                  title: str = None,
#                  collection_label: str = None,
#                  sequence_label: str = None,
#                  **additional):
#         super().__init__(self.__class__.__name__,
#                          name,
#                          ArgumentType(ArgumentTypeEnum.SEQUENCE),
#                          default_sequence,
#                          **additional)
#         self.title = title
#         self.default_collection = default_collection
#         self.default_sequence = default_sequence
#         self.collection_label = collection_label
#         self.sequence_label = sequence_label
#
#     def to_dict_widget(self):
#         collection_selector_dict = super().to_dict_widget()
#         if self.title is not None:
#             collection_selector_dict[AttributeNames.PROPERTIES.value].update(
#                 {AttributeNames.TITLE.value: self.title}
#             )
#         if self.default_collection is not None:
#             collection_selector_dict[AttributeNames.PROPERTIES.value].update(
#                 {AttributeNames.COLLECTION_ID.value: self.default_collection.collection_id}
#             )
#         if self.default_sequence is not None:
#             collection_selector_dict[AttributeNames.PROPERTIES.value].update(
#                 {AttributeNames.SEQUENCE_ID.value: self.default_sequence.sequence_id}
#             )
#         if self.collection_label is not None:
#             collection_selector_dict[AttributeNames.PROPERTIES.value].update(
#                 {AttributeNames.COLLECTION_LABEL.value: self.collection_label}
#             )
#         if self.sequence_label is not None:
#             collection_selector_dict[AttributeNames.PROPERTIES.value].update(
#                 {AttributeNames.SEQUENCE_LABEL.value: self.sequence_label}
#             )
#         return collection_selector_dict
