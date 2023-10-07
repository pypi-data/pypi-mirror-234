"""
Features related to working with numpy data in data structures and persistence. Requires the ``ml`` extra to be
installed, which can be installed in this way: ::

   pip install lifeomic-chatbot-tools[ml]

"""
import typing as t
from io import BytesIO

from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import PlainValidator
from typing_extensions import Annotated

from lifeomic_chatbot_tools._utils import ImportExtraError


try:
    import numpy as np
except ImportError:
    raise ImportExtraError("ml", __name__)


def encode_numpy(data: np.ndarray, mode="w"):
    """
    Serializes a numpy array to ``bytes`` or `str`, depending on ``mode``. Includes shape, datatype, and endianness
    information for perfect cross-platform reconstruction.

    Parameters
    ----------
    data : np.ndarray
        The data to serialize.
    mode : {'w', 'wb'}
        The serialization mode to use. if ``mode=="w"``, the output will be a string. If ``mode=="wb"``, the output
        will be ``bytes``.
    """
    mf = BytesIO()
    np.save(mf, data)
    value = mf.getvalue()
    mf.close()
    if mode == "w":
        return value.decode("latin-1")
    return value


def decode_numpy(data: t.Union[str, bytes]):
    """
    Deserializes a numpy array from ``bytes`` or ``str``, which was serialized using the :func:`encode_numpy` method.
    """
    if isinstance(data, str):
        data = data.encode("latin-1")
    mf = BytesIO(data)
    arr = np.load(mf)
    mf.close()
    return arr


def _serialize_numpy(x):
    return encode_numpy(x, mode="w")


def _deserialize_numpy(x):
    if isinstance(x, np.ndarray):
        return x
    return decode_numpy(x)


NDArray = Annotated[
    np.ndarray,
    PlainValidator(_deserialize_numpy),
    PlainSerializer(_serialize_numpy, return_type=str),
]
"""
A Pydantic-compatible Numpy array type. Assign it as the type of any Pydantic model
field that is a Numpy array and that you wish to be json-serializable. For example
this works:

>>> from pydantic import BaseModel, ConfigDict
...
... class Model(BaseModel):
...    model_config = ConfigDict(arbitrary_types_allowed=True)
...    arr: NDArray
...
... model = Model(arr=np.random.normal(size=2, 3))
... serialized = model.model_dump_json()
... assert isinstance(serialized, str)
... deserialized = Model.model_validate_json(serialized)
... assert np.allclose(model.arr, from_raw.arr)
"""
