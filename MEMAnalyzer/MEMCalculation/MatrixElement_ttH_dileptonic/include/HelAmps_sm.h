//==========================================================================
// This file has been automatically generated for C++ Standalone
// MadGraph5_aMC@NLO v. 2.6.1, 2017-12-12
// By the MadGraph5_aMC@NLO Development Team
// Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
//==========================================================================

#ifndef HelAmps_sm_H
#define HelAmps_sm_H

#include <cmath> 
#include <complex> 

using namespace std; 

namespace ttH_Hbb_dilepTops_sm 
{
void vxxxxx(double p[4], double vmass, int nhel, int nsv, std::complex<double>
    v[6]);

double Sgn(double e, double f); 

void txxxxx(double p[4], double tmass, int nhel, int nst, std::complex<double>
    fi[18]);

void ixxxxx(double p[4], double fmass, int nhel, int nsf, std::complex<double>
    fi[6]);

void sxxxxx(double p[4], int nss, std::complex<double> sc[3]); 

void oxxxxx(double p[4], double fmass, int nhel, int nsf, std::complex<double>
    fo[6]);

void FFV2_3(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> V3[]);

void FFV2_2(std::complex<double> F1[], std::complex<double> V3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFV2_1(std::complex<double> F2[], std::complex<double> V3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFV1_2(std::complex<double> F1[], std::complex<double> V3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFS4_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> S3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFV1_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFS4_1(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFV1_1(std::complex<double> F2[], std::complex<double> V3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFS4_2(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFS4_3(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> S3[]);

void VVV1P0_1(std::complex<double> V2[], std::complex<double> V3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> V1[]);

}  // end namespace ttH_Hbb_dilepTops_sm

#endif  // HelAmps_sm_H
