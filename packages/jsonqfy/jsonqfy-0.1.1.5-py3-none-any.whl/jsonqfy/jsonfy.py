import re
import os
import json
from pathlib import Path

from pprint import pprint
import threading

import re
import os
import json
from pathlib import Path

from pprint import pprint
import threading

class JsonFy:
    @classmethod
    def format_dictionary_keys(cls, data, bullet="-", custom_format_func=None, indentation_func=None):
        """
        Format the keys of a (possibly nested) dictionary with custom keys based on the provided options.

        Args:
        - data (dict): The original dictionary to be modified.
        - bullet (str): The bullet string used for indentation.
        - custom_format_func (callable): A function to customize the key formatting.
            * It receives two arguments:
                - key (str): The original dictionary key.
                - value: The value associated with the key in the dictionary.
            * It should return a formatted key (str).
        - indentation_func (callable): A function to determine the indentation.
            * It receives one argument:
                - depth (int): The nesting depth for the current dictionary level.
            * It should return a string representing the desired indentation.

        Returns:
        - list: A list of formatted keys.
        """

        formatted_keys = []

        # Default indentation function if none is provided
        if indentation_func is None:
            indentation_func = lambda depth: "|   " * depth

        # Default custom format function if none is provided
        if custom_format_func is None:
            custom_format_func = lambda key, value: key

        # Function to format a key
        def format_key(key, value, depth):
            indentation_str = indentation_func(depth)
            formatted_key = custom_format_func(key, value)
            if formatted_key is not None:
                return f"{indentation_str}{bullet} {formatted_key}"
            return None

        # Recursive function to traverse the dictionary and format the keys
        def recursive_format(dictionary, depth):
            last_value = dictionary
            for key, value in dictionary.items():
                formatted_key = format_key(key, last_value, depth)
                if formatted_key is not None:
                    formatted_keys.append(formatted_key)
                if isinstance(value, dict):
                    recursive_format(value, depth + 1)
                last_value = value

        # Start the recursive process
        recursive_format(data, 0)
        return formatted_keys


    @classmethod
    def replace_nested_dict_keys(cls, data, key_mapping):
        """
        Replace keys in a nested dictionary according to the provided mapping.

        Args:
        - data (dict): The original dictionary to be modified.
        - key_mapping (dict): A dictionary specifying the key replacements.

        Returns:
        - dict: A new dictionary with keys replaced according to the mapping.
        """

        # Initialize a new dictionary that will contain the replaced keys
        modified_data = {}

        # Iterate over the keys and values of the original dictionary
        for key, value in data.items():
            # If the value is another dictionary, recursively call the function to replace its keys
            if isinstance(value, dict):
                modified_value = cls.replace_nested_dict_keys(value, key_mapping)
            else:
                # Otherwise, keep the value unchanged
                modified_value = value

            # Replace the key if it's in the mapping, otherwise keep the original key
            modified_key = key_mapping.get(key, key)
            modified_data[modified_key] = modified_value

        # Return the new dictionary with replaced keys
        return modified_data


    @classmethod
    def insert_nested_keys_values(cls, data, value_function):
        """
        Replaces nested values in a dictionary based on the provided value function.

        Args:
            data (dict or list): The original dictionary to be modified.
            value_function (callable): A function that takes two arguments:
                - key (str): The current key in the dictionary.
                - value: The value associated with the key in the dictionary.
              The function should return:
                - The replacement value for the current key, or
                - None, to keep the current value unchanged.

        Returns:
            dict: A new dictionary with the values replaced as specified by the value_function.
        """

        if not isinstance(data, (dict, list) ):
          raise ValueError("data must be a dict or list(dict)")


        modified_data = data.copy()


        def recursive_insertion(dct):
            if not isinstance(dct, dict):
                raise ValueError("data must be a dict")
            keys_to_modify = list(dct.keys())
            for key in keys_to_modify:
                value = dct[key]
                new_value = value_function(key, value)
                if new_value is not None:
                    dct[key] = new_value

                if isinstance(dct[key], dict):
                    recursive_insertion(dct[key])
                elif isinstance(dct[key], list):
                    for item in value:
                        if isinstance(item, dict):
                            recursive_insertion(item)

        if isinstance(modified_data, dict):
            recursive_insertion(modified_data)
        elif isinstance(modified_data, list):
            for item in modified_data:
                recursive_insertion(item)

        return modified_data


    @classmethod
    def query(cls, criteria, data_structure):
        """
        Filters structured data using the specified criteria.

        This function allows you to extract specific fields from structured data represented
        as nested dictionaries or lists. The provided criteria are used to filter the data and
        return only the corresponding fields.

        Args:
        - criteria (dict | list | bool | callable): The criteria to be used for filtering.
          - If a dictionary, the function will return a new dictionary with corresponding fields.
          - If a list, it will return a list of filtered data.
          - If True, it will return the original data without filtering.
          - If a callable, it will apply the function to the respective value in the dictionary.

        - data_structure (dict | list): The structured data to be parsed.

        Returns:
        - dict | list | None: The filtered data as per the provided criteria or None if the criteria
          is neither a dictionary nor a list.

        Examples:
            # Usage with dictionary and lambda function
            data = {
                "name": "John",
                "age": 30,
                "address": {"city": "New York", "state": "NY"},
            }
            criteria = {"name": True, "address": {"city": lambda x: x.upper()}}
            result = query(criteria, data)

            # Usage with list and custom function
            data = [{"name": "John"}, {"name": "Alice"}]
            criteria = [{"name": True}, {"name": lambda x: x.lower()}]
            result = query(criteria, data)
        """

        if isinstance(criteria, bool):
            if criteria:
                return data_structure
            else:
                raise ValueError("Criteria must be True to include data_structure.")

        if isinstance(data_structure, dict):
            output = {}
            if isinstance(criteria, dict):
                for key, sub_criteria in criteria.items():
                    if key in data_structure:
                        if callable(sub_criteria):
                            output[key] = sub_criteria(data_structure[key])
                        else:
                            output[key] = cls.query(sub_criteria, data_structure[key])
            elif isinstance(criteria, list) and len(criteria) == 1:
                sub_criteria = criteria[0]
                for key, value in data_structure.items():
                    if key in sub_criteria:
                        filtered_value = (
                            sub_criteria[key](value) if callable(sub_criteria[key]) else
                            cls.query(sub_criteria[key], value) if isinstance(value, (dict, list)) else
                            value
                        )
                        output[key] = filtered_value
            return output

        elif isinstance(data_structure, list) and criteria:
            sub_criteria = criteria[0]
            if isinstance(sub_criteria, dict):
                return [cls.query(sub_criteria, item) for item in data_structure]
            elif callable(sub_criteria):
                return [sub_criteria(item) for item in data_structure]

        return None



    @staticmethod
    def save_dict_as_json_to_folder(dictionary, folder_path, file_name):
        """
        Save a dictionary as a JSON formatted file within a specified folder.

        Args:
            dictionary (dict): The dictionary to be saved as JSON.
            folder_path (str): The path to the folder where the file will be saved.
            file_name (str): The name of the file to be created.

        Raises:
            FileNotFoundError: If the specified folder doesn't exist.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

        full_path = os.path.join(folder_path, file_name)

        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)


    @staticmethod
    def read_json_file(file_path: str) -> dict:
        """
        Read a JSON file and return its content as a Python dictionary.

        Args:
            file_path (str): The path to the JSON file to be read.

        Returns:
            dict: A dictionary representing the content of the JSON file.

        Raises:
            FileNotFoundError: If the file is not found.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"The file '{file_path}' was not found.")

        try:
            with path.open('r', encoding='utf-8') as file:
                json_content = json.load(file)
                return json_content
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON: {str(e)}", e.doc, e.pos)



    @staticmethod
    def create_nested_dict_from_paths(entries, path_key=None, content_keys=None, value_name="content", use_multithreading=False, split= "/"):
        """
        Constructs a nested dictionary from a list of paths and their associated content.

        Args:
            entries (list): Data entries for processing.
            path_key (str, optional): Key for the path if input data is in the first format. Defaults to None.
            content_keys (list, optional): List of content keys. Defaults to None.
            value_name (str, optional): Default name for the content key. Defaults to "content".
            use_multithreading (bool, optional): If True, utilizes multithreading to process entries. Defaults to False.

        Returns:
            dict: A nested dictionary based on the paths.

        Note:
            The function assumes either of the two formats for the input 'entries':
            1. List of dictionaries with paths as keys and associated content.
            2. List of dictionaries where path and content are separate keys.
        """
        def process_entry(entry, result, path_key, content_keys, value_name):
            if path_key and content_keys:
                path = entry[path_key]
                content = {value_name: {key: entry[key] for key in content_keys if key in entry}}
            else:
                path, main_content = list(entry.items())[0]
                content = {value_name: main_content}

            path_parts = path.split(split)
            current_dict = result

            for part in path_parts[:-1]:
                current_dict = current_dict.setdefault(part, {})

            if path_parts[-1] in current_dict:
                for key, value in content.items():
                    if key in current_dict[path_parts[-1]]:
                        if not isinstance(current_dict[path_parts[-1]][key], list):
                            current_dict[path_parts[-1]][key] = [current_dict[path_parts[-1]][key]]
                        current_dict[path_parts[-1]][key].append(value)
                    else:
                        current_dict[path_parts[-1]][key] = value
            else:
                current_dict[path_parts[-1]] = content

        result = {}

        if use_multithreading:
            threads = []
            for entry in entries:
                t = threading.Thread(target=process_entry, args=(entry, result, path_key, content_keys, value_name))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        else:
            for entry in entries:
                process_entry(entry, result, path_key, content_keys, value_name)

        return result


    @classmethod
    def extract_paths_and_content_from_dict(cls,
                                            input_dict,
                                            separator="/",
                                            content_key="content",
                                            transform_func=None,
                                            _current_path=""):
        """
        Extracts a list of dictionaries representing paths and content from a nested dictionary.

        This function navigates a nested dictionary, constructing paths based on the keys, and captures
        the content associated with a specified key. Additionally, the function offers an option to
        transform the content using a provided function.

        Args:
            input_dict (dict): The dictionary to be processed.
            separator (str, optional): The delimiter used between segments of the path. Defaults to "/".
            content_key (str, optional): The key identifying the content. Defaults to "content".
            transform_func (callable, optional): A function that takes content as an argument and
                                                returns transformed content. Defaults to None.
            _current_path (str, optional): The current path (used internally for recursion). Defaults to an empty string.

        Returns:
            list: A list of dictionaries, each containing a path and the content after the specified key.

        Example:
            input_dict = {'Document': {'P': {'Test': {'some_key': 'content'}}}}
            result = extract_paths_and_content_from_dict(input_dict)
        """
        paths_and_content = []

        for key, value in input_dict.items():
            current_path = _current_path if key == content_key else _current_path + separator + key

            if isinstance(value, dict):
                content = value
                if transform_func:
                    content = transform_func(content)

                if key == content_key:
                    paths_and_content.append({"path": current_path, "content": content})
                else:
                    paths_and_content.extend(
                        cls.extract_paths_and_content_from_dict(
                            value, separator, content_key, transform_func, current_path
                        )
                    )
            else:
                content = value
                if transform_func:
                    content = transform_func(content)

                paths_and_content.append({"path": current_path, "content": content})

        return paths_and_content

    @staticmethod
    def get_nested_values(data, key_path):
        """
        Accesses nested values within a dictionary using a path of keys which can contain regular expressions.

        This function is designed to delve deep into nested structures, pulling out values that match a
        specified path of keys. Each segment of the path may also be a regular expression, allowing
        for flexible and pattern-based searching.

        Args:
            data (dict): The dictionary from which values will be accessed.
            key_path (str): The path of keys in the format "A/B/C", where segments can be regular expressions.

        Returns:
            list: A list of values corresponding to the key path or an empty list if no match is found.

        Example:
            nested_data = {
                "A": {
                    "B1": {"C": "value1"},
                    "B2": {"C": "value2"}
                }
            }
            result = get_nested_values(nested_data, "A/B1/C")  # Returns: ["value1"]
        """
        keys = key_path.split('/')
        current_data = [data]

        try:
            for key in keys:
                new_data = []
                for item in current_data:
                    if isinstance(item, dict) and key in item:
                        new_data.append(item[key])
                    elif isinstance(item, list):
                        for subitem in item:
                            if isinstance(subitem, dict) and key in subitem:
                                new_data.append(subitem[key])
                current_data = new_data
        except (KeyError, TypeError):
            return []

        return current_data


    @staticmethod
    def find_keys_by_regex(data, regex, return_type="dict"):
        """
        Searches for dictionary keys that match a given regular expression.

        Args:
            data (dict): The dictionary to be searched.
            regex (str): The regular expression to be matched.
            return_type (str, optional): Specifies the type of return value - "dict" for a nested dictionary
                                        or "list" for a list of matched key paths. Defaults to "dict".

        Returns:
            dict or list: Depending on the `return_type`, either a nested dictionary containing matched keys
                          or a list of matched key paths.
        """
        if return_type not in ["dict", "list"]:
            raise ValueError("return_type must be either 'dict' or 'list'.")

        if return_type == "dict":
            result = {}
        else:
            result = []

        def search_keys(item, path=[]):
            if isinstance(item, dict):
                for key, value in item.items():
                    new_path = path + [key]
                    if isinstance(value, (dict, list)):
                        search_keys(value, new_path)
                    if re.search(regex, str(key)):
                        if return_type == "dict":
                            current = result
                            for p in new_path[:-1]:
                                current = current.setdefault(p, {})
                            current[new_path[-1]] = value
                        else:
                            result.append('/'.join(map(str, new_path)))

            elif isinstance(item, list):
                for i, element in enumerate(item):
                    new_path = path + [i]
                    search_keys(element, new_path)

        search_keys(data)
        return result

    @staticmethod
    def find_values_by_depth(data, regex):
        """
        Searches for values within a nested dictionary or list structure that match
        a given regular expression and returns their paths.

        Args:
            data (dict or list): The data structure to be searched.
            regex (str): The regular expression to be matched.

        Returns:
            list of tuple: A list of tuples where the first element of each tuple
                          is the path (as a list of keys) to the matching value,
                          and the second element is the matching value itself.

        Example:
            data = {
                'a': {
                    'b': 'value1',
                    'c': ['value2', 'match1']
                },
                'd': 'match2'
            }

            find_values_by_depth(data, r'match\d')
            -> [(['a', 'c', 1], 'match1'), (['d'], 'match2')]
        """
        results = []

        def search_depth(item, path=[]):
            if isinstance(item, dict):
                for key, value in item.items():
                    new_path = path + [key]
                    if isinstance(value, (dict, list)):
                        search_depth(value, new_path)
                    elif re.match(regex, str(value)):
                        results.append((new_path, value))
            elif isinstance(item, list):
                for i, element in enumerate(item):
                    new_path = path + [i]
                    search_depth(element, new_path)

        search_depth(data)
        return results




