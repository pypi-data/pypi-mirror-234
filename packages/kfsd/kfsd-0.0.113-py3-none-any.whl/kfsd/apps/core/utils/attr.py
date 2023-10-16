
class AttrUtils(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.  """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    @staticmethod
    def format_list(value):
        return [AttrUtils.format_by_type(item) for item in value]

    @staticmethod
    def format(value):
        return AttrUtils.format_by_type(value)

    @staticmethod
    def format_by_type(value):
        if isinstance(value, dict):
            return AttrUtils(AttrUtils.format_dict(value))
        elif isinstance(value, list):
            return AttrUtils.format_list(value)
        elif isinstance(value, str):
            return value

        return value

    @staticmethod
    def format_dict(d):
        return AttrUtils({k: AttrUtils.format(v) for (k, v) in d.items()})

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrUtils, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(AttrUtils, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AttrUtils, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        return AttrUtils(self)
