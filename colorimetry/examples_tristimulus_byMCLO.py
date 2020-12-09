# -*- coding: utf-8 -*-
"""
Showcases *CIE XYZ* tristimulus values computations.
"""

import numpy as np

import colour
from colour.utilities import message_box
from colorimetry.examples_spectrum import clone_sd
from colorimetry.examples_correction import sample_sd_data
from pip._vendor.pyparsing import col
from colorimetry.examples_tristimulus import illuminant
from colour.examples.phenomena.examples_rayleigh import wavelength

class CalulateTristimulusValues:
    
    def __init__(self): 
        self.__cmfs = colour.CMFS['CIE 1931 2 Degree Standard Observer']
        self.__illuminant = colour.ILLUMINANTS_SDS['D50']

    def set_spec(self, spec):
        self.__spec = spec

    def get_cmfs(self):
        return self.__cmfs
    
    def get_illuminant(self):
        return self.__illuminant

    def get_XYZ(self, sample_sd_data, min_w, max_w, interval_w):
        message_box('"CIE XYZ" Tristimulus Values Computations')
        
        '''
        sample_sd_data = {
            380: 0.048,
            385: 0.051,
            390: 0.055,
            395: 0.060,
            400: 0.065,
            405: 0.068,
            410: 0.068,
            415: 0.067,
            420: 0.064,
            425: 0.062,
            430: 0.059,
            435: 0.057,
            440: 0.055,
            445: 0.054,
            450: 0.053,
            455: 0.053,
            460: 0.052,
            465: 0.052,
            470: 0.052,
            475: 0.053,
            480: 0.054,
            485: 0.055,
            490: 0.057,
            495: 0.059,
            500: 0.061,
            505: 0.062,
            510: 0.065,
            515: 0.067,
            520: 0.070,
            525: 0.072,
            530: 0.074,
            535: 0.075,
            540: 0.076,
            545: 0.078,
            550: 0.079,
            555: 0.082,
            560: 0.087,
            565: 0.092,
            570: 0.100,
            575: 0.107,
            580: 0.115,
            585: 0.122,
            590: 0.129,
            595: 0.134,
            600: 0.138,
            605: 0.142,
            610: 0.146,
            615: 0.150,
            620: 0.154,
            625: 0.158,
            630: 0.163,
            635: 0.167,
            640: 0.173,
            645: 0.180,
            650: 0.188,
            655: 0.196,
            660: 0.204,
            665: 0.213,
            670: 0.222,
            675: 0.231,
            680: 0.242,
            685: 0.251,
            690: 0.261,
            695: 0.271,
            700: 0.282,
            705: 0.294,
            710: 0.305,
            715: 0.318,
            720: 0.334,
            725: 0.354,
            730: 0.372,
            735: 0.392,
            740: 0.409,
            745: 0.420,
            750: 0.436,
            755: 0.450,
            760: 0.462,
            765: 0.465,
            770: 0.448,
            775: 0.432,
            780: 0.421
        }'''
        
        print(type(sample_sd_data))
        
        sd = colour.SpectralDistribution(sample_sd_data, name='Sample')
        clone_sd = sd.copy()
        print(id(sd), id(clone_sd))
        print('\n')
        
        message_box('Sample spectrol distrubtion interpolation')
        clone_sd.extrapolate(colour.SpectralShape(min_w, max_w, interval_w))
        print(clone_sd[666])
        
        print('\nUse an if clause in a dictionary comprehension (308~780):\n', clone_sd)
        
        cmfs = colour.CMFS['CIE 1931 2 Degree Standard Observer']
        illuminant = colour.ILLUMINANTS_SDS['D50']
        
        message_box(('Computing *CIE XYZ* tristimulus values for sample spectral '
                     'distribution and "CIE Standard Illuminant D50".'))
        
        XYZ = colour.sd_to_XYZ(clone_sd, cmfs, illuminant)
        print(colour.sd_to_XYZ(sd, cmfs, illuminant))
        
        print('\n')
        
        message_box(('Converting to "RBG" colourspace from given "CIE XYZ"'
                     'tristimulus values:\n'
                     '\n\t{0}'.format(XYZ)))
        D50 = colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D50']
        
        print(
            colour.XYZ_to_RGB(
                XYZ,
                D50,
                colour.RGB_COLOURSPACES['sRGB'].whitepoint,
                colour.RGB_COLOURSPACES['sRGB'].XYZ_to_RGB_matrix,
                'Bradford',
                colour.RGB_COLOURSPACES['sRGB'].cctf_encoding,
                ))
        
        print('\n')
        return XYZ

    def get_illuminat_xy_chromaticity_coordinates(self, illuminant, cmfs, XYZ):
        message_box(('Computing "CIE Standard Illuminant A" chromaticity coordinates '
                     'from its spectral distribution.'))
        print(colour.XYZ_to_xy(XYZ))
        
        print('\n')
        
    def get_XYZ_for_a_single_specified_wavelength(self, wavelength):
        message_box(('Computing *CIE XYZ* tristimulus values for a single given '
                     'wavelength in nm.'))
        print(
            colour.wavelength_to_XYZ(
                wavelength, colour.CMFS['CIE 1931 2 Degree Standard Observer']))
        
    def get_XYZ_from_given_multi_spectral_image(self, cmfs, illuminant):
        message_box(('Computing *CIE XYZ* tristimulus values from given '
                     'multi-spectral image with shape (4, 3, 6).'))
        msds = np.array([
            [[0.01367208, 0.09127947, 0.01524376, 0.02810712, 0.19176012, 0.04299992],
             [0.00959792, 0.25822842, 0.41388571, 0.22275120, 0.00407416, 0.37439537],
             [0.01791409, 0.29707789, 0.56295109, 0.23752193, 0.00236515, 0.58190280]],
            [[0.01492332, 0.10421912, 0.02240025, 0.03735409, 0.57663846, 0.32416266],
             [0.04180972, 0.26402685, 0.03572137, 0.00413520, 0.41808194, 0.24696727],
             [0.00628672, 0.11454948, 0.02198825, 0.39906919, 0.63640803, 0.01139849]],
            [[0.04325933, 0.26825359, 0.23732357, 0.05175860, 0.01181048, 0.08233768],
             [0.02484169, 0.12027161, 0.00541695, 0.00654612, 0.18603799, 0.36247808],
             [0.03102159, 0.16815442, 0.37186235, 0.08610666, 0.00413520, 0.78492409]],
            [[0.11682307, 0.78883040, 0.74468607, 0.83375293, 0.90571451, 0.70054168],
             [0.06321812, 0.41898224, 0.15190357, 0.24591440, 0.55301750, 0.00657664],
             [0.00305180, 0.11288624, 0.11357290, 0.12924391, 0.00195315, 0.21771573]],
        ])
        print(
            colour.multi_sds_to_XYZ(
                msds,
                cmfs,
                illuminant,
                method='Integration',
                shape=colour.SpectralShape(400, 700, 60)))
