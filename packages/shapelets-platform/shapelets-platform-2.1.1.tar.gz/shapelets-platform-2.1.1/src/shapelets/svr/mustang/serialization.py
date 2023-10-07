import io 
import pickle

def _persistent_load(persid):
    if persid == "Ellipsis":
        return Ellipsis
    raise pickle.UnpicklingError("unsupported persistent object")

def _persistent_id(obj):
    if obj is Ellipsis:
        return "Ellipsis"

def pickle_ast(val):
    pickled = io.BytesIO()
    pickler = pickle.Pickler(pickled)
    pickler.persistent_id = _persistent_id
    pickler.dump(val)
    return pickled


def unpickle_ast(pickled):
    pickled.seek(0)
    unpickler = pickle.Unpickler(pickled)
    unpickler.persistent_load = _persistent_load
    return unpickler.load()

