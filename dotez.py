data = {}  # Keys and values will be stored here after the load_ez() function is executed


class Datatype:
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"


def load_ez():  # Loads the .ez file into a dict called data. Do not mistake this for get_all()
    data.clear()  # Clearing the previous data in case we are just reloading it

    with open(r".ez", "r") as file:
        lines = [line.rstrip() for line in file]

        split = [line.split(" ", 2) for line in lines]

        for item in split:
            try:
                data.update({item[1]: {"Type": item[0], "Value": item[2], "Line": data.__len__()}})
            except IndexError:
                raise IndexError("Something is missing from the .ez file")


def get_item(item: str):  # Retrieves a specified object from data
    try:
        item = data[item]
    except KeyError:
        raise KeyError("Key doesn't exist in .ez file")  # Look into .ez file and check if variable exists there

    # Figure out what type of variable to return
    if item["Type"] == Datatype.STRING: return str(item["Value"])
    if item["Type"] == Datatype.INTEGER: return int(item["Value"])
    if item["Type"] == Datatype.FLOAT: return float(item["Value"])
    if item["Type"] == Datatype.BOOLEAN: return bool(item["Value"])


def get_all():
    return data


def clear_ez():  # Clear the .ez file
    with open(r".ez", "w") as file:
        file.flush()

    load_ez()  # Reload the data file, so it doesn't show previous values


def append_item(datatype: type, identifier: str, value: str or int or bool or float):  # Append an item to the .ez file
    try:
        value = datatype(value)
    except ValueError:
        raise ValueError(f"Cannot convert {value} to {datatype}")

    datakey = None

    # Figure out what type of variable to append
    if datatype == str: datakey = Datatype.STRING
    if datatype == int: datakey = Datatype.INTEGER
    if datatype == float: datakey = Datatype.FLOAT
    if datatype == bool: datakey = Datatype.BOOLEAN

    with open(r".ez", "a") as file:
        if data == {}:
            file.write(f"{datakey} {identifier.upper()} {value}")
        else:
            file.write(f"\n{datakey} {identifier.upper()} {value}")

    load_ez()  # Reload the data file, so it doesn't show previous values


def remove_item(item: str):  # Removes item from .ez file
    try:
        item = data[item]
    except KeyError:
        raise KeyError("Key doesn't exist in .ez file")  # Look into .ez file and check if variable exists there

    with open(r".ez", 'r') as file:
        lines = file.readlines()

    with open(r".ez", 'w') as file:
        for number, line in enumerate(lines):
            if number not in [item["Line"]]:
                file.write(line)

    load_ez()  # Reload the data file, so it doesn't show previous values
