# -*- coding: utf-8 -*-
"""
Showcases colour temperature and correlated colour temperature plotting
examples.
"""

import colour
from colour.plotting import (
    colour_style, plot_planckian_locus_in_chromaticity_diagram_CIE1931,
    plot_planckian_locus_in_chromaticity_diagram_CIE1960UCS, plot_blackbody_colours)
from colour.utilities import message_box

class illuminamisInDiagram:
    def __init__(self):
        message_box('Colour Temperature and Correlated Colour Temperature Plots')

        colour_style()

    def plot_in_chromaticity_diagram_CIE1931(self):
        message_box('Plotting planckian locus in "CIE 1931 Chromaticity Diagram".')
        plot_planckian_locus_in_chromaticity_diagram_CIE1931(['A', 'D65', 'D50', 'D55', 'D75'])
        
        print('\n')
        
    def plot_in_chromaticity_diagram_CIE1960(self):
        message_box('Plotting planckian locus in "CIE 1960 UCS Chromaticity Diagram".')
        plot_planckian_locus_in_chromaticity_diagram_CIE1960UCS(['A', 'D65', 'D50', 'D55', 'D75'])

        print('\n')
        
    def plot_blackbody_colors(self):
        message_box('Plotting "blackbody" colours.')
        plot_blackbody_colours()
        
        