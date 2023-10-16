import json
import logging
import os
import re

import numpy as np
from _ctypes import PyObj_FromPtr  # see https://stackoverflow.com/a/15012814/355230
from tabulate import tabulate

# class NoIndent(object):
# 	""" Value wrapper. """
# 	def __init__(self, value):
# 		if not isinstance(value, (list, tuple)):
# 			raise TypeError('Only lists and tuples can be wrapped')
# 		self.value = value

log = logging.getLogger(__name__)
log.setLevel("INFO")


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = "@@{}@@"  # Unique string pattern of NoIndent object ids.
    regex = re.compile(FORMAT_SPEC.format(r"(\d+)"))  # compile(r'@@(\d+)@@')

    def __init__(self, **kwargs):
        # Keyword arguments to ignore when encoding NoIndent wrapped values.
        ignore = {"cls", "indent"}

        # Save copy of any keyword argument values needed for use here.
        self._kwargs = {k: v for k, v in kwargs.items() if k not in ignore}
        super().__init__(**kwargs)

    def default(self, obj):
        # return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
        return (
            self.FORMAT_SPEC.format(id(obj))
            if isinstance(obj, list)
            else super().default(obj)
        )

    def iterencode(self, obj, **kwargs):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.

        # Replace any marked-up NoIndent wrapped values in the JSON repr
        # with the json.dumps() of the corresponding wrapped Python object.
        for encoded in super().iterencode(obj, **kwargs):
            match = self.regex.search(encoded)
            if match:
                id = int(match.group(1))
                no_indent = PyObj_FromPtr(id)
                json_repr = json.dumps(no_indent.value, **self._kwargs)
                # Replace the matched id string with json formatted representation
                # of the corresponding Python object.
                encoded = encoded.replace(f'"{format_spec.format(id)}"', json_repr)

            yield encoded


def save_dict_list(path, output):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sorted_output = []
    serial_numbers = []
    isAnalysis = False
    # Separate into separate lists for each chip if saving measurement output
    for out in output:
        if isAnalysis and not ("passed" in out):
            log.error(
                "List of dictionaries being saved to output contain both measurement and output formats. Please fix."
            )
            return
        if "passed" in out:  # is analysis output
            sorted_output += [out]
            isAnalysis = True
        elif out.get("serialNumber") in serial_numbers:
            sorted_output[serial_numbers.index(out.get("serialNumber"))] += [out]
        else:
            serial_numbers += [out.get("serialNumber")]
            sorted_output += [[out]]
    with open(path, "w") as fp:
        json.dump(sorted_output, fp, cls=MyEncoder, indent=4)


def load_json(path):
    with open(path) as serialized:
        inputdata = json.load(serialized)
    alldf = []
    # Can read measurement jsons (nested list) or analysis jsons (1D list)
    for chip in inputdata:
        if isinstance(chip, list):
            for _dict in chip:
                alldf += [outputDataFrame(_dict=_dict)]
        else:
            alldf += [outputDataFrame(_dict=chip)]
    return alldf


def convert_name_to_serial(chipName):
    serialPrefix = "20UPGFC"  # This will change to 20UPGFW for real wafers
    try:
        chip_number = str(int(chipName, base=16))
        # Add preceding zeros
        while len(chip_number) < 7:
            chip_number = "0" + chip_number
        return serialPrefix + str(chip_number)
    except Exception:
        print(
            f"Warning: Can't convert chip name ({chipName}) into serial number, setting serial number to {chipName}"
        )
        return chipName


def convert_serial_to_name(chipSerial):
    # Assumes prefix is of length 7 (i.e. "20UPGFC")
    try:
        # Remove prefix and preceding 0's
        chipSerial = chipSerial[7:]
        chipSerial = chipSerial.lstrip("0")
        chipName = hex(int(chipSerial))
    except Exception:
        chipName = chipSerial
        print(
            f"Warning: Can't convert chip serial number ({chipSerial}) into name, setting chip name to {chipSerial}"
        )
    return chipName


# Returns module type, given module serial number
def get_type_from_sn(module_sn):
    if "PI" in module_sn:
        if "M1" in module_sn:
            return "quad"
        return "triplet"
    if "PG" in module_sn:
        return "quad"
    print(
        f"Unknown module type ({module_sn}) - will not separate inner from outer pixels in disconnected bump analysis"
    )
    return "unknown"


