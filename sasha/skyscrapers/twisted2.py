from mcpq import Minecraft, Vec3
import math
from common.minecraft_wrap import MinecraftWrap


def build_twisted_skyscraper():

    mc = Minecraft('192.168.1.77')

    wrap = MinecraftWrap(mc)

    # Building parameters
    base_x, base_z = 400, 400  # Center of the building
    base_y = 0  # Ground level
    floors = 50  # Number of floors
    floor_height = 6  # Height of each floor
    base_size = 48  # Size of the base floor (16 * 3)

    # Materials for different parts
    materials = {
        'foundation': 'stone bricks',
        'structure': 'smooth stone',
        'windows': 'glass',
        'window_frame': 'iron bars',
        'interior_floor': 'polished andesite',
        'walls': 'white concrete',
        'accents': 'light blue concrete',
        'roof': 'dark oak planks',
        'pillars': 'quartz pillar',
        'details': 'gold block',
        # Furniture materials
        'furniture_wood': 'oak planks',
        'furniture_dark': 'dark oak planks',
        'furniture_stone': 'stone',
        'carpet': 'red carpet',
        'bed': 'red bed',
        'bookshelf': 'bookshelf',
        'workbench': 'crafting table',
        'furnace': 'furnace',
        'chest': 'chest',
        'chair': 'oak stairs',
        'table': 'smooth stone slab',
        'lamp': 'glowstone'
    }

    def rotate_point(x, z, angle, center_x, center_z):
        """Rotate a point around a center by given angle in radians"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        dx = x - center_x
        dz = z - center_z
        new_x = center_x + dx * cos_a - dz * sin_a
        new_z = center_z + dx * sin_a + dz * cos_a
        return new_x, new_z

    def build_foundation():
        """Build the foundation and basement levels"""
        # Deep foundation
        for y in range(base_y - 5, base_y):
            size = base_size + 4
            wrap.set_block_cube(materials['foundation'],
                                Vec3(base_x - size // 2, y, base_z - size // 2),
                                Vec3(base_x + size // 2, y, base_z + size // 2))

        # Ground level platform
        size = base_size + 2
        wrap.set_block_cube(materials['structure'],
                            Vec3(base_x - size // 2, base_y, base_z - size // 2),
                            Vec3(base_x + size // 2, base_y, base_z + size // 2))

    def build_floor(floor_num, y_level):
        """Build a single floor with twist and details"""
        # Calculate twist angle (0 to 180 degrees over the height)
        twist_angle = (floor_num / floors) * math.pi

        # Calculate floor size (tapers as it goes up)
        size_reduction = floor_num * 0.3
        current_size = max(8, base_size - size_reduction)

        # Create floor corners with twist
        corners = []
        half_size = current_size / 2
        base_corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]

        for corner_x, corner_z in base_corners:
            new_x, new_z = rotate_point(corner_x, corner_z, twist_angle, 0, 0)
            corners.append((int(base_x + new_x), int(base_z + new_z)))

        # Build floor structure
        # Floor slab
        for x in range(int(base_x - current_size // 2), int(base_x + current_size // 2 + 1)):
            for z in range(int(base_z - current_size // 2), int(base_z + current_size // 2 + 1)):
                rotated_x, rotated_z = rotate_point(x - base_x, z - base_z, twist_angle, 0, 0)
                if abs(rotated_x) <= current_size // 2 and abs(rotated_z) <= current_size // 2:
                    wrap.set_block(materials['interior_floor'], Vec3(x, y_level, z))

        # Walls and windows
        wall_points = []
        for i in range(4):
            start_corner = corners[i]
            end_corner = corners[(i + 1) % 4]

            # Calculate wall points
            dx = end_corner[0] - start_corner[0]
            dz = end_corner[1] - start_corner[1]
            wall_length = max(abs(dx), abs(dz))

            if wall_length > 0:
                for j in range(wall_length + 1):
                    t = j / wall_length if wall_length > 0 else 0
                    wall_x = int(start_corner[0] + t * dx)
                    wall_z = int(start_corner[1] + t * dz)
                    wall_points.append((wall_x, wall_z))

        # Build walls with windows
        for wall_x, wall_z in wall_points:
            for wall_y in range(y_level + 1, y_level + floor_height - 1):
                # Determine if this should be a window
                is_window_level = (wall_y - y_level) in [2, 3, 4]
                is_window_position = ((wall_x + wall_z + floor_num) % 3) != 0

                if is_window_level and is_window_position:
                    wrap.set_block(materials['windows'], Vec3(wall_x, wall_y, wall_z))
                    # Window frame
                    if (wall_y - y_level) in [2, 4]:
                        wrap.set_block(materials['window_frame'], Vec3(wall_x, wall_y, wall_z))
                else:
                    wrap.set_block(materials['walls'], Vec3(wall_x, wall_y, wall_z))

        # Corner pillars
        for corner_x, corner_z in corners:
            for pillar_y in range(y_level, y_level + floor_height):
                wrap.set_block(materials['pillars'], Vec3(corner_x, pillar_y, corner_z))

        # Interior details for every 5th floor
        if floor_num % 5 == 0:
            # Central support pillar
            wrap.set_block(materials['pillars'], Vec3(base_x, y_level + floor_height - 1, base_z))

            # Decorative elements
            for dx in [-2, 0, 2]:
                for dz in [-2, 0, 2]:
                    if dx != 0 or dz != 0:
                        detail_x, detail_z = rotate_point(dx, dz, twist_angle, 0, 0)
                        wrap.set_block(materials['accents'],
                                       Vec3(int(base_x + detail_x), y_level + floor_height - 1,
                                            int(base_z + detail_z)))

        # Special floors with unique features
        if floor_num == floors // 3:  # Observation deck
            # Extended platform
            for x in range(int(base_x - current_size // 2 - 2), int(base_x + current_size // 2 + 3)):
                for z in range(int(base_z - current_size // 2 - 2), int(base_z + current_size // 2 + 3)):
                    rotated_x, rotated_z = rotate_point(x - base_x, z - base_z, twist_angle, 0, 0)
                    if abs(rotated_x) <= current_size // 2 + 2 and abs(rotated_z) <= current_size // 2 + 2:
                        wrap.set_block(materials['details'], Vec3(x, y_level + floor_height, z))

        if floor_num == floors * 2 // 3:  # Sky garden level
            # Garden elements
            for x in range(int(base_x - current_size // 4), int(base_x + current_size // 4 + 1)):
                for z in range(int(base_z - current_size // 4), int(base_z + current_size // 4 + 1)):
                    rotated_x, rotated_z = rotate_point(x - base_x, z - base_z, twist_angle, 0, 0)
                    if abs(rotated_x) <= current_size // 4 and abs(rotated_z) <= current_size // 4:
                        wrap.set_block('grass_block', Vec3(x, y_level + 1, z))
                        if (x + z) % 4 == 0:
                            wrap.set_block('oak_leaves', Vec3(x, y_level + 2, z))

    def build_roof():
        """Build the roof and spire"""
        roof_y = base_y + floors * floor_height
        roof_twist = math.pi  # Full 180-degree twist at the top

        # Main roof structure
        roof_size = max(6, base_size - floors * 0.3)
        for level in range(4):
            current_roof_size = roof_size - level * 1.5
            if current_roof_size <= 0:
                break

            level_twist = roof_twist + level * 0.2

            for x in range(int(base_x - current_roof_size // 2), int(base_x + current_roof_size // 2 + 1)):
                for z in range(int(base_z - current_roof_size // 2), int(base_z + current_roof_size // 2 + 1)):
                    rotated_x, rotated_z = rotate_point(x - base_x, z - base_z, level_twist, 0, 0)
                    if abs(rotated_x) <= current_roof_size // 2 and abs(rotated_z) <= current_roof_size // 2:
                        wrap.set_block(materials['roof'], Vec3(x, roof_y + level, z))

        # Spire
        spire_height = 8
        for i in range(spire_height):
            spire_y = roof_y + 4 + i
            spire_twist = roof_twist + i * 0.3

            # Spire gets smaller as it goes up
            spire_size = max(1, 3 - i // 2)

            for dx in range(-spire_size, spire_size + 1):
                for dz in range(-spire_size, spire_size + 1):
                    if abs(dx) + abs(dz) <= spire_size:
                        rotated_x, rotated_z = rotate_point(dx, dz, spire_twist, 0, 0)
                        wrap.set_block(materials['details'],
                                       Vec3(int(base_x + rotated_x), spire_y, int(base_z + rotated_z)))

        # Top ornament
        wrap.set_block('beacon', Vec3(base_x, roof_y + 4 + spire_height, base_z))

    def build_external_features():
        """Add external features like balconies and architectural details"""
        for floor_num in range(1, floors):
            if floor_num % 7 == 0:  # Balcony every 7 floors
                y_level = base_y + floor_num * floor_height
                twist_angle = (floor_num / floors) * math.pi
                current_size = max(8, base_size - floor_num * 0.3)

                # Add balcony extensions
                balcony_points = [
                    (current_size // 2 + 1, 0),
                    (-(current_size // 2 + 1), 0),
                    (0, current_size // 2 + 1),
                    (0, -(current_size // 2 + 1))
                ]

                for bal_x, bal_z in balcony_points:
                    rotated_x, rotated_z = rotate_point(bal_x, bal_z, twist_angle, 0, 0)
                    balcony_x = int(base_x + rotated_x)
                    balcony_z = int(base_z + rotated_z)

                    # Balcony floor
                    wrap.set_block(materials['accents'], Vec3(balcony_x, y_level + 1, balcony_z))
                    # Balcony railing
                    wrap.set_block(materials['window_frame'], Vec3(balcony_x, y_level + 2, balcony_z))

    # Build the complete skyscraper
    print("Building foundation...")
    build_foundation()

    print("Building floors...")
    for floor in range(floors):
        y_level = base_y + floor * floor_height
        build_floor(floor, y_level)
        if floor % 5 == 0:
            print(f"Completed floor {floor}/{floors}")

    print("Building roof and spire...")
    build_roof()

    print("Adding external features...")
    build_external_features()

    print("Rendering to Minecraft...")
    wrap.draw()

    print(f"Twisted skyscraper completed! {floors} floors with full 180° twist.")
    print("Features included:")
    print("- Gradual twist from base to top")
    print("- Individual floor details")
    print("- Windows with frames")
    print("- Corner pillars")
    print("- Observation deck")
    print("- Sky garden level")
    print("- Balconies every 7 floors")
    print("- Decorative spire with beacon")


if __name__ == "__main__":
    build_twisted_skyscraper()
