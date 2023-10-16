from typing import Dict

from docstring_parser import parse

TYPE_MAP: Dict[str, str] = {
    "str": "string",
    "int": "integer",
    "float": "float",
    "list": "list",
}


def chatgpt_wrapper(func: callable):
    """Wraps a function with a docstring and assigns the method chatgpt_function to the function wrapper.

    Args:
        func (callable): The function or method to wrap.

    Returns:
        callable: The wrapped function.

    Example:
        from chatgpt_function import chatgpt_wrapper
        @chatgpt_function
         def my_function(my_arg: str) -> str:
             '''This is my function.

             Args:
                 my_arg (str): This is my argument.

             Returns:
                 str: This is my return value.
             '''
             return "Hello World!" + my_arg
         my_function.chatgpt_function()
        {
            "name": "my_function",
            "description": "This is my function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "my_arg": {
                        "type": "string",
                        "description": "This is my argument."
                    }
                },
                "required": [
                    "my_arg"
                ]
            },
            "returns": [
                {
                    "description": "This is my return value.",
                    "type": "string"
                }
            ]
        }
        my_function("!")
        'Hello World!!'
        # usage with ChatGPT
        from openai import ChatCompletion
        response = ChatCompletion.create(messages=messages,
                                         functions=[my_function.chatgpt_function()],
                                         **kwargs)
    """
    if not callable(func):
        raise TypeError("Input must be a callable function or method")

    if func.__doc__ is None:
        raise ValueError(f"Function '{func.__name__}' must have a docstring")
    doc = parse(func.__doc__)

    parameters = []
    for param in doc.params:
        param_name = param.arg_name
        param_type = TYPE_MAP.get(param.type_name, "any")
        param_desc = param.description
        parameters.append(
            {"name": param_name, "type": param_type, "description": param_desc}
        )

    returns = []
    if doc.returns:
        return_desc = doc.returns.description
        return_type = TYPE_MAP.get(doc.returns.type_name, "any")
        returns.append({"description": return_desc, "type": return_type})
    method_info = {
        "name": func.__name__,
        "description": doc.short_description,
        "parameters": {
            "type": "object",
            "properties": dict(zip(map(lambda x: x["name"], parameters), parameters)),
            "required": list(map(lambda x: x["name"], parameters)),
        },
        "returns": returns,
    }
    # delete name from each parameter in parameters
    for parameter in method_info["parameters"]["properties"].values():
        del parameter["name"]

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    def chatgpt_function():
        return method_info

    wrapper.chatgpt_function = chatgpt_function
    return wrapper