# requires the connectivity file name to be "<ATLAS_SN>_<layer>_<suffix>.json" as output from the database tool
def get_sn_from_connectivity(fileName):
    try:
        moduleSN = os.path.basename(fileName).split("_")[0]
        check_sn_format(moduleSN)
    except Exception as e:
        print(f"Error: Cannot extract module serial number from path ({fileName}): {e}")
        exit()
    return moduleSN


def get_layer_from_sn(sn):
    check_sn_format(sn)
    if "PIMS" in sn or "PIR6" in sn:
        return "L0"
    elif "PIM0" in sn or "PIR7" in sn:
        return "L0"  # "R0"
    elif "PIM5" in sn or "PIR8" in sn:
        return "L0"  # "R0.5"
    elif "PIM1" in sn or "PIRB" in sn:
        return "L1"
    elif "PG" in sn:
        return "L2"
    else:
        print(f"Error: Cannot recognise {sn}, not a valid module SN.")
        exit()


def get_nlanes_from_sn(sn):
    check_sn_format(sn)
    if "PIMS" in sn or "PIR6" in sn:
        return 4  # L0
    elif "PIM0" in sn or "PIR7" in sn:
        return 3  # R0
    elif "PIM5" in sn or "PIR8" in sn:
        return 2  # R0.5
    elif "PIM1" in sn or "PIRB" in sn:
        return 1  # L1
    elif "PG" in sn:
        return 1  # L2-L4
    else:
        print(f"Error: Cannot get the number of lanes from this SN: {sn} \U0001F937")
        exit()


def check_sn_format(sn):
    if len(sn) != 14 or not sn.startswith("20U"):
        print(f"Error: Cannot recognise ATLAS SN {sn}. Please enter a valid ATLAS SN.")
        exit()
    return True


def get_env(key):
    value = os.getenv(key, default=None)
    if value:
        log.info(f"{key} is {value}.")
    else:
        log.warning(f"Variable '{key}' is not set.")
    return value


