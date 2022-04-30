from abc import ABCMeta


from django.db.models.base import ModelBase


class AbstractModelMeta(ABCMeta, ModelBase):
    pass
