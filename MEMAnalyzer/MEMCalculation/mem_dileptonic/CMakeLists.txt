# Tutorials and examples for MoMEMta, the Modular Matrix Element Method implementation
#
# Copyright (C) 2016  Universite catholique de Louvain (UCL), Belgium
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


add_executable(mem_dileptonic "mem_dileptonic.cc")

target_link_libraries(mem_dileptonic momemta::momemta)
# The TTbar example uses TreePlayer
target_link_libraries(mem_dileptonic ${ROOT_TREEPLAYER_LIBRARY})

set_target_properties(mem_dileptonic PROPERTIES OUTPUT_NAME
      "mem_dileptonic.exe")

add_executable(mem_comparison_dileptonic "mem_comparison_dileptonic.cc")
target_link_libraries(mem_comparison_dileptonic momemta::momemta)
target_link_libraries(mem_comparison_dileptonic ${ROOT_TREEPLAYER_LIBRARY})
set_target_properties(mem_comparison_dileptonic PROPERTIES OUTPUT_NAME
            "mem_comparison_dileptonic.exe")
