from mcpq import Minecraft, Vec3
import math
import time

# Connect to Minecraft
mc = Minecraft('192.168.1.77')
mc.postToChat("Building a magnificent castle! This may take a while...")


# Castle configuration
CASTLE_BASE_X = -131
CASTLE_BASE_Y = 64
CASTLE_BASE_Z = 45
CASTLE_SIZE = 120

def build_filled_box(material, pos1, pos2):
    """Build a filled box between two positions"""
    min_x, max_x = min(pos1.x, pos2.x), max(pos1.x, pos2.x)
    min_y, max_y = min(pos1.y, pos2.y), max(pos1.y, pos2.y)
    min_z, max_z = min(pos1.z, pos2.z), max(pos1.z, pos2.z)
    
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            for z in range(int(min_z), int(max_z) + 1):
                mc.setBlock(material, Vec3(x, y, z))

def build_hollow_box(material, pos1, pos2, wall_thickness=1):
    """Build a hollow box with specified wall thickness"""
    min_x, max_x = min(pos1.x, pos2.x), max(pos1.x, pos2.x)
    min_y, max_y = min(pos1.y, pos2.y), max(pos1.y, pos2.y)
    min_z, max_z = min(pos1.z, pos2.z), max(pos1.z, pos2.z)
    
    # Build walls
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            for z in range(int(min_z), int(max_z) + 1):
                # Check if we're on the outer shell
                is_wall = (x <= min_x + wall_thickness - 1 or x >= max_x - wall_thickness + 1 or
                          z <= min_z + wall_thickness - 1 or z >= max_z - wall_thickness + 1 or
                          y == min_y or y == max_y)
                
                if is_wall:
                    mc.setBlock(material, Vec3(x, y, z))

def build_cylinder(material, center, radius, height, hollow=False, wall_thickness=1):
    """Build a cylinder (for towers)"""
    for y in range(height):
        for x in range(-radius, radius + 1):
            for z in range(-radius, radius + 1):
                distance = math.sqrt(x*x + z*z)
                
                if hollow:
                    if distance <= radius and distance >= radius - wall_thickness:
                        mc.setBlock(material, Vec3(center.x + x, center.y + y, center.z + z))
                else:
                    if distance <= radius:
                        mc.setBlock(material, Vec3(center.x + x, center.y + y, center.z + z))

def build_battlements(base_pos, width, length, height=3):
    """Build crenellated battlements on top of walls"""
    for x in range(width):
        for z in range(length):
            # Create merlon pattern (every other block is higher)
            if (x + z) % 4 < 2:
                mc.setBlock("stone bricks", Vec3(base_pos.x + x, base_pos.y + height, base_pos.z + z))
                mc.setBlock("stone bricks", Vec3(base_pos.x + x, base_pos.y + height + 1, base_pos.z + z))

