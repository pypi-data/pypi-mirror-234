# -*- coding: utf-8 -*-

import base64, pickle


def encode(obj: object) -> str:
    encoded = base64.encodebytes(pickle.dumps(obj))
    return encoded.decode('ascii')


def decode(str_repr: str):
    encoded = str_repr.encode('ascii')
    return pickle.loads(base64.decodebytes(encoded))