# # # Example usage with the new class and methods
# my_dict = {
#     "A": {
#         "B": {
#             "C": {
#                 "Text": "blalbalbal"
#             },
#             "D": "Value2"
#         },
#         "E": "Value3"
#     },
#     "F": {
#         "G": {
#             "H": "Value4"
#         },
#         "I": 3
#         }
# }

# def custom_get_indent(depth):
#     return "--" + str(depth) + "--"

# def custom_name_function(key, value):
#     custom_key = {
#         'A': 'Custom A'
#     }
#     if key in custom_key:
#         return custom_key[key]
#     elif key == 'Text':
#         return value[key]
#     else:
#         return key  # If the key does not exist, return the original key name

# formatter = JsonFy()
# formatted_keys = formatter.format_dictionary_keys(my_dict,
#                                                   bullet="-",
#                                                   custom_format_func=custom_name_function,
#                                                   indentation_func=custom_get_indent)
# # bullet="-", custom_format_func=None, indentation_func=None

# formatted_keys_string = "\n".join(formatted_keys)
# print(formatted_keys_string)

# print('---'*100)
# key_mapping = {"C": "New C", "subchave1": "new_subkey1"}
# pprint(formatter.replace_nested_dict_keys(my_dict, key_mapping))



# print('---'*100)


