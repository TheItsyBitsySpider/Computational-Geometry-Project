# Computational-Geometry-Project
Written by Cole Salvato (ColeSalvato@gmail.com)

## Usage

### Installation

This project is written in python 3.10 and cannot be guaranteed to work in any other versions. to install required libraries, navigate to this directory and run

```pip install -r requirements.txt```

### Demo

```python testall.py```

This sample program renders an image of a toy boat and has prompts for rotating it. Typing ```spin``` will cause it to spin in a circle. This may take some time.

## Implementation

### Rasterizer
The rasterizer object requires a few things when it's created:

* An nx3x3 array of the cornerd of triangles to display
* An nx3 array of rgb colors to display the triangles in
* Optionally, an int representing the pixel width of the ouput window
* Optionally, an int representing the pixel height of the ouput window
* Optionally, an array of length 3 specifying the color of the background

The callable functions are as follows:

#### rasterize()
Renders the scene with the current parameters as specified in the initial declaration. Returns a 3d array of pixels (x,y,rgb).

#### rotate(rotation matrix)
This will rotate all triangles around the center of the screen (located at [5,5,0] world space) by a given 3x3 rotation matrix. Returns nothing.

### Display

There are no input parameters when creating the object.

#### Screen.display(image, short=False)
Displays a given image using cv2. Unless short is set to true, the window will stay open for 100 seconds or until the user presses a button.
