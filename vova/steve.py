from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.66')
mc.postToChat("I.. am Steve")

# Начальные координаты (нижний левый угол передней левой ноги)

start = Vec3(-490, 72, -185)
y = start.y

shoes = Vec3(3, 1, 7)
details = Vec3(1, 0, 7)

pants = Vec3(3, 10, 7)
body = Vec3(3, 9, 7)

hands_color = Vec3(3, 3, 3)
hands = Vec3(3, 7, 3)

head = Vec3(7, 7, 7)

hair_top = Vec3(7, 1, 7)
hair_middle = Vec3(4, 1, 7)
hair_nape = Vec3(2, 0, 7)
hair_bottom = Vec3(0, 0, 3)

hair_sides_face = Vec3(0, 0, 0)
hair_sides_top = Vec3(6, 0, 7)
hair_sides_middle = Vec3(6, 0, 7)

eye_blocks = Vec3(0, 0, 0)
nose = Vec3(0, 0, 1)
mouth = Vec3(0, 0, 3)

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

y = y + head.y - 1
start_hair_top = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("brown wool", start_hair_top, start_hair_top + hair_top)

y = y - hair_top.y
start_hair_side_face_right = Vec3(start.x + head.x - 2, y, start.z)
start_hair_side_face_left = Vec3(start.x + head.x - 2, y, start.z + head.z)

mc.setBlockCube("brown wool", start_hair_side_face_right, start_hair_side_face_right + hair_sides_face)
mc.setBlockCube("brown wool", start_hair_side_face_left, start_hair_side_face_left + hair_sides_face)

y = y - hair_sides_face.y
start_hair_sides_top = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("brown wool", start_hair_sides_top, start_hair_sides_top + hair_sides_top)

y = y - hair_sides_top.y - 1
start_hair_side_middle = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("brown wool", start_hair_side_middle, start_hair_side_middle + hair_sides_middle)

y = y - hair_sides_middle.y - hair_middle.y - 1
start_hair_middle = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("brown wool", start_hair_middle, start_hair_middle + hair_middle)

y = y - hair_middle.y
start_hair_nape = Vec3(start.x - 2, y, start.z)

mc.setBlockCube("brown wool", start_hair_nape, start_hair_nape + hair_nape)

y = y - hair_nape.y - 1
start_hair_bottom = Vec3(start.x - 2, y, start.z + 2)

mc.setBlockCube("brown wool", start_hair_bottom, start_hair_bottom + hair_bottom)

y = y + 3
start_eye_right_white = Vec3(start.x - 2 + head.x, y, start.z + 1)
start_eye_right_blue = Vec3(start.x - 2 + head.x, y, start.z + 2)
start_eye_left_white = Vec3(start.x - 2 + head.x, y, start.z + 2 + 4)
start_eye_left_blue = Vec3(start.x - 2 + head.x, y, start.z + 1 + 4)

mc.setBlockCube("white wool", start_eye_right_white, start_eye_right_white + eye_blocks)
mc.setBlockCube("blue wool", start_eye_right_blue, start_eye_right_blue + eye_blocks)
mc.setBlockCube("blue wool", start_eye_left_blue, start_eye_left_blue + eye_blocks)
mc.setBlockCube("white wool", start_eye_left_white, start_eye_left_white + eye_blocks)

y = y - 1
start_nose = Vec3(start.x - 2 + head.x, y, start.z + 3)

mc.setBlockCube("brown wool", start_nose, start_nose + nose)

y = y - 1
start_mouth = Vec3(start.x - 2 + head.x, y, start.z + 2)

mc.setBlockCube("terracotta", start_mouth, start_mouth + mouth)