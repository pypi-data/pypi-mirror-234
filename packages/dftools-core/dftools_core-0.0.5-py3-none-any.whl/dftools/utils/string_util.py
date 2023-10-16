

def compare_string(str1 : str, str2 : str) -> int:
    """
        Compares 2 strings by checking if they are valued and their value is different

        Returns
        -----------
        comparison_result : int
            The comparison result will be :
                - Equal to 0 if both strings are not valued or if both strings are valued and equal
                - Equal to -1 if only one of the strings is valued
                - Equal to 1 if both string are valued but are not equal
    """
    if (str1 == None & str2 == None) :
        return 0
    if (str1 == None | str2 == None):
        return -1
    if (str1 != str2):
        return 1
    return 0