# propagate_tle.py - Propagate many TLEs in parallel.
# Copyright (C) 2019-2020 University of Texas
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

import sys
import argparse
from datetime import datetime, timedelta
from orbdetpy import configure
from orbdetpy.conversion import get_J2000_epoch_offset, get_UTC_string
from orbdetpy.propagation import propagate_orbits

day0 = datetime.today()
day1 = day0 + timedelta(days=1)
timefmt = "%Y-%m-%dT%H:%M:%S.%fZ"

parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("tle-file", help="Input TLE file", type=argparse.FileType("r"))
parser.add_argument("--start-time", help="Propagation start time",
                    default=datetime(day0.year, day0.month, day0.day).strftime(timefmt))
parser.add_argument("--end-time", help="Propagation end time",
                    default = datetime(day1.year, day1.month, day1.day).strftime(timefmt))
parser.add_argument("--step-size", help="Step size [sec.]", type=float, default=900.0)
if (len(sys.argv) == 1):
    parser.print_help()
    exit(1)

args = parser.parse_args()
start = get_J2000_epoch_offset(args.start_time)
end = get_J2000_epoch_offset(args.end_time)
config, elements = [], [l for l in getattr(args, "tle-file").read().splitlines()
                        if l.startswith("1") or l.startswith("2")]
for i in range(0, len(elements), 2):
    config.append(configure(prop_start=start, prop_initial_TLE=elements[i:i+2],
                            prop_end=end, prop_step=args.step_size))

try:
    i = 0
    for o in propagate_orbits(config):
        print("\nObject {}:".format(elements[i][2:7]))
        i += 2
        for m in o.array:
            print(get_UTC_string(m.time), m.true_state)
except Exception as exc:
    print(exc)
