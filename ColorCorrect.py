import colour
from colour.plotting import plot_multi_colour_checkers

from colour_checker_detection import (
    colour_checkers_coordinates_segmentation,
    detect_colour_checkers_segmentation)

from colour_checker_detection.detection.segmentation import (
    adjust_image)

from collections import OrderedDict


def color_correct(image, ref_color_checker, plot=False, method='Cheung 2004', **kwargs):
    assert method in {'Finlayson 2015', 'Cheung 2004', 'Vandermonde'}

    # Find the color checker swatches
    swatches = detect_colour_checkers_segmentation(image)[0][::-1]

    # define D65 as the standard illuminant we will use
    D65 = colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']

    # convert the reference color checker to RGB, by going through XYZ and using the D65 illuminant
    ref_color_checker_RGB = colour.XYZ_to_RGB(
        colour.xyY_to_XYZ(list(ref_color_checker.data.values())),
        ref_color_checker.illuminant, D65,
        colour.RGB_COLOURSPACES['sRGB'].XYZ_to_RGB_matrix)

    # plot the color checkers overlapped with the colors extracted from the image
    if plot:
        # convert the uncorrected swatches extracted from the image from RGB to xyY by going through XYZ
        swatches_xyY = colour.XYZ_to_xyY(
            colour.RGB_to_XYZ(
                swatches, D65, D65,
                colour.RGB_COLOURSPACES['sRGB'].RGB_to_XYZ_matrix))

        # use the RGB reference color checker to correct just the color checker swatches from the image
        swatches_corrected = colour.colour_correction(
            swatches, swatches, ref_color_checker_RGB, method=method, **kwargs)

        # convert these color corrected swatches from RGB to xyY by going through XYZ
        swatches_corrected_xyY = colour.XYZ_to_xyY(
            colour.RGB_to_XYZ(
                swatches_corrected, D65, D65,
                colour.RGB_COLOURSPACES['sRGB'].RGB_to_XYZ_matrix))

        image_colour_checker = colour.characterisation.ColourChecker(
            'Uncorrected Image',
            OrderedDict(zip(ref_color_checker.data.keys(),
                            swatches_xyY)),
            D65)
        image_colour_checker_corrected = colour.characterisation.ColourChecker(
            'Corrected Image with {:}'.format(method),
            OrderedDict(zip(ref_color_checker.data.keys(),
                            swatches_corrected_xyY)),
            D65)

        plot_multi_colour_checkers(
            [ref_color_checker, image_colour_checker])

        plot_multi_colour_checkers(
            [ref_color_checker, image_colour_checker_corrected])

    return colour.colour_correction(image, swatches, ref_color_checker_RGB, method=method, **kwargs)
