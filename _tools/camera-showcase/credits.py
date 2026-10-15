# survey key -> (display name, HiPS ids used, acknowledgement, reference)
CREDITS = {
 "PS1": ("Pan-STARRS1 (PS1) DR1", "CDS/P/PanSTARRS/DR1/{g,r,i,z,y,color-i-r-g}",
  "The Pan-STARRS1 Surveys (PS1) and the PS1 public science archive have been made possible through contributions by the Institute for Astronomy, the University of Hawaii, the Pan-STARRS Project Office, the Max-Planck Society and its participating institutes, the Johns Hopkins University, Durham University, the University of Edinburgh, the Queen's University Belfast, the Harvard-Smithsonian Center for Astrophysics, the Las Cumbres Observatory Global Telescope Network Incorporated, the National Central University of Taiwan, the Space Telescope Science Institute, NASA, the NSF, the University of Maryland, Eotvos Lorand University, the Los Alamos National Laboratory, and the Gordon and Betty Moore Foundation.",
  "Chambers et al. 2016, arXiv:1612.05560; Flewelling et al. 2020, ApJS 251, 7"),
 "SDSS": ("Sloan Digital Sky Survey (SDSS) DR9", "CDS/P/SDSS9/u",
  "Funding for SDSS-III has been provided by the Alfred P. Sloan Foundation, the Participating Institutions, the National Science Foundation, and the U.S. Department of Energy Office of Science.",
  "Ahn et al. 2012, ApJS 203, 21"),
 "SkyMapper": ("SkyMapper Southern Sky Survey", "CDS/P/skymapper-{U,G,R,I,Z}",
  "The national facility capability for SkyMapper has been funded through ARC LIEF grant LE130100104 from the Australian Research Council, awarded to the University of Sydney, the Australian National University, Swinburne University of Technology, the University of Queensland, the University of Western Australia, the University of Melbourne, Curtin University of Technology, Monash University and the Australian Astronomical Observatory. SkyMapper is owned and operated by The Australian National University's Research School of Astronomy and Astrophysics.",
  "Wolf et al. 2018, PASA 35, e010"),
 "Legacy": ("DESI Legacy Imaging Surveys DR10", "CDS/P/DESI-Legacy-Surveys/DR10/{g,r,i,z,color}",
  "The Legacy Surveys consist of three projects: the Dark Energy Camera Legacy Survey (DECaLS), the Beijing-Arizona Sky Survey (BASS) and the Mayall z-band Legacy Survey (MzLS). DR10 also includes DECam data from DES and other public programmes. The Legacy Surveys project is honored to be permitted to conduct astronomical research on Iolkam Du'ag (Kitt Peak), a mountain with particular significance to the Tohono O'odham Nation.",
  "Dey et al. 2019, AJ 157, 168"),
 "DES": ("Dark Energy Survey (DES) DR2", "CDS/P/DES-DR2/{g,r,i,z,Y,ColorIRG}",
  "This project used public archival data from the Dark Energy Survey (DES), funded by the U.S. Department of Energy, the U.S. National Science Foundation and the collaborating institutions listed at darkenergysurvey.org, based on observations at Cerro Tololo Inter-American Observatory, NSF NOIRLab.",
  "Abbott et al. 2021, ApJS 255, 20"),
 "VVV": ("VISTA Variables in the Vía Láctea (VVV) DR4", "CDS/P/VISTA/VVV/DR4/Y",
  "Based on observations with ESO telescopes at the Paranal Observatory under programme ID 179.B-2002.",
  "Minniti et al. 2010, New Astronomy 15, 433"),
 "2MASS": ("Two Micron All Sky Survey (2MASS)", "CDS/P/2MASS/J",
  "This publication makes use of data products from the Two Micron All Sky Survey, which is a joint project of the University of Massachusetts and the Infrared Processing and Analysis Center/California Institute of Technology, funded by the National Aeronautics and Space Administration and the National Science Foundation.",
  "Skrutskie et al. 2006, AJ 131, 1163"),
 "DSS2": ("Digitized Sky Survey 2 (DSS2)", "CDS/P/DSS2/{blue,red,NIR,color}",
  "The Digitized Sky Surveys were produced at the Space Telescope Science Institute under U.S. Government grant NAG W-2166. The images of these surveys are based on photographic data obtained using the Oschin Schmidt Telescope on Palomar Mountain and the UK Schmidt Telescope. The plates were processed into the present compressed digital form with the permission of these institutions.",
  "Lasker et al. 1996, ASP Conf. Ser. 101, 88"),
 "GALEX": ("GALEX GR6/7", "CDS/P/GALEXGR6_7/NUV",
  "Based on observations made with the NASA Galaxy Evolution Explorer. GALEX is operated for NASA by the California Institute of Technology under NASA contract NAS5-98034.",
  "Martin et al. 2005, ApJ 619, L1; Bianchi et al. 2017, ApJS 230, 24"),
}
SERVICES = ("This page used the hips2fits cutout service and the Sesame name resolver developed at CDS, Strasbourg Astronomical Observatory, France, the SIMBAD database (Wenger et al. 2000, A&AS 143, 9), the HiPS standard (Fernique et al. 2015, A&A 578, A114) and Astropy (Astropy Collaboration et al. 2022, ApJ 935, 167). "
            "Cutouts were reprojected, stretched and annotated for target selection only; use the original survey archives for any scientific measurement.")

def key(label):
    for k in ("PS1", "SDSS", "SkyMapper", "Legacy", "DES", "VVV", "2MASS", "DSS2", "GALEX"):
        if k in label: return k
    return None
