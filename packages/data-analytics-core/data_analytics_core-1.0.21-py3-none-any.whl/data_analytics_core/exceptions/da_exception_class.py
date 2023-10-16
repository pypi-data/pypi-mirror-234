from data_analytics_core.metaclasses.singleton import SingletonMetaClass


class DataAnalyticsException(Exception, metaclass=SingletonMetaClass):
    def __init__(self):
        self.code = None
        self.message = None
        self.tech_component = None
