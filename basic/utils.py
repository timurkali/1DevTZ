def sum_of_list_numbers(my_list: list):
    result = 0
    for elem in my_list:
        if isinstance(elem, int):
            result += elem

    return result
