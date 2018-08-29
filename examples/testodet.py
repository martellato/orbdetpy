# testodet.py - Example program for orbit determination.
# Copyright (C) 2018 Shiva Iyer <shiva.iyer AT utexas DOT edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orbdetpy import init
init()

if (len(sys.argv) < 4):
    print("Usage: python %s config_file measurement_file output_file [EKF|UKF]"
          % sys.argv[0])
    exit()

if (len(sys.argv) > 4 and sys.argv[4].lower() == "ekf"):
    filt = "EKF"
    from orbdetpy.ekf import estimate
else:
    filt = "UKF"
    from orbdetpy.ukf import estimate

with open(sys.argv[1], "r") as f:
    config = json.load(f)

print("%s start : %s" % (filt, time.strftime("%Y-%m-%d %H:%M:%S")))
with open(sys.argv[2], "r") as fin:
    res = estimate(config, json.load(fin))
    with open(sys.argv[3], "w") as fout:
        json.dump(res, fout, indent = 1)
print("%s end   : %s" % (filt, time.strftime("%Y-%m-%d %H:%M:%S")))