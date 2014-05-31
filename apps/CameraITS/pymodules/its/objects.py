# Copyright 2013 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import os.path
import sys
import re
import json
import tempfile
import time
import unittest
import subprocess
import math

def int_to_rational(i):
    """Function to convert Python integers to Camera2 rationals.

    Args:
        i: Python integer or list of integers.

    Returns:
        Python dictionary or list of dictionaries representing the given int(s)
        as rationals with denominator=1.
    """
    if isinstance(i, list):
        return [{"numerator":val, "denominator":1} for val in i]
    else:
        return {"numerator":i, "denominator":1}

def float_to_rational(f, denom=128):
    """Function to convert Python floats to Camera2 rationals.

    Args:
        f: Python float or list of floats.
        denom: (Optonal) the denominator to use in the output rationals.

    Returns:
        Python dictionary or list of dictionaries representing the given
        float(s) as rationals.
    """
    if isinstance(f, list):
        return [{"numerator":math.floor(val*denom+0.5), "denominator":denom}
                for val in f]
    else:
        return {"numerator":math.floor(f*denom+0.5), "denominator":denom}

def rational_to_float(r):
    """Function to convert Camera2 rational objects to Python floats.

    Args:
        r: Rational or list of rationals, as Python dictionaries.

    Returns:
        Float or list of floats.
    """
    if isinstance(r, list):
        return [float(val["numerator"]) / float(val["denominator"])
                for val in r]
    else:
        return float(r["numerator"]) / float(r["denominator"])

def manual_capture_request(sensitivity, exp_time, linear_tonemap=False):
    """Return a capture request with everything set to manual.

    Uses identity/unit color correction, and the default tonemap curve.
    Optionally, the tonemap can be specified as being linear.

    Args:
        sensitivity: The sensitivity value to populate the request with.
        exp_time: The exposure time, in nanoseconds, to populate the request
            with.
        linear_tonemap: [Optional] whether a linear tonemap should be used
            in this request.

    Returns:
        The default manual capture request, ready to be passed to the
        its.device.do_capture function.
    """
    req = {
        "android.control.mode": 0,
        "android.control.aeMode": 0,
        "android.control.awbMode": 0,
        "android.control.afMode": 0,
        "android.control.effectMode": 0,
        "android.sensor.frameDuration": 0,
        "android.sensor.sensitivity": sensitivity,
        "android.sensor.exposureTime": exp_time,
        "android.colorCorrection.mode": 0,
        "android.colorCorrection.transform":
                int_to_rational([1,0,0, 0,1,0, 0,0,1]),
        "android.colorCorrection.gains": [1,1,1,1],
        "android.tonemap.mode": 1,
        }
    if linear_tonemap:
        req["android.tonemap.mode"] = 0
        req["android.tonemap.curveRed"] = [0.0,0.0, 1.0,1.0]
        req["android.tonemap.curveGreen"] = [0.0,0.0, 1.0,1.0]
        req["android.tonemap.curveBlue"] = [0.0,0.0, 1.0,1.0]
    return req

def auto_capture_request():
    """Return a capture request with everything set to auto.
    """
    return {
        "android.control.mode": 1,
        "android.control.aeMode": 1,
        "android.control.awbMode": 1,
        "android.control.afMode": 1,
        "android.colorCorrection.mode": 1,
        "android.tonemap.mode": 1,
        }

class __UnitTest(unittest.TestCase):
    """Run a suite of unit tests on this module.
    """

    # TODO: Add more unit tests.

    def test_int_to_rational(self):
        """Unit test for int_to_rational.
        """
        self.assertEqual(int_to_rational(10),
                         {"numerator":10,"denominator":1})
        self.assertEqual(int_to_rational([1,2]),
                         [{"numerator":1,"denominator":1},
                          {"numerator":2,"denominator":1}])

if __name__ == '__main__':
    unittest.main()

