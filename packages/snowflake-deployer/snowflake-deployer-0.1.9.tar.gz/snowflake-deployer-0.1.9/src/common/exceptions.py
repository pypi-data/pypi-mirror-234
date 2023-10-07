class file_not_exists(Exception):
    def __init__(self, file_path, message=''):
        self.file_path = file_path
        self.message = 'file not found in path: ' + file_path + '.' + message
        self.return_error = True
        super().__init__(self.message)


class missing_parameter(Exception):
    def __init__(self, parameter, message=''):
        self.parameter = parameter
        self.message = 'Missing required parameter: ' + parameter + '.' + message
        self.return_error = True
        super().__init__(self.message)

class feature_not_supported(Exception):
    def __init__(self, object_type:str, feature:str, message=''):
        self.object_type = object_type
        self.feature = feature
        self.message = 'Not supported feature. Object: ' + object_type + '; feature: ' + feature + '.' + message
        self.return_error = True
        super().__init__(self.message)

class object_type_not_supported(Exception):
    def __init__(self, object_type:str, message=''):
        self.object_type = object_type
        self.message = 'Not supported object type: ' + object_type + '.' + message
        self.return_error = True
        super().__init__(self.message)



#def __init__(self, file_path, message="Salary is not in (5000, 15000) range"):