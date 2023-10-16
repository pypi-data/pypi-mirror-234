
from dftools.utils.list_util import concat_list_and_deduplicate

def encode_value(input_value, encoding : str):
    """
        Encodes a value. 
        The input value should be of type str, int, ...
        
        Parameters
        -----------
            input_value : The input value
            encoding : The encoding

        Returns
        -----------
            The encoded value
    """
    if input_value is None:
        return None
    if type(input_value) == str:
        return input_value.encode(encoding)
    return input_value


def encode_list(input_list : list, encoding : str):
    """
        Encodes a list. 
        
        Parameters
        -----------
            input_list : The input list
            encoding : The encoding

        Returns
        -----------
            The encoded list
    """
    encoded_list = []
    for list_value in input_list :
        encoded_list_value = None
        if list_value is not None :
            list_value_type = type(list_value)
            if list_value_type == dict:
                encoded_list_value = encode_dict(input_dict=list_value, encoding=encoding)
            elif list_value_type == list:
                encoded_list_value = encode_list(input_list=list_value, encoding=encoding)
            else :
                encoded_list_value = encode_value(input_value=list_value, encoding=encoding)
        encoded_list.append(encoded_list_value)
    return encoded_list
   
def encode_dict(input_dict : dict, encoding : str) -> dict:
    """
        Encodes a dictionnary. 
        
        Parameters
        -----------
            input_dict : The input dictionnary
            encoding : The encoding

        Returns
        -----------
            The encoded dictionnary
    """
    dict_encode = {}
    for k, v in input_dict.items():
        encoded_key = k.encode(encoding) if (k is not None) & (type(k) == str) else k
        encoded_value = None
        if v is not None : 
            value_type = type(v)
            if value_type == dict:
                encoded_value = encode_dict(input_dict=v, encoding=encoding)
            elif value_type == list :
                encoded_value = encode_list(input_list=v, encoding=encoding)
            else :
                encoded_value = encode_value(input_value=v, encoding=encoding)
        dict_encode.update({encoded_key: encoded_value})
    return dict_encode



def decode_value(input_value, encoding : str):
    """
        Decodes a value. 
        The input value should be of type str, int, ...
        
        Parameters
        -----------
            input_value : The input value
            encoding : The encoding

        Returns
        -----------
            The decoded value
    """
    if input_value is None:
        return None
    if type(input_value) == bytes:
        return input_value.decode(encoding)
    return input_value


def decode_list(input_list : list, encoding : str):
    """
        Decodes a list. 
        
        Parameters
        -----------
            input_list : The input list
            encoding : The encoding

        Returns
        -----------
            The decoded list
    """
    decoded_list = []
    for list_value in input_list :
        decoded_list_value = None
        if list_value is not None :
            list_value_type = type(list_value)
            if list_value_type == dict:
                decoded_list_value = decode_dict(input_dict=list_value, encoding=encoding)
            elif list_value_type == list:
                decoded_list_value = decode_list(input_list=list_value, encoding=encoding)
            else :
                decoded_list_value = decode_value(input_value=list_value, encoding=encoding)
        decoded_list.append(decoded_list_value)
    return decoded_list
   
def decode_dict(input_dict : dict, encoding : str) -> dict:
    """
        Decodes a dictionnary. 
        
        Parameters
        -----------
            input_dict : The input dictionnary
            encoding : The encoding

        Returns
        -----------
            The decoded dictionnary
    """
    dict_decode = {}
    for k, v in input_dict.items():
        encoded_key = k.decode(encoding, 'replace') if (k is not None) & (type(k) == str) else k
        decoded_value = None
        if v is not None : 
            value_type = type(v)
            if value_type == dict:
                decoded_value = decode_dict(input_dict=v, encoding=encoding)
            elif value_type == list :
                decoded_value = decode_list(input_list=v, encoding=encoding)
            else :
                decoded_value = decode_value(input_value=v, encoding=encoding)
        dict_decode.update({encoded_key: decoded_value})
    return dict_decode

def get_unique_key_list(dict1 : dict, dict2 : dict) -> list:
    return concat_list_and_deduplicate(list(dict1.keys()), list(dict2.keys()))