# Color Correction

This repo performs color correction and texture analysis using [Colour](https://www.colour-science.org/) and [scikit-image](https://scikit-image.org/) libraries. The color correction also uses opencv to automatically find color correction charts embedded in images.

To run the examples the easiest thing to do is to start with a clean virtual environment. After you clone the repo, create the virtual environment and install the requirements.

```
python3 -m venv color-venv
source color-venv/bin/activate
pip install -r requirements.txt
```
then start jupyter and you should be able to run the code in `photo_transform.ipynb` and `texture_assement.ipynb`.

## Explanation of files
- `SpyderCHECKR24.py`: This defines the colors used in the SpyderCHECKR24 color calibration chart
- `ColorCorrect.py`: This is a convienence function which calls the `colour.colour_correction`, as well as handling color space transformations.
- `batch_colorcorrect.py`: This is a script to loop through all images in `JPG_uncorrected` and performing color correction on them.
- `photo_transform.ipynb`: This is an example color correction calculation.
- `texture_assessment.ipynb`: This is an example texture calculation.
