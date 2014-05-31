# Copyright 2014 The Android Open Source Project
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

import its.image
import its.device
import its.objects
import os.path

def main():
    """Test capturing a single frame as both RAW and YUV outputs.
    """
    NAME = os.path.basename(__file__).split(".")[0]

    with its.device.ItsSession() as cam:
        props = cam.get_camera_properties()

        cam.do_3a()

        req = its.objects.auto_capture_request()
        cap_raw, cap_yuv = cam.do_capture(req, cam.CAP_RAW_YUV)

        img = its.image.convert_capture_to_rgb_image(cap_yuv)
        its.image.write_image(img, "%s_yuv.jpg" % (NAME))

        img = its.image.convert_capture_to_rgb_image(cap_raw, props=props)
        its.image.write_image(img, "%s_raw.jpg" % (NAME), True)

if __name__ == '__main__':
    main()

