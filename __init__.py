# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "UV-Colorizer",
    "author" : "Rouven Bröckelmann",
    "description" : "Colorize with texture-based color palettes and zero-scaled UVs : Edited from Christian Schnoor",
    "blender" : (4, 00, 0),
    "version" : (0, 0, 5),
    "location" : "",
    "warning" : "",
    "category" : "UV"
}

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()
