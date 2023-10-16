class Input:
    def __init__(self, entity, **kwargs):
        self.entity = entity
        self.kwargs = kwargs


class Output:
    def __init__(self, entity=None, materialized: bool = True, **kwargs):
        self.materialize = materialized
        self.entity = entity
        self.kwargs = kwargs
