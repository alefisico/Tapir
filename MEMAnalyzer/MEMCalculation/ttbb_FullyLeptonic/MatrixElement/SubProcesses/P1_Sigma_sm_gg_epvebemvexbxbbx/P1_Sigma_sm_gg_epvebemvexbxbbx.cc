// 
// *  This file was automatically generated by MoMEMta-MaGMEE,
// *  A MadGraph Matrix Element Exporter plugin for MoMEMta.
// *
// *  It is subject to MoMEMta-MaGMEE's license and copyright:
// *
// *  Copyright (C) 2016  Universite catholique de Louvain (UCL), Belgium
// *
// *  This program is free software: you can redistribute it and/or modify
// *  it under the terms of the GNU General Public License as published by
// *  the Free Software Foundation, either version 3 of the License, or
// *  (at your option) any later version.
// *
// *  This program is distributed in the hope that it will be useful,
// *  but WITHOUT ANY WARRANTY; without even the implied warranty of
// *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// *  GNU General Public License for more details.
// *
// *  You should have received a copy of the GNU General Public License
// *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
// 

#include <string> 
#include <utility> 
#include <vector> 
#include <map> 

#include <P1_Sigma_sm_gg_epvebemvexbxbbx.h> 
#include <HelAmps_sm.h> 

#include <momemta/ParameterSet.h> 
#include <momemta/SLHAReader.h> 

namespace ttbb_FullyLeptonic_sm 
{

//==========================================================================
// Class member functions for calculating the matrix elements for
// Process: g g > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: u u~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: c c~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: d d~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: s s~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: g g > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: u u~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: c c~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: d d~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: s s~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: g g > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: u u~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: c c~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: d d~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: s s~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > mu+ vm WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > e- ve~ WEIGHTED<=2
// Process: g g > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: u u~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: c c~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: d d~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2
// Process: s s~ > t t~ b b~ WEIGHTED<=4 @1
// *   Decay: t > w+ b WEIGHTED<=2
// *     Decay: w+ > e+ ve WEIGHTED<=2
// *   Decay: t~ > w- b~ WEIGHTED<=2
// *     Decay: w- > mu- vm~ WEIGHTED<=2

//--------------------------------------------------------------------------

// Initialize process.

P1_Sigma_sm_gg_epvebemvexbxbbx::P1_Sigma_sm_gg_epvebemvexbxbbx(const
    ParameterSet& configuration)
{

  std::string param_card = configuration.get < std::string > ("card"); 
  params.reset(new Parameters_sm(SLHA::Reader(param_card))); 

  // Set external particle masses for this matrix element
  mME.push_back(std::ref(params->ZERO)); 
  mME.push_back(std::ref(params->ZERO)); 
  mME.push_back(std::ref(params->ZERO)); 
  mME.push_back(std::ref(params->ZERO)); 
  mME.push_back(std::ref(params->mdl_MB)); 
  mME.push_back(std::ref(params->ZERO)); 
  mME.push_back(std::ref(params->ZERO)); 
  mME.push_back(std::ref(params->mdl_MB)); 
  mME.push_back(std::ref(params->mdl_MB)); 
  mME.push_back(std::ref(params->mdl_MB)); 

  mapFinalStates[{-11, 12, 5, 11, -12, -5, 5, -5}] = 
  {
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_emvex, 
      false, 
      {
        std::make_pair(21, 21)
      }, 
      1024, 
      256
    }
    , 
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_emvex, 
      true, 
      {
        std::make_pair(2, -2), std::make_pair(4, -4), std::make_pair(1, -1),
            std::make_pair(3, -3)
      }, 
      1024, 
      36
    }
  }; 
  mapFinalStates[{-11, 12, 5, 13, -14, -5, 5, -5}] = 
  {
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_mumvmx, 
      false, 
      {
        std::make_pair(21, 21)
      }, 
      1024, 
      256
    }
    , 
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_mumvmx, 
      true, 
      {
        std::make_pair(2, -2), std::make_pair(4, -4), std::make_pair(1, -1),
            std::make_pair(3, -3)
      }, 
      1024, 
      36
    }
  }; 
  mapFinalStates[{-13, 14, 5, 13, -14, -5, 5, -5}] = 
  {
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_mumvmx, 
      false, 
      {
        std::make_pair(21, 21)
      }, 
      1024, 
      256
    }
    , 
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_mumvmx, 
      true, 
      {
        std::make_pair(2, -2), std::make_pair(4, -4), std::make_pair(1, -1),
            std::make_pair(3, -3)
      }, 
      1024, 
      36
    }
  }; 
  mapFinalStates[{-13, 14, 5, 11, -12, -5, 5, -5}] = 
  {
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_emvex, 
      false, 
      {
        std::make_pair(21, 21)
      }, 
      1024, 
      256
    }
    , 
    {
      &P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_emvex, 
      true, 
      {
        std::make_pair(2, -2), std::make_pair(4, -4), std::make_pair(1, -1),
            std::make_pair(3, -3)
      }, 
      1024, 
      36
    }
  }; 

}

