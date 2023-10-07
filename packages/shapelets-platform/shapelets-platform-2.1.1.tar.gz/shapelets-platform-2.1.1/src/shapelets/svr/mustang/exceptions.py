
class AstError(Exception):
    pass

class ERDiagramError(Exception):
    pass

class DecompileError(NotImplementedError):
    pass

class InvalidQuery(Exception):
    pass

class TranslationError(Exception):
    pass

class ExprEvalError(Exception):
    def __init__(exc, src, cause):
        assert isinstance(cause, Exception)
        msg = '`%s` raises %s: %s' % (src, type(cause).__name__, str(cause))
        ExprEvalError.__init__(exc, msg)
        exc.cause = cause

def throw(exc_type, *args, **kwargs):
    if isinstance(exc_type, Exception):
        assert not args and not kwargs
        exc = exc_type
    else:
        exc = exc_type(*args, **kwargs)
    exc.__cause__ = None
    try:
        raise exc
    finally:
        del exc
        
def reraise(exc_type, exc, tb):
    try:
        raise exc.with_traceback(tb)
    finally:
        del exc, tb        