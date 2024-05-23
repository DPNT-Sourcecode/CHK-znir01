def validate_parameter_type(parameter, valid_type=int):

    return type(parameter)==valid_type


def sum(integer1, integer2):

    """ 
    Returns the sum of two integers.

        Parameters:
            integer1 - the first integer to be summed (int)
            integer2 - the second integer to be summed (int)
    
        Returns:
            The sum of the two numbers (int)
    """

    try:
        assert(validate_parameter_type(integer1))
        assert(validate_parameter_type(integer2))
    
    except AssertionError:
        print("\n Please ensure that both input parameters are integers i.e. whole numbers e.g. 3, 5, 7 etc. \n")
        return False
    
    except: 
        print("\n Something went wrong. Please check and try again. \n")
        return False


    return integer1 + integer2

