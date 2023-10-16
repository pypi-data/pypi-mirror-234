from ds_core.properties.abstract_properties import AbstractPropertyManager

__author__ = 'Darryl Oatridge'


class FeatureBuildPropertyManager(AbstractPropertyManager):
    """property manager for the Data Builder"""

    def __init__(self, task_name: str, creator: str):
        """initialises the properties manager.

        :param task_name: the name of the task name within the property manager
        :param creator: a username of this instance
        """
        root_keys = []
        knowledge_keys = ['describe']
        super().__init__(task_name=task_name, root_keys=root_keys, knowledge_keys=knowledge_keys, creator=creator)
