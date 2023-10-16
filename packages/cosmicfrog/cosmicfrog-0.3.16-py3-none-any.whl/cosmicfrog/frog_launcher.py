import argparse
import json
import inspect
import traceback
import sqlalchemy as sa
from cosmicfrog import FrogModel, Params
from .suppress_stdio import Suppress_stdio
from .frog_platform import OptilogicClient
from .frog_utilitydetails import UtilityDetails

# Handles launch code for utilities (so you don't have to!)

def __parse_args():

    parser = argparse.ArgumentParser(description='This is a Cosmic Frog utility. Visit www.cosmicfrog.com.')

    exclusive_group = parser.add_mutually_exclusive_group(required=True)

    # Usage: either call a function e.g. run, or --details to call both description and parameters and get an info block for 
    # the utility
    exclusive_group.add_argument('--run', action='store_true', help='Run the utility.')
    exclusive_group.add_argument('--details', action='store_true', help='Get the info block for the utility.')

    # Addition information when calling run
    parser.add_argument('--model_connection_string', type=str, help='Frog model connection string.', default=None)
    parser.add_argument('json_data', type=str, nargs='?', default=None, help='The JSON data payload passed to the function.')
    
    return parser.parse_args()

def __call_utility_details(main_globals) -> None:
    """ Calls the details method of a utility, used to populate CF UI with parameters
    """

    details = main_globals.get('details')
    if not details:
        raise ValueError(f"Function 'details' not found.")

    function_params = inspect.signature(details).parameters

    num_params = len(function_params) 

    if num_params != 0:
        raise ValueError(f"Expecting 0 arguments for details function, found {num_params}.")

    # TODO: Error handling, see frogspawn
    with Suppress_stdio(): 
        details = details()

    assert isinstance(details, UtilityDetails)
    assert isinstance(details.category, str)
    assert isinstance(details.description, str)
    assert isinstance(details.params, Params)

    print(details.to_json())


def __call_utility_run(connection_string, data, main_globals):
    """Calls the run function, passing in a model connection and parameters from UI
    """

    func = main_globals.get('run')
    if not func:
        raise ValueError(f"Function 'run' not found.")

    function_params = inspect.signature(func).parameters

    num_params = len(function_params) 

    if num_params != 2:
        raise ValueError(f"Expecting 2 arguments for 'run' function, found {num_params}.")

    params = Params(data)

    print(f"Connecting to : {params.model_name}")

    # If no connection string supplied on command line, assume running in Andromeda
    # and need to pick up connection 
    if connection_string is None:

        oc = OptilogicClient()

        success, connection_string = oc.get_connection_string(params.model_name)

        if not success:
            raise ValueError(f"Cannot get connection string for frog model: {params.model_name}")
        
    engine = sa.create_engine(connection_string)

    # Initialise Frog model (quietly, no console output)
    with Suppress_stdio():
        model = FrogModel(engine=engine)

    func(model, params)


def start_utility(main_globals):
    """
    Passes off control to the requested function in the utility
    """
    try:
        args = __parse_args()

        if args.run:

            data = json.loads(args.json_data) if args.json_data else None

            assert isinstance(data, list), "The data is not a list of parameter values"

            # Note: At a minimum, all utilities need the model name as a parameter
            assert len(data) > 0, "The parameter list is empty"

            __call_utility_run(args.model_connection_string, data, main_globals)

            return
    
        assert(args.details)

        # TODO: Currently the details function does not get a connection, this may change
        return __call_utility_details(main_globals)

    except Exception as e:
        # Handle the exception as needed. For now, just print the error message.
        print(f"An error occurred: {e}")
        traceback.print_exc()
