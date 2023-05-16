# Adaptive-Mean-and-Median-Filters
This project implements an adaptive mean and adaptive median filter for use on images that have been corrupted by impulse noise. Observations about the difference in the effectiveness of the two filters can be drawn by the euclidean distance that the resulting images are from the original image.

## Usage:
<pre>
adaptive [-h] -n [percent of corrupted pixels] -t input_image -s [output_image] -m [output_image]
    -t : Target Image (t)
    -s : Output Median Filtered Image
    -m : Output Mean Filtered Image
    -n : percent of corrupted pixels
    -w : mean filter window size

            </pre>
