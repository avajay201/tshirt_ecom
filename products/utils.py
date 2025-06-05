def get_first_serializer_error(serializer_errors):
    """
    Returns the first error from serializer.errors as a dictionary with key 'error'.
    Converts ErrorDetail to plain string.
    """
    if isinstance(serializer_errors, dict):
        for field, messages in serializer_errors.items():
            if isinstance(messages, list) and messages:
                return {'error': str(messages[0])}
            elif isinstance(messages, dict):
                return get_first_serializer_error(messages)
    return {'error': 'Unknown error'}
