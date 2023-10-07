from ds_capability.components.commons import Commons
from ds_capability.intent.abstract_feature_intent import AbstractFeatureIntentModel
from ds_capability.managers.feature_transform_property_manager import FeatureTransformPropertyManager

class AbstractFeatureTransformIntentModel(AbstractFeatureIntentModel):

    def __init__(self, property_manager: FeatureTransformPropertyManager, default_save_intent: bool=None,
                 default_intent_level: [str, int, float]=None, order_next_available: bool=None,
                 default_replace_intent: bool=None):
        """initialisation of the Intent class.

        :param property_manager: the property manager class that references the intent contract.
        :param default_save_intent: (optional) The default action for saving intent in the property manager
        :param default_intent_level: (optional) the default level intent should be saved at
        :param order_next_available: (optional) if the default behaviour for the order should be next available order
        :param default_replace_intent: (optional) the default replace existing intent behaviour
        """
        default_save_intent = default_save_intent if isinstance(default_save_intent, bool) else True
        default_replace_intent = default_replace_intent if isinstance(default_replace_intent, bool) else True
        default_intent_level = default_intent_level if isinstance(default_intent_level, (str, int, float)) else 'primary'
        default_intent_order = -1 if isinstance(order_next_available, bool) and order_next_available else 0
        intent_param_exclude = ['canonical']
        intent_type_additions = []
        super().__init__(property_manager=property_manager, default_save_intent=default_save_intent,
                         intent_param_exclude=intent_param_exclude, default_intent_level=default_intent_level,
                         default_intent_order=default_intent_order, default_replace_intent=default_replace_intent,
                         intent_type_additions=intent_type_additions)
        self.label_gen = Commons.label_gen()
