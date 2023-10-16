import re

def dance(template_string: str, local_dict: dict) -> str:
    # Regular expression to find function calls or variables in {{}}
    pattern = r"\{\{(.*?)\}\}"

    # Find all matches in the template string
    matches = re.findall(pattern, template_string)

    for match in matches:
        # Check if it's a function call
        if '(' in match and ')' in match:
            function_name, parameters = match.split('(')
            parameters = parameters.rstrip(')')

            # Execute the function with the parameters and get the result
            try:
                result = eval(f"{function_name}({parameters})", globals(), local_dict)
            except Exception as e:
                return f"The function failed to bring the data: {str(e)}"

        else:
            # It's a variable
            variable_name = match

            # Get the value of the variable
            try:
                result = eval(variable_name, globals(), local_dict)
            except Exception as e:
                return f"The variable failed to bring the data: {str(e)}"

        # Replace the function call or variable in the template string with the result
        template_string = template_string.replace(f"{{{{{match}}}}}", str(result))

    return template_string


def hello(name: str) -> str:
    return f"Yo me llamo {name}"

if __name__ == "__main__":
    template_string = "My name is Marcelo, but in Spanish {{hello('Marcelo')}}"
    print(dance(template_string))
