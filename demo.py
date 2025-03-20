data = [
    {'name': 'bb', 'key': '331406f6ef8a1e3c954e87548c236dd7dde8d8a88e552b2428cf116cecc10ca7'},
    {'name': 'bb', 'key': 'd8f06053f57d018091d19c3e6008227861ddc9ef1dc2d6a5903862a31cbbc770'},
    {'name': 'bb', 'key': 'beab7e4a19378a8d19c505233d3983a799552b08578d30d0028b52ba5ab942fa'},
    {'name': 'bb', 'key': 'eb33d38b9d604394bb0509a489353d712f4248bfd8147bf6384622e96127b96d'}
]
api_key = "eb33d38b9d604394bb0509a489353d712f4248bfd8147bf6384622e96127b96"

def check_exist_api_key(data, api_key):
    """
    Checks if the given API key exists in the provided data.

    Args:
        data (list): A list of dictionaries, where each dictionary contains 'key'.
        api_key (str): The API key to search for.

    Returns:
        bool: True if the API key exists, False otherwise.
    """
    if not isinstance(data, list):
        raise TypeError("Data must be a list.")

    if not isinstance(api_key, str):
        raise TypeError("API key must be a string.")

    for item in data:
        if not isinstance(item, dict):
            raise TypeError("Items in data must be dictionaries.")

        if "key" not in item:
            raise ValueError("Each item in data must contain a 'key'.")

        if item["key"] == api_key:
            return True

    return False

test = check_exist_api_key(data, api_key )
print ( "test : ",  test )