class qcDataFrame:
    """
    The QC data frame which stores meta data and task data.
    """

    def __init__(self, columns=None, units=None, x=None, _dict=None):
        self._identifiers = {}
        self._meta_data = {}
        self._data = {}
        self._property = {}
        self._parameter = {}
        self._comment = ""
        if _dict:
            self.from_dict(_dict)
            return

        columns = columns or []

        for i, column in enumerate(columns):
            self._data[column] = {
                "X": x[i] if x else False,
                "Unit": units[i] if units else None,
                "Values": [],
            }

    def add_meta_data(self, key, value):
        self._meta_data[key] = value

    def add_data(self, data):
        for key, value in data.items():
            self._data[key]["Values"] += list(value)

    def add_column(self, column, unit=False, x=False, data=None):
        data = data or []
        if column in self._data:
            print(f"Warning: column {column} already exists! Will overwrite.")
        self._data[column] = {"X": x, "Unit": unit, "Values": list(data)}

    def add_property(self, key, value, precision=-1):
        if self._property.get(key):
            print(f"Warning: property {key} already exists! Will overwrite.")
        if precision != -1:
            try:
                value = self._round(key, value, precision)
            except Exception:
                pass
        self._property[key] = value

    def add_parameter(self, key, value, precision=-1):
        if self._parameter.get(key):
            print(f"Warning: parameter {key} already exists! Will overwrite.")
        if precision != -1:
            if type(value) == dict:
                for k, v in value.items():
                    value[k] = self._round(k, v, precision)
            else:
                value = self._round(key, value, precision)
        self._parameter[key] = value

    def _round(self, key, value, precision):
        try:
            if type(value) == list:
                value = np.around(value, precision).tolist()
            else:
                value = round(value, precision)
        except Exception:
            log.warning(f"Unable to round value stored in output file for {key}.")
        return value

    def add_comment(self, comment, override=False):
        if override or self._comment == "":
            self._comment = comment
        else:
            self._comment += ". " + str(comment)

    def __getitem__(self, column):
        return np.array(self._data[column]["Values"])

    def set_unit(self, column, unit):
        self._data[column]["Unit"] = unit

    def get_unit(self, column):
        return self._data[column]["Unit"]

    def set_x(self, column, x):
        self._data[column]["X"] = x

    def get_x(self, column):
        return self._data[column]["X"]

    def __len__(self):
        return max(len(value["Values"]) for value in self._data.values())

    def sort_values(self, by, reverse=False):
        for key, value in self._data.items():
            if key == by:
                continue
            value["Values"] = list(
                next(
                    zip(
                        *sorted(
                            zip(
                                value["Values"], self._data[by]["Values"], strict=False
                            ),
                            key=lambda x: x[1],
                            reverse=reverse,
                        ),
                        strict=False,
                    )
                )
            )
        self._data[by]["Values"].sort(reverse=reverse)

    def get_meta_data(self):
        return self._meta_data

    def get_identifiers(self):
        return {
            k: self._meta_data.get(k)
            for k in (
                "ChipID",
                "Name",
                "ModuleSN",
                "Institution",
                "TestType",
                "TimeStart",
                "TimeEnd",
            )
        }

    def get_properties(self):
        return self._property

    def get_comment(self):
        return self._comment

    def __str__(self):
        text = "Identifiers:\n"
        text += str(json.dumps(self.get_identifiers(), cls=MyEncoder, indent=4))
        text += "\n"
        # text += "Meta data:\n"
        # text += str(json.dumps(self._meta_data, cls=MyEncoder, indent=4))
        # text += "\n"
        table = []
        for key, value in self._data.items():
            table.append(
                [key + (f" [{value['Unit']}]" if value["Unit"] else "")]
                + value["Values"]
            )
        text += tabulate(table, floatfmt=".3f")
        return text

    def to_dict(self):
        _dict = {
            "property": self._property,
            "parameter": self._parameter,
            "comment": self._comment,
            "Measurements": self._data,
            "Metadata": self._meta_data,
        }
        return _dict

    def from_dict(self, _dict):
        self._meta_data = _dict["Metadata"]
        self._identifiers = self.get_identifiers()
        self._data = _dict["Measurements"]
        self._property = _dict["property"]
        self._comment = _dict["comment"]

    def to_json(self):
        _dict = self.to_dict()
        return json.dumps(_dict, cls=MyEncoder, indent=4)

    def save_json(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _dict = self.to_dict()
        with open(path, "w") as fp:
            json.dump(_dict, fp, cls=MyEncoder, indent=4)


class outputDataFrame:
    """
    The output file format, designed to work well with localDB and prodDB
    """

    def __init__(self, _dict=None):
        self._serialNumber = "Unknown"
        self._testType = "Not specified"
        self._subtestType = ""
        self._results = qcDataFrame()  # holds qcDataFrame
        self._passed = "Not specified"
        if _dict:
            self.from_dict(_dict)
            return

    def set_serial_num(self, serial_num=None):
        if serial_num is not None:
            self._serialNumber = serial_num
        else:
            try:
                chipName = self._results._meta_data["Name"]
            except Exception:
                print("Warning: Can't find chip name for serial number conversion")
                return
            self._serialNumber = convert_name_to_serial(chipName)

    def set_test_type(self, test_type=None):
        if test_type is not None:
            self._testType = test_type
        else:
            self._testType = "Not specified"

    def set_subtest_type(self, subtest_type=None):
        if subtest_type is not None:
            self._subtestType = subtest_type
        else:
            self._subtestType = "Not specified"

    def set_pass_flag(self, passed=False):
        self._passed = passed

    def set_results(self, results=None):
        if results is not None:
            self._results = results
        else:
            self._results = qcDataFrame()
        if self._serialNumber == "Unknown":
            self.set_serial_num()

    def get_results(self):
        return self._results

    def to_dict(self, forAnalysis=False):
        _dict = {"serialNumber": self._serialNumber, "testType": self._testType}
        if not forAnalysis:
            _dict.update({"subtestType": self._subtestType})
        all_results = self.get_results().to_dict()
        parameters = all_results.get("parameter")
        all_results.pop("parameter")

        # Write out different information, depending on if we are in measurement or analysis step
        if forAnalysis:
            all_results.pop("Measurements")
            metadata_keep = [
                "MEASUREMENT_VERSION",
                "QC_LAYER",
                "INSTITUTION",
            ]  # Metadata we want to write out
            metadata_keys = list(all_results.get("Metadata").keys())
            for key in metadata_keys:
                if key not in metadata_keep:
                    all_results.get("Metadata").pop(key)
            all_results.pop("comment")
            for key, value in parameters.items():
                all_results[key] = value
            _dict["passed"] = self._passed
        results = {"results": all_results}
        _dict.update(results)
        return _dict

    def save_json(self, path, forAnalysis=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _dict = self.to_dict(forAnalysis)
        with open(path, "w") as fp:
            json.dump(_dict, fp, cls=MyEncoder, indent=4)

    def from_dict(self, _dict):
        self._serialNumber = _dict.get("serialNumber")
        self._testType = _dict.get("testType")
        self._subtestType = _dict.get("subtestType")
        try:
            self._results = qcDataFrame(_dict=_dict.get("results"))
        except Exception:
            self._results = _dict.get("results")
