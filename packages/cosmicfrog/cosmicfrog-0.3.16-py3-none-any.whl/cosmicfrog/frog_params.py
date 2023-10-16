
POSSIBLE_TYPES = ["int",        # User enters an integer
                   "double",    # User enters a double
                   "string"     # User enters a string
                 ]

#Note: Type can also be list of strings: [Option1, Option2] which requires the user to select


class Params:
    """
        A helper class to represent a set of parameters for a CF Model Function.

        Attributes
        ----------
        None
        
        Methods
        -------
        add - Adds a new parameter
        result - Returns all added parameters as a string
    """

    def __init__(self, params : str = None):
        
        self.__params = []
        
        # Note: No validation on params passed here, is responsibility of the running script to validate
        if params is not None:
            self.__loaded_params = params
            self.model_name = self.__loaded_params.pop(0)

    def __getitem__(self, index):
        return self.__loaded_params[index]
    
    def __is_valid_param_type(self, param_type: str) -> bool:

        if param_type in POSSIBLE_TYPES:
            return True
            
        if param_type.startswith('[') and param_type.endswith(']'):
                return True
        
        return False
                     

    def add(self, name: str, description: str, default : any, param_type: str) -> None:
        """Add a new parameter.

        Args:
            name: the name of the parameter to add.
            description: a user friendly description of the parameter
            default: default value of the parameter
            param_type: the type of the parameter
        Returns:
            None.
        Raises:
            ValueError if the type does not validate as a type
        """

        name = name.strip()
        description = description.strip()
        param_type = param_type.strip()
        if not param_type.startswith("["):
            param_type = param_type.lower()

        if not self.__is_valid_param_type(param_type):
            raise ValueError(f"Invalid param type: {param_type}")
       
        self.__params.append({"Name": name, "Description": description, "Value": default, "Type": param_type})

    def result(self):
        """Returns the parameter list as a string.
        
        Args:
            None.
        Returns:
            String representation of added parameters.
        """
        return self.__params