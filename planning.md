# Planning

# General
- Must look at what image colourspace is being inputted (RGB, RGBA, HSV, etc)
and match it, else processing images will be hard

# Cropping
- *Selection value* fields should be number inputs like min/max size
- Bonus feature: Smart cropping like how Samsung Gallery app does it
- *Aspect ratio* should have choices rather than text field
    - 4:3
    - 3:4
    - 16:9
    - 9:16
    - 1:1
    - 1.618 (golden ratio)
    - Free

# Gray level mapping
- Include defaults
    - Negative
    - Common power laws

# Kernels
- Include defaults
    - `box` -> Box blur
    - `gauss` -> Gaussian blur
    - `high-pass` -> High-pass filter
    - `low-pass` -> Low-pass filter
    - `sobel` -> Sobel filter

# Bonus Features
- Cropping: Smart cropping
- Pull EXIF data from the image
- Background removal via chroma key
- Colourize images
- Undo button with the Undo Guy from Kidpix
