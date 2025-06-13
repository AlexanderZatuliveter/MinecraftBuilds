from mcpq import Minecraft, Vec3
import math

mc = Minecraft('192.168.1.77')
mc.postToChat("Строю объемную радугу...")

start_x = -279
start_y = 76
start_z = -75

# Цвета радуги (снаружи внутрь)
colors = [
    "red",
    "orange",
    "yellow",
    "lime",
    "light blue",
    "blue",
    "purple"
]

radius = 50             # Радиус дуги
thickness = 5           # Толщина каждой цветной полосы (внутрь)
width = 3               # Ширина каждой полосы (вглубь - по оси Z)
segments = 150          # Кол-во сегментов дуги (чем больше — тем плавнее)

# Построение радуги
for i, color in enumerate(colors):
    inner_radius = radius - i * thickness
    for seg in range(segments):
        angle = math.pi * seg / segments  # от 0 до PI (полукруг)
        x = int(inner_radius * math.cos(angle))
        y = int(inner_radius * math.sin(angle))
        
        for dx in range(thickness):  # Толщина вверх/вниз
            for dz in range(width):  # Глубина
                pos = Vec3(
                    start_x + x,
                    start_y + y + dx,
                    start_z + dz
                )
                mc.setBlock(f"{color} concrete", pos)
