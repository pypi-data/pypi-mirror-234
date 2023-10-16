class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Instantiates class only once during runtime, follows Singleton DP.

        If at least one class attribute value is different from the one
        specified in the previous instantiation call, a new instance is created.

        """
        if cls in cls._instances:
            class_attributes = cls._instances[cls].__dict__.copy()
            for key in cls._instances[cls].__dict__.keys():
                if key not in kwargs.keys():
                    class_attributes.pop(key)
            new_instance_has_a_different_attribute_value = (class_attributes
                                                            != kwargs)
        if (cls not in cls._instances) or (
                cls in cls._instances
                and new_instance_has_a_different_attribute_value
        ):
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]
