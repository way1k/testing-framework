class ConfigClass:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConfigClass, cls).__new__(cls)
        return cls.instance

    @classmethod
    def as_dict(cls):
        """Method for getting cfg settings as dict"""
        attributes = {}
        for item in cls.instance.__dict__.items():
            if not (item[0].startswith("_") or item[0] == "as_dict"):
                attributes[item[0]] = item[1]
        return attributes


config_obj = ConfigClass()
