import os
import pathlib
import colour
import json
import numpy

import ColorCorrect
import SpyderCHECKR24


IN_DIR = 'JPG_uncorrected'
OUT_DIR = 'JPG_corrected'

# get all files in the input directory
# filter all the *.JPG files
files = [file for file in os.listdir(IN_DIR) if file.endswith('JPG')]
processed = [file for file in os.listdir(OUT_DIR) if file.endswith('JPG')]

files = [file for file in files if pathlib.Path(file).stem + '_corrected' + pathlib.Path(file).suffix not in processed]
files = [file for file in files if file[0] != 'z']

def process(file):
    path = pathlib.Path(file)
    filename = path.stem
    extension = path.suffix
 
    print("processing {:}".format(filename))
    try:
        image = colour.cctf_decoding(
            colour.io.read_image(os.path.join(IN_DIR, file), method='Imageio'), function='sRGB')

        corrected_image = numpy.clip(ColorCorrect.color_correct(
            image, SpyderCHECKR24.colour_checker, method='Finlayson 2015'), 0.0, 1.0)

        output_filename = os.path.join(
            OUT_DIR, filename + '_corrected' + extension)
        colour.io.write_image(
            colour.cctf_encoding(corrected_image, function='sRGB'), output_filename, bit_depth='uint8', method='Imageio')
    except:
        print("error processing {:}".format(filename))

print(files)


from multiprocessing import Pool
p = Pool(16)
p.map(process, files)