void P1_Sigma_sm_gg_epvebemvexbxbbx::resetHelicities() 
{
  for (auto& finalState: mapFinalStates)
  {
    for (auto& subProcess: finalState.second)
    {
      subProcess.resetHelicities(); 
    }
  }
}


//--------------------------------------------------------------------------
// Evaluate |M|^2, return a map of final states

std::map < std::pair < int, int > , double >
    P1_Sigma_sm_gg_epvebemvexbxbbx::compute(const std::pair <
    std::vector<double> , std::vector<double> > &initialMomenta, const
    std::vector < std::pair < int, std::vector<double> > > &finalState)
{

  // Set initial particle momenta
  momenta[0] = (double * ) (&initialMomenta.first[0]); 
  momenta[1] = (double * ) (&initialMomenta.second[0]); 

  // Suppose final particles are passed in the "correct" order
  std::vector<int> selectedFinalState(10 - 2); 
  for (size_t index = 0; index < (10 - 2); index++ )
  {
    selectedFinalState[index] = finalState[index].first; 
    momenta[index + 2] = (double * ) (&finalState[index].second[0]); 
  }

  // Set the event specific parameters
  params->updateParameters(); 
  params->updateCouplings(); 

  // Initialise result object
  std::map < std::pair < int, int > , double > result; 

  // Define permutation
  int perm[10]; 
  for(int i = 0; i < 10; i++ )
  {
    perm[i] = i; 
  }

  for(auto &me: mapFinalStates[selectedFinalState])
  {

    double me_sum = 0; 
    double me_mirror_sum = 0; 

    for(int ihel = 0; ihel < 1024; ihel++ )
    {

      if(me.goodHel[ihel])
      {

        double sum = 0.; 
        calculate_wavefunctions(perm, helicities[ihel]); 
        double meTemp = me.callback( * this); 
        sum += meTemp; 
        me_sum += meTemp/me.denominator; 

        if(me.hasMirrorProcess)
        {
          perm[0] = 1; 
          perm[1] = 0; 
          // Calculate wavefunctions
          calculate_wavefunctions(perm, helicities[ihel]); 
          // Mirror back
          perm[0] = 0; 
          perm[1] = 1; 
          meTemp = me.callback( * this); 
          sum += meTemp; 
          me_mirror_sum += meTemp/me.denominator; 
        }

        if( !sum)
          me.goodHel[ihel] = false; 
      }
    }

    for (auto const &initialState: me.initialStates)
    {
      result[initialState] = me_sum; 
      if (me.hasMirrorProcess)
        result[std::make_pair(initialState.second, initialState.first)] =
            me_mirror_sum;
    }
  }


  return result; 
}

//==========================================================================
// Private class member functions

//--------------------------------------------------------------------------
// Evaluate |M|^2 for each subprocess

