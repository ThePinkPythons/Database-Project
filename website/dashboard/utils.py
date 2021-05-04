"""
Utiltities for the REST API
"""


def check_str_param(param):
    """
    Checks to ensure that a string exists and is parseable. Returns None oterhwise.

    :param param:   The parameter to parse.
    :return:    A string or None
    """
    try:
        if param:
            if type(param) is str:
                param = param.strip()
            else:
                param = str(param)
            if len(param) > 0:
                return param
        return None
    except Exception as e:
        print(e)
        return None


def check_float_param(param):
    """
    Checks to ensure that a float exists and parseable. Returns None otherwise.

    :param param:   The parameter to check
    :return:    The parameter value
    """
    try:
        if param:
            if type(param) is int or type(param) is float or (type(param) is str and len(param) > 0):
                try:
                    param = float(param)
                    return param
                except Exception as e:
                    print(e)
        return None
    except Exception as e:
        print(e)
        return None


def check_int_param(param):
    """
    Checks to ensure that a  int exists and is parseable. Returns None otherwise.

    :param param:   The parameter to check
    :return:    The parameter value
    """
    try:
        if param:
            if type(param) is int or type(param) is float or (type(param) is str and len(param) > 0):
                try:
                    param = int(param)
                    return param
                except Exception as e:
                    print(e)
        return None
    except Exception as e:
        print(e)
        return None