# # # Defina uma função que recebe o valor da hierarquia atual e retorna uma nova chave e valor
# def custom_value_func_embed(key, value):
#     if 'Text' in value.keys():
#         return {
#             'Text':'12',
#             'Embed':'312',
#                 }

# # # Defina uma função que recebe o valor da hierarquia atual e retorna uma nova chave e valor



# # # Adicionando uma nova subchave e valor sob a chave 'C' com base na função personalizada
# test = formatter.insert_nested_keys_values(my_dict, custom_value_func_embed)
# pprint(test)



# print('---'*100)


# def custom_fun(x):
#   return formatter.insert_nested_keys_values(x, custom_value_func_embed)

# query = {
#     'A': {
#         "B": custom_fun,
#         'E':True
#         },
#     'F': True
# }

# test = formatter.query(query, my_dict)
# pprint(test)


# print('---'*100)


# # # Retorne funções mais complexas, como retornar todos os valores como True
# # def custom_value_func(key, value):
#         # return {x: True for x in value.keys()}

# # test = formatter.add_new_subkey_value(my_dict, custom_value_func)
# # pprint(test)

# ## orr

# def custom_value_func(value):
#   for k,v in value.items():
#     if isinstance(v, dict):
#       return {x: custom_value_func(v) for x in value.keys()}
#     else:
#       return True



# query = {key:custom_value_func for key in my_dict.keys()}
# test = formatter.query(query, my_dict)
# # pprint(test)

# import json

# print(json.dumps(test, indent=2))

# print('---'*100)

# # Exemplo de uso
# my_dict = {
#     "A": {
#         "B": [
#             {"C": {"Text": "blalbalbal"}},
#             {"C": {"Text": "other text"}},
#         ],
#         "E": ["Value3", "Value3"]
#     }
# }

# key_path = "A/B/C"
# results = formatter.get_nested_values(my_dict, key_path)

# print(results)  # Deve imprimir ['blalbalbal', 'other text']
