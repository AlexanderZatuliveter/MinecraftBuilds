from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')
mc.postToChat("I.. am Steve")

# Начальные координаты (нижний левый угол передней левой ноги)

start = Vec3(-1062, 70, -140)
y = start.y

shoes = Vec3(3, 1, 7)
details = Vec3(1, 0, 7)

pants = Vec3(3, 10, 7)
body = Vec3(3, 9, 7)

hands_color = Vec3(3, 3, 3)
hands = Vec3(3, 7, 3)

head = Vec3(7, 7, 7)

hair_top = Vec3(7, 1, 7)

mc.setBlockCube("gray concrete", start, start + shoes)

y = y + shoes.y + 1
start_details_shoes = Vec3(start.x, y, start.z)
start_details_pants = Vec3(start.x + 2, y, start.z)

mc.setBlockCube("gray concrete", start_details_shoes, start_details_shoes + details)
mc.setBlockCube("blue wool", start_details_pants, start_details_pants + details)

y = y + details.y + 1
start_pants = Vec3(start.x, y, start.z)

mc.setBlockCube("blue wool", start_pants, start_pants + pants)

y = y + pants.y + 1
start_body = Vec3(start.x, y, start.z)

mc.setBlockCube("light blue wool", start_body, start_body + body)

y = y + body.y - hands_color.y
start_hand_color_right = Vec3(start.x, y, start.z - hands_color.z - 1)
start_hand_color_left = Vec3(start.x, y, start.z + body.z + 1)

mc.setBlockCube("light blue wool", start_hand_color_right, start_hand_color_right + hands_color)
mc.setBlockCube("light blue wool", start_hand_color_left, start_hand_color_left + hands_color)

y = y - hands.y - 1
start_hand_right = Vec3(start.x, y, start.z - hands.z - 1)
start_hand_left = Vec3(start.x, y, start.z + body.z + 1)

mc.setBlockCube("stripped jungle wood", start_hand_right, start_hand_right + hands)
mc.setBlockCube("stripped jungle wood", start_hand_left, start_hand_left + hands)

y = y + hands.y + hands_color.y + 2
start_head = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("stripped jungle wood", start_head, start_head + head)

y = y + head.y
start_hair_top = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("brown wool", start_hair_top, start_hair_top + hair_top)