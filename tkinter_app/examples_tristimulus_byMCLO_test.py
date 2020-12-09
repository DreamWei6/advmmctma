'''
Created on 2020年11月25日

@author: kankuni
'''
import colorimetry.examples_tristimulus_byMCLO as calXYZ
import colour
'''

'''
NUM_SPEC = 36#31
def main():
    calXYZ1 = calXYZ.CalulateTristimulusValues()
    
    # Create a list hold the sample's SR for test
    specs = [0] * NUM_SPEC
    # Get the specs for each day
    for index in range(len(specs)):
#         specs[index] = 400 + 10 * index
        specs[index] = 380 + 10 * index
    # open a file for reading
#     infile = open('CyanSolid_SR.txt', 'r', encoding = "utf-8")
    infile = open('CC_NO1.txt', 'r', encoding = "utf-8")
    
    # Read the contents of the sample's SR file into a list
    sample_sr_data = infile.readlines()
    # Close the file
    infile.close()
    
    # Strip the \n from each element
    for index in range(len(sample_sr_data)):
        sample_sr_data[index] = sample_sr_data[index].rstrip("\n")
    
    # Print the contents of the list
    print('only SR', sample_sr_data)
    
    # Using dictionary comprehension
    # to convert lists to dictionary
    sample_sd_data = {specs[i]: sample_sr_data[i] for i in range(len(sample_sr_data))}
    print('\nUse an if clause in a dictionary comprehension:\n', sample_sd_data)
    XYZ = calXYZ1.get_XYZ(sample_sd_data, 380, 780, 5)
    calXYZ1.get_illuminat_xy_chromaticity_coordinates(calXYZ1.get_illuminant(), calXYZ1.get_cmfs(), XYZ)

if __name__ == '__main__':
    main()