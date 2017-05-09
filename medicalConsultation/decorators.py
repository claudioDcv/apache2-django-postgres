def print_blue(msg):
    print(chr(27)+"[0;36m")
    print(msg)
    print(chr(27)+"[0m")


def decorator_auditor_save(function):
    def wrap(self, *args, **kwargs):
        name = self.__class__.__name__
        print_blue("<< save model: {} >>".format(name))
        return function(self, *args, **kwargs)
    # wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap
