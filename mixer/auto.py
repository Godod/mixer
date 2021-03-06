""" Automatic backend selection. """
from importlib import import_module

from .main import ProxyMixer


class MixerProxy:

    """ Load mixer for class automaticly.

    ::

        from mixer.auto import mixer

        django_model_instance = mixer.blend('django.app.models.Model')
        sqlalchemy_model_instance = mixer.blend('sqlalchemy.app.models.Model')
        mongo_model_instance = mixer.blend('mongoengine.app.models.Model')

    """

    __store__ = dict()

    @classmethod
    def cycle(cls, count=5):
        """ Generate a lot instances.

        :return MetaMixer:

        """
        return ProxyMixer(cls, count)

    @classmethod
    def blend(cls, model, **params):
        """ Get a mixer class for model.

        :return instance:

        """
        scheme = cls._load_cls(model)
        backend = cls.__store__.get(scheme)

        if not backend:

            if cls._is_django_model(scheme):
                from .backend.django import mixer as backend

            elif cls._is_sqlalchemy_model(scheme):
                from .backend.sqlalchemy import mixer as backend

            elif cls._is_mongoengine_model(scheme):
                from .backend.mongoengine import mixer as backend

            cls.__store__[scheme] = backend

        return backend.blend(scheme, **params)

    @staticmethod
    def _load_cls(cls_type):
        if isinstance(cls_type, str):
            mod, cls_type = cls_type.rsplit('.', 1)
            mod = import_module(mod)
            cls_type = getattr(mod, cls_type)
        return cls_type

    @staticmethod
    def _is_django_model(model):
        try:
            from django.db.models import Model
            return issubclass(model, Model)
        except ImportError:
            return False

    @staticmethod
    def _is_sqlalchemy_model(model):
        return bool(getattr(model, '__mapper__', False))

    @staticmethod
    def _is_mongoengine_model(model):
        try:
            from mongoengine.base.document import BaseDocument
            return issubclass(model, BaseDocument)
        except ImportError:
            return False


mixer = MixerProxy()
