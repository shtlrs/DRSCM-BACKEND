from abc import ABCMeta


from django.db.models.base import ModelBase


class AbstractModelMeta(ABCMeta, ModelBase):
    """
    A meta class that will be used to create abstract proxy models
    """
    pass
