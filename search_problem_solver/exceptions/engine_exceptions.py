
class NoRulesException(Exception):
    """
    Used to signal the inexsistence of rules to use by the engine.
    """


class NotApplicableException(Exception):
    """
    Used when one particular rule can't be applied to some state.
    """
