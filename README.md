# 3D Cube Transformations

This project creates a 3D object composed of 5 different colored cubes and applies various geometric transformations to it.

## Features

- **5-Cube Object**: Creates an object made of 5 cubes in different colors:
  - Red cube (center)
  - Blue cube (right)
  - Green cube (back)
  - Yellow cube (top)
  - Purple cube (left)

- **Geometric Transformations**:
  - Rotation (around X, Y, Z axes)
  - Translation (movement in 3D space)
  - Scaling (resize along different axes)
  - Reflection (mirroring)
  - Combined transformations

- **Visualizations**:
  - Static display showing 6 different transformations
  - Animated version with continuous transformations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the main script to see both static and animated transformations:

```bash
python cube_transformations.py
```

## Transformations Demonstrated

1. **Original Object**: The base 5-cube structure
2. **Rotation**: 45° around X, 30° around Y, 60° around Z
3. **Translation**: Move by (1, 1, 1) units
4. **Scaling**: Scale by factors (1.5, 0.5, 2.0)
5. **Combined**: Rotation + Translation + Scaling
6. **Reflection**: Mirror across the YZ plane
7. **Animation**: Continuous transformations over time

## Code Structure

- `Cube`: Class representing a single colored cube
- `CubeObject`: Class managing the 5-cube object
- Transformation matrices for rotation, translation, scaling
- Visualization functions using matplotlib 3D
- Animation system for continuous transformations

The program uses homogeneous coordinates and 4x4 transformation matrices for all geometric operations.