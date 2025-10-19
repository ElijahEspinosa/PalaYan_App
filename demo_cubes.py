#!/usr/bin/env python3
"""
Simple demo script to show the 5-cube object and basic transformations
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_cube_vertices(center, size=1.0):
    """Create vertices for a cube centered at given position"""
    s = size / 2
    vertices = np.array([
        [-s, -s, -s], [+s, -s, -s], [+s, +s, -s], [-s, +s, -s],  # bottom face
        [-s, -s, +s], [+s, -s, +s], [+s, +s, +s], [-s, +s, +s],  # top face
    ]) + center
    return vertices

def get_cube_faces(vertices):
    """Get the 6 faces of a cube"""
    return [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
        [vertices[4], vertices[7], vertices[6], vertices[5]],  # top
        [vertices[0], vertices[4], vertices[5], vertices[1]],  # front
        [vertices[2], vertices[6], vertices[7], vertices[3]],  # back
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # left
        [vertices[1], vertices[5], vertices[6], vertices[2]],  # right
    ]

def main():
    # Define the 5 cubes with different colors and positions
    cubes = [
        {'center': [0, 0, 0], 'color': 'red', 'name': 'Center'},
        {'center': [2, 0, 0], 'color': 'blue', 'name': 'Right'},
        {'center': [0, 2, 0], 'color': 'green', 'name': 'Back'},
        {'center': [0, 0, 2], 'color': 'yellow', 'name': 'Top'},
        {'center': [-2, 0, 0], 'color': 'purple', 'name': 'Left'},
    ]
    
    # Create figure
    fig = plt.figure(figsize=(12, 8))
    
    # Original configuration
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    all_faces = []
    all_colors = []
    
    for cube in cubes:
        vertices = create_cube_vertices(cube['center'])
        faces = get_cube_faces(vertices)
        for face in faces:
            all_faces.append(face)
            all_colors.append(cube['color'])
    
    poly3d = Poly3DCollection(all_faces, alpha=0.7, linewidths=1, edgecolors='black')
    poly3d.set_facecolors(all_colors)
    ax1.add_collection3d(poly3d)
    
    ax1.set_xlim([-3, 3])
    ax1.set_ylim([-3, 3])
    ax1.set_zlim([-3, 3])
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Original 5-Cube Object')
    
    # Rotated version
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    
    # Apply rotation matrix (45 degrees around each axis)
    angle = np.pi / 4
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    
    all_faces_rot = []
    all_colors_rot = []
    
    for cube in cubes:
        # Rotate the center position
        rotated_center = rotation_matrix @ np.array(cube['center'])
        vertices = create_cube_vertices(rotated_center)
        # Also rotate each vertex
        vertices = np.array([rotation_matrix @ v for v in vertices])
        
        faces = get_cube_faces(vertices)
        for face in faces:
            all_faces_rot.append(face)
            all_colors_rot.append(cube['color'])
    
    poly3d_rot = Poly3DCollection(all_faces_rot, alpha=0.7, linewidths=1, edgecolors='black')
    poly3d_rot.set_facecolors(all_colors_rot)
    ax2.add_collection3d(poly3d_rot)
    
    ax2.set_xlim([-3, 3])
    ax2.set_ylim([-3, 3])
    ax2.set_zlim([-3, 3])
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('Rotated 5-Cube Object (45° around Z)')
    
    plt.tight_layout()
    plt.savefig('demo_cubes.png', dpi=150, bbox_inches='tight')
    print("Demo saved as 'demo_cubes.png'")
    
    # Print cube information
    print("\n5-Cube Object Composition:")
    print("=" * 30)
    for i, cube in enumerate(cubes, 1):
        print(f"{i}. {cube['name']} cube at position {cube['center']} - Color: {cube['color']}")
    
    print("\nTransformations Applied:")
    print("=" * 25)
    print("1. Original configuration")
    print("2. 45-degree rotation around Z-axis")

if __name__ == "__main__":
    main()