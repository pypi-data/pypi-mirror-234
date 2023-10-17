# -*- coding: utf-8 -*-
import importlib, abc, warnings, arrow, copy, pdb
from packaging.version import parse as LooseVersion
from langchain import __version__
from portageur.kdutils.code import encode, decode


class ModelBase():

    def __init__(self, **kwargs):
        self.impl = None
        self.kwargs = copy.deepcopy(kwargs)
        self.update_time = arrow.now().format("YYYY-MM-DD HH:mm:ss"),

    def predict(self, **kwargs):
        return self.impl.predict_messages(**kwargs)

    async def apredict(self, immed=True, **kwargs):
        return await self.impl.apredict_messages(**kwargs) if immed else self.impl.apredict_messages(**kwargs)

    @abc.abstractmethod
    def save(self):
        if self.__class__.__module__ == '__main__':
            warnings.warn(
                "model is defined in a main module. The model_name may not be correct."
            )
        model_desc = dict(model_name=self.__class__.__module__ + "." +
                          self.__class__.__name__,
                          language='python',
                          update_time=self.update_time,
                          kwargs=encode(self.kwargs),
                          impl=encode(self.impl),
                          internal_model=self.impl.__class__.__module__ + "." +
                          self.impl.__class__.__name__)
        return model_desc

    @classmethod
    @abc.abstractmethod
    def load(cls, model_desc):
        layout = cls()
        layout.update_time = model_desc['update_time']
        layout.kwargs = decode(model_desc['kwargs'])
        layout.impl = decode(model_desc['impl'])
        return model_desc

    @property
    def m(self):
        return self.impl


def create_model_base(party_name=None):
    if not party_name:
        return ModelBase
    else:

        class ExternalLibBase(ModelBase):
            _lib_name = party_name

            def save(self) -> dict:
                model_desc = super().save()
                if self._lib_name == 'chat_models':
                    model_desc[self._lib_name + "_version"] = __version__
                elif self._lib_name == 'llms':
                    model_desc[self._lib_name + "_version"] = __version__
                else:
                    raise ValueError(
                        "3rd party lib name ({0}) is not recognized".format(
                            self._lib_name))
                return model_desc

            @classmethod
            def load(cls, model_desc):
                obj_layout = super().load(model_desc)
                if cls._lib_name == 'chat_models':
                    current_version = __version__
                elif cls._lib_name == 'llms':
                    current_version = __version__
                else:
                    raise ValueError(
                        "3rd party lib name ({0}) is not recognized".format(
                            cls._lib_name))
                if LooseVersion(current_version) < LooseVersion(
                        model_desc[cls._lib_name + "_version"]):
                    warnings.warn(
                        'Current {2} version {0} is lower than the model version {1}. '
                        'Loaded model may work incorrectly.'.format(
                            __version__, model_desc[cls._lib_name],
                            cls._lib_name))
                return obj_layout

        return ExternalLibBase


def create_models(name):
    return importlib.import_module('langchain.chat_models').__getattribute__(
        name)


def create_llms(name):
    return importlib.import_module('langchain.llms').__getattribute__(name)