def build_tower(base_pos, radius, height, material="stone bricks"):
    """Build a detailed tower with windows and battlements"""
    mc.postToChat(f"Building tower at {base_pos.x}, {base_pos.z}...")
    
    # Main tower structure
    build_cylinder(material, base_pos, radius, height, hollow=True, wall_thickness=2)
    
    # Tower floors
    for floor in range(0, height, 8):
        if floor > 0:
            build_cylinder("oak planks", Vec3(base_pos.x, base_pos.y + floor, base_pos.z), radius - 2, 1)
    
    # Windows on multiple levels
    directions = [(radius, 0), (-radius, 0), (0, radius), (0, -radius)]
    for level in range(8, height - 8, 8):
        for dx, dz in directions:
            # Window opening
            window_pos = Vec3(base_pos.x + dx, base_pos.y + level, base_pos.z + dz)
            mc.setBlock("air", window_pos)
            mc.setBlock("air", Vec3(window_pos.x, window_pos.y + 1, window_pos.z))
            mc.setBlock("air", Vec3(window_pos.x, window_pos.y + 2, window_pos.z))
            
            # Window frame
            mc.setBlock("dark oak planks", Vec3(window_pos.x, window_pos.y - 1, window_pos.z))
            mc.setBlock("dark oak planks", Vec3(window_pos.x, window_pos.y + 3, window_pos.z))
    
    # Battlements on top
    for angle in range(0, 360, 10):
        x = int(base_pos.x + radius * math.cos(math.radians(angle)))
        z = int(base_pos.z + radius * math.sin(math.radians(angle)))
        
        if angle % 30 < 15:  # Merlon pattern
            mc.setBlock("stone bricks", Vec3(x, base_pos.y + height, z))
            mc.setBlock("stone bricks", Vec3(x, base_pos.y + height + 1, z))
            mc.setBlock("stone bricks", Vec3(x, base_pos.y + height + 2, z))
    
    # Conical roof
    roof_height = radius // 2
    for y in range(roof_height):
        roof_radius = radius - (y * radius // roof_height)
        if roof_radius > 0:
            build_cylinder("dark oak planks", Vec3(base_pos.x, base_pos.y + height + 3 + y, base_pos.z), roof_radius, 1)
    
    # Tower interior details
    # Spiral staircase
    for y in range(0, height, 2):
        angle = (y * 30) % 360
        stair_x = int(base_pos.x + (radius - 3) * math.cos(math.radians(angle)))
        stair_z = int(base_pos.z + (radius - 3) * math.sin(math.radians(angle)))
        mc.setBlock("stone brick stairs", Vec3(stair_x, base_pos.y + y, stair_z))

def build_gatehouse(pos, width=12, depth=8, height=20):
    """Build an elaborate gatehouse with portcullis"""
    mc.postToChat("Building gatehouse...")
    
    # Main gatehouse structure
    build_hollow_box("stone bricks", pos, Vec3(pos.x + width, pos.y + height, pos.z + depth), 2)
    
    # Gate opening
    gate_width = 4
    gate_height = 6
    gate_start_x = pos.x + width // 2 - gate_width // 2
    
    for x in range(gate_width):
        for y in range(gate_height):
            mc.setBlock("air", Vec3(gate_start_x + x, pos.y + y + 1, pos.z))
            mc.setBlock("air", Vec3(gate_start_x + x, pos.y + y + 1, pos.z + depth))
    
    # Portcullis
    for x in range(gate_width):
        for y in range(0, gate_height, 2):
            mc.setBlock("iron bars", Vec3(gate_start_x + x, pos.y + y + 1, pos.z + 1))
    
    # Twin towers on gatehouse
    tower_pos1 = Vec3(pos.x - 2, pos.y, pos.z - 2)
    tower_pos2 = Vec3(pos.x + width + 2, pos.y, pos.z - 2)
    
    build_cylinder("stone bricks", tower_pos1, 4, height + 5, hollow=True, wall_thickness=2)
    build_cylinder("stone bricks", tower_pos2, 4, height + 5, hollow=True, wall_thickness=2)
    
    # Machicolations (overhanging battlements)
    for x in range(width + 8):
        for z in range(2):
            mach_pos = Vec3(pos.x - 4 + x, pos.y + height + 1, pos.z - 1 + z)
            mc.setBlock("stone bricks", mach_pos)
            # Murder holes
            if x % 3 == 0:
                mc.setBlock("air", Vec3(mach_pos.x, mach_pos.y - 1, mach_pos.z))

def build_great_hall(pos, width=30, length=50, height=15):
    """Build the great hall interior"""
    mc.postToChat("Building great hall...")
    
    # Clear interior space
    build_filled_box("air", Vec3(pos.x + 2, pos.y + 1, pos.z + 2), 
                     Vec3(pos.x + width - 2, pos.y + height - 1, pos.z + length - 2))
    
    # Floor
    for x in range(2, width - 2):
        for z in range(2, length - 2):
            if (x + z) % 2 == 0:
                mc.setBlock("polished andesite", Vec3(pos.x + x, pos.y, pos.z + z))
            else:
                mc.setBlock("stone bricks", Vec3(pos.x + x, pos.y, pos.z + z))
    
    # Pillars
    for x in range(8, width - 8, 8):
        for z in range(10, length - 10, 15):
            pillar_pos = Vec3(pos.x + x, pos.y + 1, pos.z + z)
            for y in range(height - 2):
                mc.setBlock("stone bricks", Vec3(pillar_pos.x, pillar_pos.y + y, pillar_pos.z))
                # Pillar decorations
                if y == height - 4:
                    for dx in [-1, 1]:
                        for dz in [-1, 1]:
                            mc.setBlock("chiseled stone brick", 
                                       Vec3(pillar_pos.x + dx, pillar_pos.y + y, pillar_pos.z + dz))
    
    # Throne area
    throne_pos = Vec3(pos.x + width // 2, pos.y + 1, pos.z + length - 5)
    # Throne platform
    build_filled_box("quartz block", throne_pos, Vec3(throne_pos.x + 4, throne_pos.y + 1, throne_pos.z + 3))
    
    # Throne
    mc.setBlock("quartz stairs", Vec3(throne_pos.x + 2, throne_pos.y + 2, throne_pos.z + 1))
    mc.setBlock("quartz block", Vec3(throne_pos.x + 2, throne_pos.y + 3, throne_pos.z + 1))
    mc.setBlock("quartz block", Vec3(throne_pos.x + 2, throne_pos.y + 4, throne_pos.z + 1))
    
    # Banquet tables
    for table_z in range(15, length - 15, 10):
        table_pos = Vec3(pos.x + width // 2 - 8, pos.y + 1, pos.z + table_z)
        # Table
        for x in range(16):
            mc.setBlock("oak planks", Vec3(table_pos.x + x, table_pos.y, table_pos.z))
            mc.setBlock("oak planks", Vec3(table_pos.x + x, table_pos.y, table_pos.z + 2))
        
        # Benches
        for x in range(0, 16, 2):
            mc.setBlock("oak stairs", Vec3(table_pos.x + x, table_pos.y, table_pos.z - 1))
            mc.setBlock("oak stairs", Vec3(table_pos.x + x, table_pos.y, table_pos.z + 3))
    
    # Windows with stained glass
    for z in range(10, length - 10, 8):
        # Side windows
        window_height = 6
        for y in range(window_height):
            mc.setBlock("air", Vec3(pos.x + 1, pos.y + 5 + y, pos.z + z))
            mc.setBlock("air", Vec3(pos.x + width - 1, pos.y + 5 + y, pos.z + z))
            
            # Stained glass pattern
            if y % 2 == 0:
                mc.setBlock("red stained glass", Vec3(pos.x + 1, pos.y + 5 + y, pos.z + z))
                mc.setBlock("blue stained glass", Vec3(pos.x + width - 1, pos.y + 5 + y, pos.z + z))

def build_castle_walls(base_pos, size, height=12):
    """Build the main castle walls with towers at corners"""
    mc.postToChat("Building castle walls...")
    
    # Main walls - build each wall properly from ground up
    # North wall
    build_filled_box("stone bricks", 
                     Vec3(base_pos.x, base_pos.y, base_pos.z), 
                     Vec3(base_pos.x + size, base_pos.y + height, base_pos.z + 3))
    
    # South wall  
    build_filled_box("stone bricks", 
                     Vec3(base_pos.x, base_pos.y, base_pos.z + size - 3), 
                     Vec3(base_pos.x + size, base_pos.y + height, base_pos.z + size))
    
    # West wall
    build_filled_box("stone bricks", 
                     Vec3(base_pos.x, base_pos.y, base_pos.z), 
                     Vec3(base_pos.x + 3, base_pos.y + height, base_pos.z + size))
    
    # East wall
    build_filled_box("stone bricks", 
                     Vec3(base_pos.x + size - 3, base_pos.y, base_pos.z), 
                     Vec3(base_pos.x + size, base_pos.y + height, base_pos.z + size))
    
    # Battlements on walls
    build_battlements(Vec3(base_pos.x, base_pos.y + height, base_pos.z), size, 3)  # North
    build_battlements(Vec3(base_pos.x, base_pos.y + height, base_pos.z + size - 3), size, 3)  # South
    build_battlements(Vec3(base_pos.x, base_pos.y + height, base_pos.z), 3, size)  # West  
    build_battlements(Vec3(base_pos.x + size - 3, base_pos.y + height, base_pos.z), 3, size)  # East
    
    # # Corner towers
    # corner_positions = [
    #     Vec3(base_pos.x - 5, base_pos.y, base_pos.z - 5),  # Northwest
    #     Vec3(base_pos.x + size + 5, base_pos.y, base_pos.z - 5),  # Northeast
    #     Vec3(base_pos.x - 5, base_pos.y, base_pos.z + size + 5),  # Southwest
    #     Vec3(base_pos.x + size + 5, base_pos.y, base_pos.z + size + 5)  # Southeast
    # ]
    
    # for corner_pos in corner_positions:
    #     build_tower(corner_pos, 8, height + 8)

def build_courtyard_features(base_pos, size):
    """Build features in the castle courtyard"""
    mc.postToChat("Building courtyard features...")
    
    # Well in center
    well_pos = Vec3(base_pos.x + size // 2, base_pos.y, base_pos.z + size // 2)
    build_cylinder("cobblestone", well_pos, 3, 4, hollow=True, wall_thickness=1)
    
    # Well roof
    for y in range(3):
        build_cylinder("dark oak planks", Vec3(well_pos.x, well_pos.y + 4 + y, well_pos.z), 4 - y, 1)
    
    # Well supports
    for angle in range(0, 360, 90):
        x = int(well_pos.x + 4 * math.cos(math.radians(angle)))
        z = int(well_pos.z + 4 * math.sin(math.radians(angle)))
        for y in range(6):
            mc.setBlock("dark oak fence", Vec3(x, well_pos.y + y, z))
    
    # Stables
    stable_pos = Vec3(base_pos.x + 10, base_pos.y, base_pos.z + 10)
    build_hollow_box("oak planks", stable_pos, Vec3(stable_pos.x + 20, stable_pos.y + 6, stable_pos.z + 15), 1)
    
    # Stable roof
    for x in range(22):
        for z in range(17):
            mc.setBlock("oak stairs", Vec3(stable_pos.x - 1 + x, stable_pos.y + 6, stable_pos.z - 1 + z))
    
    # Blacksmith
    smithy_pos = Vec3(base_pos.x + size - 25, base_pos.y, base_pos.z + 10)
    build_hollow_box("cobblestone", smithy_pos, Vec3(smithy_pos.x + 15, smithy_pos.y + 8, smithy_pos.z + 12), 1)
    
    # Forge
    forge_pos = Vec3(smithy_pos.x + 2, smithy_pos.y + 1, smithy_pos.z + 2)
    mc.setBlock("furnace", forge_pos)
    mc.setBlock("anvil", Vec3(forge_pos.x + 2, forge_pos.y, forge_pos.z))
    
    # Garden area
    garden_pos = Vec3(base_pos.x + size - 30, base_pos.y, base_pos.z + size - 30)
    for x in range(20):
        for z in range(20):
            if (x + z) % 3 == 0:
                mc.setBlock("grass block", Vec3(garden_pos.x + x, garden_pos.y, garden_pos.z + z))
                if (x + z) % 6 == 0:
                    mc.setBlock("red tulip", Vec3(garden_pos.x + x, garden_pos.y + 1, garden_pos.z + z))

# Main castle building sequence
mc.postToChat("Starting castle construction - this will take several minutes!")

# # 1. Level the ground and create foundation
# mc.postToChat("Preparing foundation...")
# foundation_pos = Vec3(CASTLE_BASE_X - 10, CASTLE_BASE_Y - 2, CASTLE_BASE_Z - 10)
# build_filled_box("stone", foundation_pos, Vec3(foundation_pos.x + CASTLE_SIZE + 20, CASTLE_BASE_Y, foundation_pos.z + CASTLE_SIZE + 20))

# 2. Build outer walls and corner towers
castle_base = Vec3(CASTLE_BASE_X, CASTLE_BASE_Y, CASTLE_BASE_Z)
build_castle_walls(castle_base, CASTLE_SIZE, 15)

# # 3. Build gatehouse
# gatehouse_pos = Vec3(CASTLE_BASE_X + CASTLE_SIZE // 2 - 6, CASTLE_BASE_Y, CASTLE_BASE_Z - 8)
# build_gatehouse(gatehouse_pos, 12, 8, 20)

# # 4. Build keep (central tower)
# keep_pos = Vec3(CASTLE_BASE_X + CASTLE_SIZE // 2, CASTLE_BASE_Y, CASTLE_BASE_Z + CASTLE_SIZE // 2 + 20)
# build_tower(keep_pos, 12, 35, "stone bricks")

# # 5. Build great hall
# hall_pos = Vec3(CASTLE_BASE_X + 20, CASTLE_BASE_Y, CASTLE_BASE_Z + 20)
# build_hollow_box("stone bricks", hall_pos, Vec3(hall_pos.x + 30, hall_pos.y + 18, hall_pos.z + 50), 2)
# build_great_hall(hall_pos, 30, 50, 15)

# # 6. Additional towers
# # Wizard tower
# wizard_tower_pos = Vec3(CASTLE_BASE_X + 15, CASTLE_BASE_Y, CASTLE_BASE_Z + CASTLE_SIZE - 15)
# build_tower(wizard_tower_pos, 6, 40, "purple concrete")

# # Bell tower
# bell_tower_pos = Vec3(CASTLE_BASE_X + CASTLE_SIZE - 15, CASTLE_BASE_Y, CASTLE_BASE_Z + 20)
# build_tower(bell_tower_pos, 5, 30, "stone bricks")

# # Add bell
# bell_pos = Vec3(bell_tower_pos.x, bell_tower_pos.y + 25, bell_tower_pos.z)
# mc.setBlock("iron block", bell_pos)

# # 7. Build courtyard features
# build_courtyard_features(castle_base, CASTLE_SIZE)

# # 8. Add defensive features
# # Moat
# mc.postToChat("Adding moat...")
# moat_width = 8
# for x in range(-moat_width, CASTLE_SIZE + moat_width):
#     for z in range(-moat_width, 0):
#         for y in range(CASTLE_BASE_Y - 4, CASTLE_BASE_Y):
#             mc.setBlock("water", Vec3(CASTLE_BASE_X + x, y, CASTLE_BASE_Z + z))

# # Drawbridge
# bridge_pos = Vec3(CASTLE_BASE_X + CASTLE_SIZE // 2 - 2, CASTLE_BASE_Y, CASTLE_BASE_Z - moat_width)
# for x in range(5):
#     for z in range(moat_width):
#         mc.setBlock("oak planks", Vec3(bridge_pos.x + x, bridge_pos.y, bridge_pos.z + z))

# # 9. Final details and decorations
# mc.postToChat("Adding final details...")

# # Banners on towers
# banner_positions = [
#     Vec3(CASTLE_BASE_X - 5, CASTLE_BASE_Y + 25, CASTLE_BASE_Z - 5),
#     Vec3(CASTLE_BASE_X + CASTLE_SIZE + 5, CASTLE_BASE_Y + 25, CASTLE_BASE_Z - 5),
#     Vec3(keep_pos.x, keep_pos.y + 40, keep_pos.z)
# ]

# for banner_pos in banner_positions:
#     mc.setBlock("oak fence", banner_pos)
#     mc.setBlock("red banner", Vec3(banner_pos.x, banner_pos.y + 1, banner_pos.z))

# # Torches for lighting
# torch_positions = []
# for x in range(CASTLE_BASE_X, CASTLE_BASE_X + CASTLE_SIZE, 10):
#     for z in [CASTLE_BASE_Z + 5, CASTLE_BASE_Z + CASTLE_SIZE - 5]:
#         torch_positions.append(Vec3(x, CASTLE_BASE_Y + 16, z))

# for torch_pos in torch_positions:
#     mc.setBlock("torch", torch_pos)

mc.postToChat("MAGNIFICENT CASTLE CONSTRUCTION COMPLETE!")
mc.postToChat(f"Your castle spans {CASTLE_SIZE}x{CASTLE_SIZE} blocks with:")
mc.postToChat("- 4 corner towers with spiral staircases")
mc.postToChat("- Massive gatehouse with twin towers")
mc.postToChat("- 35-block high central keep")
mc.postToChat("- Great hall with throne room")
mc.postToChat("- Wizard tower, bell tower")
mc.postToChat("- Courtyard with well, stables, smithy, garden")
mc.postToChat("- Defensive moat and drawbridge")
mc.postToChat("- Detailed battlements and machicolations")
mc.postToChat("Welcome to your new medieval fortress!")