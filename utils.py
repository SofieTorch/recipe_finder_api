
def csv_str_to_list(list_str: str):
    new_str = list_str.replace('\'', '').replace('[', '').replace(']', '').replace('\', \'', '\',\'')
    result = new_str.split(',')
    return result

