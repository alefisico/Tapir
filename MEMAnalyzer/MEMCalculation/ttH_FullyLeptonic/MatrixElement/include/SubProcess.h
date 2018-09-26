/*
 *  This file was automatically generated by MoMEMta-MaGMEE,
 *  A MadGraph Matrix Element Exporter plugin for MoMEMta.
 *  
 *  It is subject to MoMEMta-MaGMEE's license and copyright:
 *  
 *  Copyright (C) 2016  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include <vector> 
#include <utility>
#include <functional>

namespace ttH_FullyLeptonic_groupSubprocesses_VLF_Singlet_UFO {

    template<class T>
    struct SubProcess {
        public:
            using Callback = std::function<double(T&)>;
    
            SubProcess(const Callback& callback, bool mirror, const std::vector<std::pair<int, int>>& iniStates, int ncomb, int denom):
                callback(callback), 
                hasMirrorProcess(mirror), 
                initialStates(iniStates), 
                goodHel(ncomb, true), 
                denominator(denom) {
                    // Empty
                }

            void resetHelicities() {
                std::fill(goodHel.begin(), goodHel.end(), true);
            }
    
            Callback callback;
            bool hasMirrorProcess; 
            std::vector<std::pair<int, int>> initialStates; 
            std::vector<bool> goodHel; 
            int denominator;
    
        private:
            SubProcess() = delete;
    }; 

}
