# Sapio Native Tools allows users to read in/out objects against native lib.
from sapiopylib.sapio_input_data import SapioInputData
import pickle

sapio_input_data = SapioInputData()


def get_sapio_input():
    """
    Get the Sapio Input Data object. If it has not been retrieved yet, retrieve it.
    If it has been retrieved, then return what's in the cache.
    :return: The sapio input object fed from Sapio app into this script.
    """
    return sapio_input_data


def set_output_object(output_object):
    """
    Set the output object data, which will upload immediately to Sapio for consumption.
    However, Sapio will not consume it until the script terminates or times out.
    """
    if output_object is None:
        return
    input_data: SapioInputData = get_sapio_input()
    output_file = input_data.get_output_file()
    with open(output_file, "wb") as fp:
        pickle.dump(output_object, fp, protocol=2)
