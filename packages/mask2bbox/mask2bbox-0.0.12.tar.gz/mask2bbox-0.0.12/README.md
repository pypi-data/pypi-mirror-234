# mask2bbox
[![PyPI](https://img.shields.io/pypi/v/mask2bbox?style=flat-square)](https://pypi.org/project/mask2bbox/)

For a given mask, gets the coordinates of bounding box of each element of the mask. It will also allow for more operations in the future.

## Instalation

`pip install mask2bbox`

## Usage

```python
import numpy as np
from mask2bbox import BBoxes

# Create a BBoxes object
all_boxes = BBoxes.from_mask("path/to/mask.png")

# Expand the bounding boxes
all_boxes = all_boxes.expand(n=10)

# Remove the bounding boxes that are located on the edge of the image
all_boxes = all_boxes.remove_from_edge()

# Get the sides of all the bounding boxes
sides = all_boxes.get("sides")

# Filter the bounding boxes by the sides
filtered_boxes = all_boxes.filter("sides", np.greater_equal, (35, 35))

# Get the IoU matrix of all the bounding boxes
iou = filtered_boxes.iou_matrix()

# Save the IoU matrix to a csv file
filtered_boxes.save_iou("path/to/save/iou.csv")

# Plot the bounding boxes on the mask image
filtered_boxes.draw(to="image", method="matplotlib", show="False", save="path/to/save/image.png")

# Save your bounding boxes
filtered_boxes.save_csv("path/to/bounding_boxes.csv")

# Get resize factors to resize the bounding boxes to a given size
resize_factors = filtered_boxes.de(desired_ratio=0.7, size=(256, 256))

# Extract the bounding boxes as images
filtered_boxes.extract(resize_factors, size=(256, 256), output="path/to/save/images")
```

## Version Notes

### 0.0.12 - Update
- Update:
  - `BBoxes.from_mask()` now accepts an image parameter as an additional input, this removes the need of having to load the image separately.
  - `__getitem__` magic attribute indexes based on the cell/mask id (making it base 1 instead of base 0).
- Replaced `BBoxes.extract_single()` and `BBoxes.grab()` -> with `BBoxes.grab_pixels_from()`
  - `BBoxes.grab_pixels_from()` gets the pixels from the image/mask that are inside the bounding boxes.
  - `BBoxes.grab_pixels_from()` makes optional the processing steps implemented in `BBoxes.extract()`.

### 0.0.11 - Added functionality
- Added `BBoxes.grab()`
- Replaced `plot_to_mask()`  and `BBoxes.plot_to_image()` -> with `BBoxes.draw()` 
  - `BBoxes.draw()` allows to plot the bounding boxes on the mask or the image.
  - `BBoxes.draw()` allows to choose between `matplotlib` and `numpy` to generate the plot.
- Modified `BBoxes.extract_single()`
  - `BBoxes.extract_single()` adds pre-processing steps such as `BBoxes.extract()`

### 0.0.10 - Added functionality
- Added `extract_single()`: This method allows to extract a single bounding box form the image/mask.
- Added check to `BBoxes.from_mask()`: Now the method checks if the mask contains any element or not and raises an error if it doesn't.

### 0.0.9 - Fix bug in `BBoxes.extract()`
- Fix bug in `BBoxes.extract()` that caused the images to be saved with the wrong name amd created a new folder.

### 0.0.8 - Change methods, change constructor, added functionality. 
- **Constructor:** BBox object is now constructed with the syntax `BBoxes.from_mask(mask)` instead of `BBoxes(mask)`.
- **Operations:** BBox object operations are no longer performed in place, the affected methods are:
  - `BBoxes.remove_from_edge()`
  - `BBoxes.expand()`
  - `BBoxes.filter()`

- **Removed methods:**
  - `is_area_smaller_than()`
  - `is_area_larger_than()`
  - `are_dims_smaller_than()`
  - `are_dims_larger_than()`
  - `filter_identities()`  

These methods used in-place operations and are no longer needed, they were substituted with.  
- **Renamed:**
  - `BBoxes.get_bbox_areas()` -> `BBoxes.get_areas()`
  - `BBoxes.get_bbox_dims()` -> `BBoxes.get_sizes()`
  - `BBoxes.get_bbox_centers()` -> `BBoxes.get_centers()`
  - `BBoxes.get_bbox_ratios()` -> `BBoxes.get_ratios()`
  
- **New methods:**
  - `BBoxes.filter():` This method allows to filter the bounding boxes by any of the attributes in the object specifying the comparison operator and threshold value. It returns a new BBoxes object with the filtered values.
  - `BBoxes.get():` This method allows to get the values of the attributes in the object. It works as a simplification to `BBoxes.get_areas()`, `BBoxes.get_centers()`, `BBoxes.get_sizes()` and `BBoxes.get_ratios()`.
  - `BBoxes.extract():` This new method isolates the bounding boxes as images and saves them to the desired location.
  - `BBoxes.calculate_resizing_factor():` This method calculates the resizing factor needed to resize the bounding boxes to a given size.
  - `BBoxes._pad_crop():` Helper method to pad or crop the bounding boxes to a desired output size.
  - `BBoxes.plot_to_image():` This method plots the bounding boxes to the corresponding image and saves it to the desired location.


### 0.0.7 - Improved functionality
Improvements in IoU calculation

### 0.0.6 - Added functionality

### 0.0.5 - Added functionality

- IoU related operations:
  - `boxes.get_iou_matrix()` - Gets the IoU of all the bounding boxes.
  - `boxes.are_overlaping()` - Returns identities where the IoU is greater than 0
  - `boxes.overlaping_pais()` - Returns the pairs of bounding boxes that are overlaping.
  - `boxes.save_iou()` - Saves the IoU matrix to a csv file.

- Plots
  - `boxes.plot_to_mask()` Plots the bounding boxes on the mask image.

Example of `boxes.plot_to_mask()`
![](tests/plot.png)

### 0.0.4 - Added functionality
Now is possible to extract:
- Bounding boxes dimensions `BBoxes.get_bbox_dims()`
- Bounding boxes area `BBoxes.get_bbox_areas()`
- Bounding boxes center `BBoxes.get_bbox_centers()`
- Bounding boxes ratios `BBoxes.get_bbox_ratios()`

### 0.0.3 - Added functionality  
Added the remove_edge_boxes method to remove the bounding boxes that are located on the edge of the image.

### 0.0.2 - Added the expand method to expand the bounding boxes by a given number of pixels.
Added the expand method to expand the bounding boxes by a given number of pixels.  
Fixed a bug in the setup.py file that made it hard to import the package.

### 0.0.1 - Initial release of the package.
Initial release of the package. It allows to get the bounding boxes of a mask and save them to a csv file.