void P1_Sigma_sm_gg_epvebemvexbxbbx::calculate_wavefunctions(const int perm[],
    const int hel[])
{
  // Calculate wavefunctions for all processes
  static std::complex<double> w[52][18]; 

  // Calculate all wavefunctions
  vxxxxx(&momenta[perm[0]][0], mME[0], hel[0], -1, w[0]); 
  vxxxxx(&momenta[perm[1]][0], mME[1], hel[1], -1, w[1]); 
  ixxxxx(&momenta[perm[2]][0], mME[2], hel[2], -1, w[2]); 
  oxxxxx(&momenta[perm[3]][0], mME[3], hel[3], +1, w[3]); 
  FFV2_3(w[2], w[3], params->GC_100, params->mdl_MW, params->mdl_WW, w[4]); 
  oxxxxx(&momenta[perm[4]][0], mME[4], hel[4], +1, w[5]); 
  FFV2_1(w[5], w[4], params->GC_100, params->mdl_MT, params->mdl_WT, w[6]); 
  oxxxxx(&momenta[perm[5]][0], mME[5], hel[5], +1, w[7]); 
  ixxxxx(&momenta[perm[6]][0], mME[6], hel[6], -1, w[8]); 
  FFV2_3(w[8], w[7], params->GC_100, params->mdl_MW, params->mdl_WW, w[9]); 
  ixxxxx(&momenta[perm[7]][0], mME[7], hel[7], -1, w[10]); 
  FFV2_2(w[10], w[9], params->GC_100, params->mdl_MT, params->mdl_WT, w[11]); 
  oxxxxx(&momenta[perm[8]][0], mME[8], hel[8], +1, w[12]); 
  ixxxxx(&momenta[perm[9]][0], mME[9], hel[9], -1, w[13]); 
  VVV1P0_1(w[0], w[1], params->GC_10, params->ZERO, params->ZERO, w[14]); 
  FFV1P0_3(w[11], w[6], params->GC_11, params->ZERO, params->ZERO, w[15]); 
  FFV1_1(w[12], w[14], params->GC_11, params->mdl_MB, params->ZERO, w[16]); 
  FFV1_2(w[13], w[14], params->GC_11, params->mdl_MB, params->ZERO, w[17]); 
  FFV1P0_3(w[13], w[12], params->GC_11, params->ZERO, params->ZERO, w[18]); 
  FFV1_1(w[6], w[14], params->GC_11, params->mdl_MT, params->mdl_WT, w[19]); 
  FFV1_2(w[11], w[14], params->GC_11, params->mdl_MT, params->mdl_WT, w[20]); 
  FFV1_1(w[6], w[0], params->GC_11, params->mdl_MT, params->mdl_WT, w[21]); 
  FFV1_2(w[11], w[1], params->GC_11, params->mdl_MT, params->mdl_WT, w[22]); 
  FFV1_1(w[12], w[1], params->GC_11, params->mdl_MB, params->ZERO, w[23]); 
  FFV1P0_3(w[11], w[21], params->GC_11, params->ZERO, params->ZERO, w[24]); 
  FFV1_2(w[13], w[1], params->GC_11, params->mdl_MB, params->ZERO, w[25]); 
  FFV1_1(w[21], w[1], params->GC_11, params->mdl_MT, params->mdl_WT, w[26]); 
  FFV1_2(w[11], w[0], params->GC_11, params->mdl_MT, params->mdl_WT, w[27]); 
  FFV1_1(w[6], w[1], params->GC_11, params->mdl_MT, params->mdl_WT, w[28]); 
  FFV1P0_3(w[27], w[6], params->GC_11, params->ZERO, params->ZERO, w[29]); 
  FFV1_2(w[27], w[1], params->GC_11, params->mdl_MT, params->mdl_WT, w[30]); 
  FFV1_1(w[12], w[0], params->GC_11, params->mdl_MB, params->ZERO, w[31]); 
  FFV1P0_3(w[13], w[31], params->GC_11, params->ZERO, params->ZERO, w[32]); 
  FFV1_1(w[31], w[1], params->GC_11, params->mdl_MB, params->ZERO, w[33]); 
  FFV1_2(w[13], w[0], params->GC_11, params->mdl_MB, params->ZERO, w[34]); 
  FFV1P0_3(w[34], w[12], params->GC_11, params->ZERO, params->ZERO, w[35]); 
  FFV1_2(w[34], w[1], params->GC_11, params->mdl_MB, params->ZERO, w[36]); 
  FFV1_1(w[28], w[0], params->GC_11, params->mdl_MT, params->mdl_WT, w[37]); 
  VVV1P0_1(w[0], w[18], params->GC_10, params->ZERO, params->ZERO, w[38]); 
  FFV1_2(w[22], w[0], params->GC_11, params->mdl_MT, params->mdl_WT, w[39]); 
  FFV1_1(w[23], w[0], params->GC_11, params->mdl_MB, params->ZERO, w[40]); 
  VVV1P0_1(w[0], w[15], params->GC_10, params->ZERO, params->ZERO, w[41]); 
  FFV1_2(w[25], w[0], params->GC_11, params->mdl_MB, params->ZERO, w[42]); 
  ixxxxx(&momenta[perm[0]][0], mME[0], hel[0], +1, w[43]); 
  oxxxxx(&momenta[perm[1]][0], mME[1], hel[1], -1, w[44]); 
  FFV1P0_3(w[43], w[44], params->GC_11, params->ZERO, params->ZERO, w[45]); 
  FFV1_1(w[12], w[45], params->GC_11, params->mdl_MB, params->ZERO, w[46]); 
  FFV1_2(w[13], w[45], params->GC_11, params->mdl_MB, params->ZERO, w[47]); 
  FFV1_1(w[6], w[45], params->GC_11, params->mdl_MT, params->mdl_WT, w[48]); 
  FFV1_2(w[11], w[45], params->GC_11, params->mdl_MT, params->mdl_WT, w[49]); 
  FFV1_2(w[43], w[15], params->GC_11, params->ZERO, params->ZERO, w[50]); 
  FFV1_2(w[43], w[18], params->GC_11, params->ZERO, params->ZERO, w[51]); 

  // Calculate all amplitudes
  // Amplitude(s) for diagram number 0
  FFV1_0(w[13], w[16], w[15], params->GC_11, amp[0]); 
  FFV1_0(w[17], w[12], w[15], params->GC_11, amp[1]); 
  VVV1_0(w[14], w[15], w[18], params->GC_10, amp[2]); 
  FFV1_0(w[11], w[19], w[18], params->GC_11, amp[3]); 
  FFV1_0(w[20], w[6], w[18], params->GC_11, amp[4]); 
  FFV1_0(w[22], w[21], w[18], params->GC_11, amp[5]); 
  FFV1_0(w[13], w[23], w[24], params->GC_11, amp[6]); 
  FFV1_0(w[25], w[12], w[24], params->GC_11, amp[7]); 
  FFV1_0(w[11], w[26], w[18], params->GC_11, amp[8]); 
  VVV1_0(w[1], w[18], w[24], params->GC_10, amp[9]); 
  FFV1_0(w[27], w[28], w[18], params->GC_11, amp[10]); 
  FFV1_0(w[13], w[23], w[29], params->GC_11, amp[11]); 
  FFV1_0(w[25], w[12], w[29], params->GC_11, amp[12]); 
  FFV1_0(w[30], w[6], w[18], params->GC_11, amp[13]); 
  VVV1_0(w[1], w[18], w[29], params->GC_10, amp[14]); 
  FFV1_0(w[11], w[28], w[32], params->GC_11, amp[15]); 
  FFV1_0(w[22], w[6], w[32], params->GC_11, amp[16]); 
  FFV1_0(w[25], w[31], w[15], params->GC_11, amp[17]); 
  FFV1_0(w[13], w[33], w[15], params->GC_11, amp[18]); 
  VVV1_0(w[1], w[15], w[32], params->GC_10, amp[19]); 
  FFV1_0(w[11], w[28], w[35], params->GC_11, amp[20]); 
  FFV1_0(w[22], w[6], w[35], params->GC_11, amp[21]); 
  FFV1_0(w[34], w[23], w[15], params->GC_11, amp[22]); 
  FFV1_0(w[36], w[12], w[15], params->GC_11, amp[23]); 
  VVV1_0(w[1], w[15], w[35], params->GC_10, amp[24]); 
  FFV1_0(w[11], w[37], w[18], params->GC_11, amp[25]); 
  FFV1_0(w[11], w[28], w[38], params->GC_11, amp[26]); 
  FFV1_0(w[39], w[6], w[18], params->GC_11, amp[27]); 
  FFV1_0(w[22], w[6], w[38], params->GC_11, amp[28]); 
  FFV1_0(w[13], w[40], w[15], params->GC_11, amp[29]); 
  FFV1_0(w[13], w[23], w[41], params->GC_11, amp[30]); 
  FFV1_0(w[42], w[12], w[15], params->GC_11, amp[31]); 
  FFV1_0(w[25], w[12], w[41], params->GC_11, amp[32]); 
  VVVV1_0(w[0], w[1], w[15], w[18], params->GC_12, amp[33]); 
  VVVV3_0(w[0], w[1], w[15], w[18], params->GC_12, amp[34]); 
  VVVV4_0(w[0], w[1], w[15], w[18], params->GC_12, amp[35]); 
  VVV1_0(w[1], w[18], w[41], params->GC_10, amp[36]); 
  VVV1_0(w[1], w[15], w[38], params->GC_10, amp[37]); 
  FFV1_0(w[13], w[46], w[15], params->GC_11, amp[38]); 
  FFV1_0(w[47], w[12], w[15], params->GC_11, amp[39]); 
  VVV1_0(w[45], w[15], w[18], params->GC_10, amp[40]); 
  FFV1_0(w[11], w[48], w[18], params->GC_11, amp[41]); 
  FFV1_0(w[49], w[6], w[18], params->GC_11, amp[42]); 
  FFV1_0(w[50], w[44], w[18], params->GC_11, amp[43]); 
  FFV1_0(w[51], w[44], w[15], params->GC_11, amp[44]); 

}
double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_emvex() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[12]; 
  // The color matrix
  static const double denom[12] = {3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3}; 
  static const double cf[12][12] = {{48, 16, 16, 6, 0, 16, -2, 0, -6, -2, -2,
      6}, {16, 48, 6, 16, 16, 0, 0, -2, -2, -6, 6, -2}, {16, 6, 48, 16, -2, 0,
      0, 16, -2, 6, -6, -2}, {6, 16, 16, 48, 0, -2, 16, 0, 6, -2, -2, -6}, {0,
      16, -2, 0, 48, 16, 16, 6, 0, -2, 16, 0}, {16, 0, 0, -2, 16, 48, 6, 16,
      -2, 0, 0, 16}, {-2, 0, 0, 16, 16, 6, 48, 16, 16, 0, 0, -2}, {0, -2, 16,
      0, 6, 16, 16, 48, 0, 16, -2, 0}, {-6, -2, -2, 6, 0, -2, 16, 0, 48, 16,
      16, 6}, {-2, -6, 6, -2, -2, 0, 0, 16, 16, 48, 6, 16}, {-2, 6, -6, -2, 16,
      0, 0, -2, 16, 6, 48, 16}, {6, -2, -2, -6, 0, 16, -2, 0, 6, 16, 16, 48}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./2. * (-1./3. * cI * amp[3] - 1./3. * cI * amp[4] + 1./3. *
      amp[5] + 1./3. * amp[8] + 1./3. * amp[27]);
  jamp[1] = +1./2. * (+cI * amp[1] - amp[2] + cI * amp[3] - amp[7] - amp[8] +
      cI * amp[9] - amp[31] - cI * amp[32] - amp[34] - amp[33] - amp[36]);
  jamp[2] = +1./2. * (+cI * amp[0] + amp[2] + cI * amp[4] - amp[16] - amp[18] +
      cI * amp[19] - amp[27] - cI * amp[28] + amp[33] - amp[35] - amp[37]);
  jamp[3] = +1./2. * (-1./3. * cI * amp[0] - 1./3. * cI * amp[1] + 1./3. *
      amp[17] + 1./3. * amp[18] + 1./3. * amp[31]);
  jamp[4] = +1./2. * (+1./3. * amp[6] + 1./3. * amp[7] + 1./3. * amp[11] +
      1./3. * amp[12]);
  jamp[5] = +1./2. * (-amp[5] - amp[6] - cI * amp[9] - amp[21] - amp[22] + cI *
      amp[24] + cI * amp[28] - cI * amp[30] + amp[34] + amp[35] + amp[36] +
      amp[37]);
  jamp[6] = +1./2. * (-amp[10] - amp[12] + cI * amp[14] - amp[15] - amp[17] -
      cI * amp[19] - cI * amp[26] + cI * amp[32] + amp[34] + amp[35] + amp[36]
      + amp[37]);
  jamp[7] = +1./2. * (+1./3. * amp[15] + 1./3. * amp[16] + 1./3. * amp[20] +
      1./3. * amp[21]);
  jamp[8] = +1./2. * (+1./3. * cI * amp[3] + 1./3. * cI * amp[4] + 1./3. *
      amp[10] + 1./3. * amp[13] + 1./3. * amp[25]);
  jamp[9] = +1./2. * (-cI * amp[1] + amp[2] - cI * amp[3] - amp[20] - amp[23] -
      cI * amp[24] - amp[25] + cI * amp[26] + amp[33] - amp[35] - amp[37]);
  jamp[10] = +1./2. * (-cI * amp[0] - amp[2] - cI * amp[4] - amp[11] - amp[13]
      - cI * amp[14] - amp[29] + cI * amp[30] - amp[34] - amp[33] - amp[36]);
  jamp[11] = +1./2. * (+1./3. * cI * amp[0] + 1./3. * cI * amp[1] + 1./3. *
      amp[22] + 1./3. * amp[23] + 1./3. * amp[29]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 12; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 12; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_emvex() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[6]; 
  // The color matrix
  static const double denom[6] = {1, 1, 1, 1, 1, 1}; 
  static const double cf[6][6] = {{27, 9, 9, 3, 3, 9}, {9, 27, 3, 9, 9, 3}, {9,
      3, 27, 9, 9, 3}, {3, 9, 9, 27, 3, 9}, {3, 9, 9, 3, 27, 9}, {9, 3, 3, 9,
      9, 27}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./4. * (-1./9. * amp[38] - 1./9. * amp[39] - 1./9. * amp[41] -
      1./9. * amp[42] - 1./9. * amp[43] - 1./9. * amp[44]);
  jamp[1] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[41] +
      1./3. * amp[42]);
  jamp[2] = +1./4. * (+1./3. * amp[41] + 1./3. * amp[42] + 1./3. * amp[43] +
      1./3. * amp[44]);
  jamp[3] = +1./4. * (-amp[38] + cI * amp[40] - amp[42] - amp[44]); 
  jamp[4] = +1./4. * (-amp[39] - cI * amp[40] - amp[41] - amp[43]); 
  jamp[5] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[43] +
      1./3. * amp[44]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 6; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 6; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_mumvmx() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[12]; 
  // The color matrix
  static const double denom[12] = {3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3}; 
  static const double cf[12][12] = {{48, 16, 16, 6, 0, 16, -2, 0, -6, -2, -2,
      6}, {16, 48, 6, 16, 16, 0, 0, -2, -2, -6, 6, -2}, {16, 6, 48, 16, -2, 0,
      0, 16, -2, 6, -6, -2}, {6, 16, 16, 48, 0, -2, 16, 0, 6, -2, -2, -6}, {0,
      16, -2, 0, 48, 16, 16, 6, 0, -2, 16, 0}, {16, 0, 0, -2, 16, 48, 6, 16,
      -2, 0, 0, 16}, {-2, 0, 0, 16, 16, 6, 48, 16, 16, 0, 0, -2}, {0, -2, 16,
      0, 6, 16, 16, 48, 0, 16, -2, 0}, {-6, -2, -2, 6, 0, -2, 16, 0, 48, 16,
      16, 6}, {-2, -6, 6, -2, -2, 0, 0, 16, 16, 48, 6, 16}, {-2, 6, -6, -2, 16,
      0, 0, -2, 16, 6, 48, 16}, {6, -2, -2, -6, 0, 16, -2, 0, 6, 16, 16, 48}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./2. * (-1./3. * cI * amp[3] - 1./3. * cI * amp[4] + 1./3. *
      amp[5] + 1./3. * amp[8] + 1./3. * amp[27]);
  jamp[1] = +1./2. * (+cI * amp[1] - amp[2] + cI * amp[3] - amp[7] - amp[8] +
      cI * amp[9] - amp[31] - cI * amp[32] - amp[34] - amp[33] - amp[36]);
  jamp[2] = +1./2. * (+cI * amp[0] + amp[2] + cI * amp[4] - amp[16] - amp[18] +
      cI * amp[19] - amp[27] - cI * amp[28] + amp[33] - amp[35] - amp[37]);
  jamp[3] = +1./2. * (-1./3. * cI * amp[0] - 1./3. * cI * amp[1] + 1./3. *
      amp[17] + 1./3. * amp[18] + 1./3. * amp[31]);
  jamp[4] = +1./2. * (+1./3. * amp[6] + 1./3. * amp[7] + 1./3. * amp[11] +
      1./3. * amp[12]);
  jamp[5] = +1./2. * (-amp[5] - amp[6] - cI * amp[9] - amp[21] - amp[22] + cI *
      amp[24] + cI * amp[28] - cI * amp[30] + amp[34] + amp[35] + amp[36] +
      amp[37]);
  jamp[6] = +1./2. * (-amp[10] - amp[12] + cI * amp[14] - amp[15] - amp[17] -
      cI * amp[19] - cI * amp[26] + cI * amp[32] + amp[34] + amp[35] + amp[36]
      + amp[37]);
  jamp[7] = +1./2. * (+1./3. * amp[15] + 1./3. * amp[16] + 1./3. * amp[20] +
      1./3. * amp[21]);
  jamp[8] = +1./2. * (+1./3. * cI * amp[3] + 1./3. * cI * amp[4] + 1./3. *
      amp[10] + 1./3. * amp[13] + 1./3. * amp[25]);
  jamp[9] = +1./2. * (-cI * amp[1] + amp[2] - cI * amp[3] - amp[20] - amp[23] -
      cI * amp[24] - amp[25] + cI * amp[26] + amp[33] - amp[35] - amp[37]);
  jamp[10] = +1./2. * (-cI * amp[0] - amp[2] - cI * amp[4] - amp[11] - amp[13]
      - cI * amp[14] - amp[29] + cI * amp[30] - amp[34] - amp[33] - amp[36]);
  jamp[11] = +1./2. * (+1./3. * cI * amp[0] + 1./3. * cI * amp[1] + 1./3. *
      amp[22] + 1./3. * amp[23] + 1./3. * amp[29]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 12; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 12; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_mumvmx() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[6]; 
  // The color matrix
  static const double denom[6] = {1, 1, 1, 1, 1, 1}; 
  static const double cf[6][6] = {{27, 9, 9, 3, 3, 9}, {9, 27, 3, 9, 9, 3}, {9,
      3, 27, 9, 9, 3}, {3, 9, 9, 27, 3, 9}, {3, 9, 9, 3, 27, 9}, {9, 3, 3, 9,
      9, 27}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./4. * (-1./9. * amp[38] - 1./9. * amp[39] - 1./9. * amp[41] -
      1./9. * amp[42] - 1./9. * amp[43] - 1./9. * amp[44]);
  jamp[1] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[41] +
      1./3. * amp[42]);
  jamp[2] = +1./4. * (+1./3. * amp[41] + 1./3. * amp[42] + 1./3. * amp[43] +
      1./3. * amp[44]);
  jamp[3] = +1./4. * (-amp[38] + cI * amp[40] - amp[42] - amp[44]); 
  jamp[4] = +1./4. * (-amp[39] - cI * amp[40] - amp[41] - amp[43]); 
  jamp[5] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[43] +
      1./3. * amp[44]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 6; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 6; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_emvex() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[12]; 
  // The color matrix
  static const double denom[12] = {3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3}; 
  static const double cf[12][12] = {{48, 16, 16, 6, 0, 16, -2, 0, -6, -2, -2,
      6}, {16, 48, 6, 16, 16, 0, 0, -2, -2, -6, 6, -2}, {16, 6, 48, 16, -2, 0,
      0, 16, -2, 6, -6, -2}, {6, 16, 16, 48, 0, -2, 16, 0, 6, -2, -2, -6}, {0,
      16, -2, 0, 48, 16, 16, 6, 0, -2, 16, 0}, {16, 0, 0, -2, 16, 48, 6, 16,
      -2, 0, 0, 16}, {-2, 0, 0, 16, 16, 6, 48, 16, 16, 0, 0, -2}, {0, -2, 16,
      0, 6, 16, 16, 48, 0, 16, -2, 0}, {-6, -2, -2, 6, 0, -2, 16, 0, 48, 16,
      16, 6}, {-2, -6, 6, -2, -2, 0, 0, 16, 16, 48, 6, 16}, {-2, 6, -6, -2, 16,
      0, 0, -2, 16, 6, 48, 16}, {6, -2, -2, -6, 0, 16, -2, 0, 6, 16, 16, 48}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./2. * (-1./3. * cI * amp[3] - 1./3. * cI * amp[4] + 1./3. *
      amp[5] + 1./3. * amp[8] + 1./3. * amp[27]);
  jamp[1] = +1./2. * (+cI * amp[1] - amp[2] + cI * amp[3] - amp[7] - amp[8] +
      cI * amp[9] - amp[31] - cI * amp[32] - amp[34] - amp[33] - amp[36]);
  jamp[2] = +1./2. * (+cI * amp[0] + amp[2] + cI * amp[4] - amp[16] - amp[18] +
      cI * amp[19] - amp[27] - cI * amp[28] + amp[33] - amp[35] - amp[37]);
  jamp[3] = +1./2. * (-1./3. * cI * amp[0] - 1./3. * cI * amp[1] + 1./3. *
      amp[17] + 1./3. * amp[18] + 1./3. * amp[31]);
  jamp[4] = +1./2. * (+1./3. * amp[6] + 1./3. * amp[7] + 1./3. * amp[11] +
      1./3. * amp[12]);
  jamp[5] = +1./2. * (-amp[5] - amp[6] - cI * amp[9] - amp[21] - amp[22] + cI *
      amp[24] + cI * amp[28] - cI * amp[30] + amp[34] + amp[35] + amp[36] +
      amp[37]);
  jamp[6] = +1./2. * (-amp[10] - amp[12] + cI * amp[14] - amp[15] - amp[17] -
      cI * amp[19] - cI * amp[26] + cI * amp[32] + amp[34] + amp[35] + amp[36]
      + amp[37]);
  jamp[7] = +1./2. * (+1./3. * amp[15] + 1./3. * amp[16] + 1./3. * amp[20] +
      1./3. * amp[21]);
  jamp[8] = +1./2. * (+1./3. * cI * amp[3] + 1./3. * cI * amp[4] + 1./3. *
      amp[10] + 1./3. * amp[13] + 1./3. * amp[25]);
  jamp[9] = +1./2. * (-cI * amp[1] + amp[2] - cI * amp[3] - amp[20] - amp[23] -
      cI * amp[24] - amp[25] + cI * amp[26] + amp[33] - amp[35] - amp[37]);
  jamp[10] = +1./2. * (-cI * amp[0] - amp[2] - cI * amp[4] - amp[11] - amp[13]
      - cI * amp[14] - amp[29] + cI * amp[30] - amp[34] - amp[33] - amp[36]);
  jamp[11] = +1./2. * (+1./3. * cI * amp[0] + 1./3. * cI * amp[1] + 1./3. *
      amp[22] + 1./3. * amp[23] + 1./3. * amp[29]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 12; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 12; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_mupvm_tx_wmbx_wm_emvex() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[6]; 
  // The color matrix
  static const double denom[6] = {1, 1, 1, 1, 1, 1}; 
  static const double cf[6][6] = {{27, 9, 9, 3, 3, 9}, {9, 27, 3, 9, 9, 3}, {9,
      3, 27, 9, 9, 3}, {3, 9, 9, 27, 3, 9}, {3, 9, 9, 3, 27, 9}, {9, 3, 3, 9,
      9, 27}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./4. * (-1./9. * amp[38] - 1./9. * amp[39] - 1./9. * amp[41] -
      1./9. * amp[42] - 1./9. * amp[43] - 1./9. * amp[44]);
  jamp[1] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[41] +
      1./3. * amp[42]);
  jamp[2] = +1./4. * (+1./3. * amp[41] + 1./3. * amp[42] + 1./3. * amp[43] +
      1./3. * amp[44]);
  jamp[3] = +1./4. * (-amp[38] + cI * amp[40] - amp[42] - amp[44]); 
  jamp[4] = +1./4. * (-amp[39] - cI * amp[40] - amp[41] - amp[43]); 
  jamp[5] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[43] +
      1./3. * amp[44]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 6; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 6; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_gg_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_mumvmx() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[12]; 
  // The color matrix
  static const double denom[12] = {3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3}; 
  static const double cf[12][12] = {{48, 16, 16, 6, 0, 16, -2, 0, -6, -2, -2,
      6}, {16, 48, 6, 16, 16, 0, 0, -2, -2, -6, 6, -2}, {16, 6, 48, 16, -2, 0,
      0, 16, -2, 6, -6, -2}, {6, 16, 16, 48, 0, -2, 16, 0, 6, -2, -2, -6}, {0,
      16, -2, 0, 48, 16, 16, 6, 0, -2, 16, 0}, {16, 0, 0, -2, 16, 48, 6, 16,
      -2, 0, 0, 16}, {-2, 0, 0, 16, 16, 6, 48, 16, 16, 0, 0, -2}, {0, -2, 16,
      0, 6, 16, 16, 48, 0, 16, -2, 0}, {-6, -2, -2, 6, 0, -2, 16, 0, 48, 16,
      16, 6}, {-2, -6, 6, -2, -2, 0, 0, 16, 16, 48, 6, 16}, {-2, 6, -6, -2, 16,
      0, 0, -2, 16, 6, 48, 16}, {6, -2, -2, -6, 0, 16, -2, 0, 6, 16, 16, 48}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./2. * (-1./3. * cI * amp[3] - 1./3. * cI * amp[4] + 1./3. *
      amp[5] + 1./3. * amp[8] + 1./3. * amp[27]);
  jamp[1] = +1./2. * (+cI * amp[1] - amp[2] + cI * amp[3] - amp[7] - amp[8] +
      cI * amp[9] - amp[31] - cI * amp[32] - amp[34] - amp[33] - amp[36]);
  jamp[2] = +1./2. * (+cI * amp[0] + amp[2] + cI * amp[4] - amp[16] - amp[18] +
      cI * amp[19] - amp[27] - cI * amp[28] + amp[33] - amp[35] - amp[37]);
  jamp[3] = +1./2. * (-1./3. * cI * amp[0] - 1./3. * cI * amp[1] + 1./3. *
      amp[17] + 1./3. * amp[18] + 1./3. * amp[31]);
  jamp[4] = +1./2. * (+1./3. * amp[6] + 1./3. * amp[7] + 1./3. * amp[11] +
      1./3. * amp[12]);
  jamp[5] = +1./2. * (-amp[5] - amp[6] - cI * amp[9] - amp[21] - amp[22] + cI *
      amp[24] + cI * amp[28] - cI * amp[30] + amp[34] + amp[35] + amp[36] +
      amp[37]);
  jamp[6] = +1./2. * (-amp[10] - amp[12] + cI * amp[14] - amp[15] - amp[17] -
      cI * amp[19] - cI * amp[26] + cI * amp[32] + amp[34] + amp[35] + amp[36]
      + amp[37]);
  jamp[7] = +1./2. * (+1./3. * amp[15] + 1./3. * amp[16] + 1./3. * amp[20] +
      1./3. * amp[21]);
  jamp[8] = +1./2. * (+1./3. * cI * amp[3] + 1./3. * cI * amp[4] + 1./3. *
      amp[10] + 1./3. * amp[13] + 1./3. * amp[25]);
  jamp[9] = +1./2. * (-cI * amp[1] + amp[2] - cI * amp[3] - amp[20] - amp[23] -
      cI * amp[24] - amp[25] + cI * amp[26] + amp[33] - amp[35] - amp[37]);
  jamp[10] = +1./2. * (-cI * amp[0] - amp[2] - cI * amp[4] - amp[11] - amp[13]
      - cI * amp[14] - amp[29] + cI * amp[30] - amp[34] - amp[33] - amp[36]);
  jamp[11] = +1./2. * (+1./3. * cI * amp[0] + 1./3. * cI * amp[1] + 1./3. *
      amp[22] + 1./3. * amp[23] + 1./3. * amp[29]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 12; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 12; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}

double P1_Sigma_sm_gg_epvebemvexbxbbx::matrix_1_uux_ttxbbx_t_wpb_wp_epve_tx_wmbx_wm_mumvmx() 
{

  static std::complex<double> ztemp; 
  static std::complex<double> jamp[6]; 
  // The color matrix
  static const double denom[6] = {1, 1, 1, 1, 1, 1}; 
  static const double cf[6][6] = {{27, 9, 9, 3, 3, 9}, {9, 27, 3, 9, 9, 3}, {9,
      3, 27, 9, 9, 3}, {3, 9, 9, 27, 3, 9}, {3, 9, 9, 3, 27, 9}, {9, 3, 3, 9,
      9, 27}};

  // Calculate color flows
  static const std::complex<double> cI(0., 1.); 
  jamp[0] = +1./4. * (-1./9. * amp[38] - 1./9. * amp[39] - 1./9. * amp[41] -
      1./9. * amp[42] - 1./9. * amp[43] - 1./9. * amp[44]);
  jamp[1] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[41] +
      1./3. * amp[42]);
  jamp[2] = +1./4. * (+1./3. * amp[41] + 1./3. * amp[42] + 1./3. * amp[43] +
      1./3. * amp[44]);
  jamp[3] = +1./4. * (-amp[38] + cI * amp[40] - amp[42] - amp[44]); 
  jamp[4] = +1./4. * (-amp[39] - cI * amp[40] - amp[41] - amp[43]); 
  jamp[5] = +1./4. * (+1./3. * amp[38] + 1./3. * amp[39] + 1./3. * amp[43] +
      1./3. * amp[44]);

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  for(int i = 0; i < 6; i++ )
  {
    ztemp = 0.; 
    for(int j = 0; j < 6; j++ )
      ztemp = ztemp + cf[i][j] * jamp[j]; 
    matrix = matrix + real(ztemp * conj(jamp[i]))/denom[i]; 
  }

  return matrix; 
}



}

// Register matrix element with MoMEMta
#include <momemta/MatrixElementFactory.h> 
REGISTER_MATRIX_ELEMENT("ttbb_FullyLeptonic_sm_P1_Sigma_sm_gg_epvebemvexbxbbx",
    ttbb_FullyLeptonic_sm::P1_Sigma_sm_gg_epvebemvexbxbbx);

