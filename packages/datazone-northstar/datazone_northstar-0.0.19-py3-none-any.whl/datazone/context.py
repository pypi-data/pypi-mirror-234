from contextvars import ContextVar

inspect_mode = ContextVar("inspect_mode", default=False)
debug_mode = ContextVar("debug_mode", default=False)
