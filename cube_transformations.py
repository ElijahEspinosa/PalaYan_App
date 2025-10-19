import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

class Cube:
    def __init__(self, position, size=1.0, color='blue'):
        """
        Create a cube at given position with specified size and color
        """
        self.position = np.array(position)
        self.size = size
        self.color = color
        self.vertices = self._generate_vertices()
    
    def _generate_vertices(self):
        """Generate the 8 vertices of a cube"""
        s = self.size / 2
        vertices = np.array([
            [-s, -s, -s],  # 0
            [+s, -s, -s],  # 1
            [+s, +s, -s],  # 2
            [-s, +s, -s],  # 3
            [-s, -s, +s],  # 4
            [+s, -s, +s],  # 5
            [+s, +s, +s],  # 6
            [-s, +s, +s],  # 7
        ])
        return vertices + self.position
    
    def get_faces(self):
        """Get the 6 faces of the cube for rendering"""
        vertices = self.vertices
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
            [vertices[4], vertices[7], vertices[6], vertices[5]],  # top
            [vertices[0], vertices[4], vertices[5], vertices[1]],  # front
            [vertices[2], vertices[6], vertices[7], vertices[3]],  # back
            [vertices[0], vertices[3], vertices[7], vertices[4]],  # left
            [vertices[1], vertices[5], vertices[6], vertices[2]],  # right
        ]
        return faces

class CubeObject:
    def __init__(self):
        """Create an object made of 5 different colored cubes"""
        self.cubes = [
            Cube([0, 0, 0], color='red'),      # Center cube
            Cube([2, 0, 0], color='blue'),     # Right cube
            Cube([0, 2, 0], color='green'),    # Back cube
            Cube([0, 0, 2], color='yellow'),   # Top cube
            Cube([-2, 0, 0], color='purple'), # Left cube
        ]
        self.original_positions = [cube.position.copy() for cube in self.cubes]
    
    def apply_transformation(self, transformation_matrix):
        """Apply a 4x4 transformation matrix to all cubes"""
        for i, cube in enumerate(self.cubes):
            # Convert to homogeneous coordinates
            pos_homogeneous = np.append(self.original_positions[i], 1)
            # Apply transformation
            new_pos = transformation_matrix @ pos_homogeneous
            # Update cube position
            cube.position = new_pos[:3]
            cube.vertices = cube._generate_vertices()
    
    def get_all_faces(self):
        """Get all faces from all cubes with their colors"""
        all_faces = []
        all_colors = []
        for cube in self.cubes:
            faces = cube.get_faces()
            for face in faces:
                all_faces.append(face)
                all_colors.append(cube.color)
        return all_faces, all_colors

def create_rotation_matrix(angle_x, angle_y, angle_z):
    """Create a 4x4 rotation matrix for rotations around x, y, z axes"""
    # Rotation around X axis
    Rx = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x), 0],
        [0, np.sin(angle_x), np.cos(angle_x), 0],
        [0, 0, 0, 1]
    ])
    
    # Rotation around Y axis
    Ry = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y), 0],
        [0, 1, 0, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y), 0],
        [0, 0, 0, 1]
    ])
    
    # Rotation around Z axis
    Rz = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0, 0],
        [np.sin(angle_z), np.cos(angle_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    return Rz @ Ry @ Rx

def create_translation_matrix(tx, ty, tz):
    """Create a 4x4 translation matrix"""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def create_scaling_matrix(sx, sy, sz):
    """Create a 4x4 scaling matrix"""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def plot_cube_object(cube_object, ax, title="Cube Object"):
    """Plot the cube object on given axes"""
    ax.clear()
    faces, colors = cube_object.get_all_faces()
    
    # Create 3D polygon collection
    poly3d = Poly3DCollection(faces, alpha=0.7, linewidths=1, edgecolors='black')
    poly3d.set_facecolors(colors)
    ax.add_collection3d(poly3d)
    
    # Set equal aspect ratio and limits
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-4, 4])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

def main():
    """Main function to demonstrate cube transformations"""
    # Create the cube object
    cube_obj = CubeObject()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # Original object
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    plot_cube_object(cube_obj, ax1, "Original Object")
    
    # Rotation transformation
    cube_obj_rot = CubeObject()
    rotation_matrix = create_rotation_matrix(np.pi/4, np.pi/6, np.pi/3)
    cube_obj_rot.apply_transformation(rotation_matrix)
    ax2 = fig.add_subplot(2, 3, 2, projection='3d')
    plot_cube_object(cube_obj_rot, ax2, "Rotated (45°, 30°, 60°)")
    
    # Translation transformation
    cube_obj_trans = CubeObject()
    translation_matrix = create_translation_matrix(1, 1, 1)
    cube_obj_trans.apply_transformation(translation_matrix)
    ax3 = fig.add_subplot(2, 3, 3, projection='3d')
    plot_cube_object(cube_obj_trans, ax3, "Translated (1, 1, 1)")
    
    # Scaling transformation
    cube_obj_scale = CubeObject()
    scaling_matrix = create_scaling_matrix(1.5, 0.5, 2.0)
    cube_obj_scale.apply_transformation(scaling_matrix)
    ax4 = fig.add_subplot(2, 3, 4, projection='3d')
    plot_cube_object(cube_obj_scale, ax4, "Scaled (1.5, 0.5, 2.0)")
    
    # Combined transformation (rotation + translation + scaling)
    cube_obj_combined = CubeObject()
    combined_matrix = translation_matrix @ rotation_matrix @ scaling_matrix
    cube_obj_combined.apply_transformation(combined_matrix)
    ax5 = fig.add_subplot(2, 3, 5, projection='3d')
    plot_cube_object(cube_obj_combined, ax5, "Combined Transform")
    
    # Reflection transformation (negative scaling)
    cube_obj_reflect = CubeObject()
    reflection_matrix = create_scaling_matrix(-1, 1, 1)  # Reflect across YZ plane
    cube_obj_reflect.apply_transformation(reflection_matrix)
    ax6 = fig.add_subplot(2, 3, 6, projection='3d')
    plot_cube_object(cube_obj_reflect, ax6, "Reflected (X-axis)")
    
    plt.tight_layout()
    plt.savefig('cube_transformations.png', dpi=150, bbox_inches='tight')
    print("Static transformations saved as 'cube_transformations.png'")
    plt.close()

def create_animation():
    """Create an animated version showing continuous transformations"""
    cube_obj = CubeObject()
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    def animate(frame):
        # Create time-varying transformations
        t = frame * 0.1
        
        # Rotating transformation
        rotation_matrix = create_rotation_matrix(t, t*0.7, t*0.5)
        translation_matrix = create_translation_matrix(
            np.sin(t) * 0.5, 
            np.cos(t) * 0.5, 
            np.sin(t*0.3) * 0.5
        )
        scaling_matrix = create_scaling_matrix(
            1 + 0.3 * np.sin(t*2),
            1 + 0.3 * np.cos(t*2),
            1 + 0.2 * np.sin(t*3)
        )
        
        # Combine transformations
        combined_matrix = translation_matrix @ rotation_matrix @ scaling_matrix
        
        # Apply to cube object
        cube_obj_anim = CubeObject()
        cube_obj_anim.apply_transformation(combined_matrix)
        
        # Plot
        plot_cube_object(cube_obj_anim, ax, f"Animated Transformations (Frame {frame})")
        
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=200, interval=50, repeat=True)
    plt.show()
    
    return anim

if __name__ == "__main__":
    print("Displaying static transformations...")
    main()
    
    print("\nCreating animated transformations...")
    anim = create_animation()