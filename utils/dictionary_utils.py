def check_existing_dictionary_in_list( list , key, value):
    '''
    Given a list of dictionaries check if list contains a dictory with the key/value
    '''
    it_contains_value = False

    for item in list:
        if getattr(item, key , False) == value:
            it_contains_value = True
            break

    return it_contains_value

