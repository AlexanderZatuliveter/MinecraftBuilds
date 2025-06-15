from mcpq import Minecraft, Vec3
from common.minecraft_wrap import MinecraftWrap
import random

mc = Minecraft('192.168.1.77')
mcw = MinecraftWrap(mc)

start = Vec3(-340, 63, -577)

floors = 25
floor_height = 6
width = 30
depth = 20

# Материалы
wall_blocks = ["white concrete", "light gray concrete", "gray concrete"]
glass_blocks = ["light blue stained glass", "blue stained glass", "cyan stained glass", "white stained glass"]
floor_blocks = ["polished granite", "polished diorite", "quartz block", "smooth stone"]
pillar_blocks = ["gray concrete", "black concrete", "iron block"]
roof_block = "black concrete"
antenna_blocks = ["iron bars", "lightning rod", "chain"]

# Типы интерьеров
interior_types = ["office", "apartment", "restaurant", "gym", "library", "medical", "tech", "luxury"]


def create_exterior_details(start: Vec3):
    """Создаёт внешние детали здания"""
    # Балконы на случайных этажах
    for floor_num in range(2, floors, 3):
        if random.random() < 0.7:  # 70% шанс балкона
            floor_y = floor_num * floor_height
            balcony_x = random.randint(2, width - 4)
            balcony_z = 0 if random.random() < 0.5 else depth - 1

            # Основа балкона
            for dx in range(3):
                mcw.set_block(
                    "stone slab",
                    start +
                    Vec3(
                        balcony_x +
                        dx,
                        floor_y,
                        balcony_z -
                        1 if balcony_z == 0 else balcony_z +
                        1))

            # Ограждение балкона
            for dx in range(3):
                mcw.set_block(
                    "iron bars",
                    start +
                    Vec3(
                        balcony_x +
                        dx,
                        floor_y +
                        1,
                        balcony_z -
                        1 if balcony_z == 0 else balcony_z +
                        1))


def create_advanced_roof(start: Vec3):
    """Создаёт сложную крышу с деталями"""
    roof_y = floors * floor_height

    # Основная крыша
    roof_pos1 = start + Vec3(-2, roof_y, -2)
    roof_pos2 = start + Vec3(width + 2, roof_y, depth + 2)
    mcw.set_block_cube(roof_block, roof_pos1, roof_pos2)

    # Вентиляционные шахты
    for i in range(4):
        vent_x = random.randint(3, width - 4)
        vent_z = random.randint(3, depth - 4)
        vent_pos1 = start + Vec3(vent_x, roof_y + 1, vent_z)
        vent_pos2 = start + Vec3(vent_x + 1, roof_y + 3, vent_z + 1)
        mcw.set_block_cube("stone bricks", vent_pos1, vent_pos2)
        # Вентилятор сверху
        mcw.set_block("iron trapdoor", start + Vec3(vent_x, roof_y + 4, vent_z))

    # Водонапорная башня
    tower_x = width // 2
    tower_z = depth // 2
    for y in range(8):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if abs(dx) + abs(dz) <= 1:  # Крестообразная форма
                    mcw.set_block("iron block", start + Vec3(tower_x + dx, roof_y + 1 + y, tower_z + dz))

    # Резервуар
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) <= 1 and abs(dz) <= 1:
                mcw.set_block("iron block", start + Vec3(tower_x + dx, roof_y + 9, tower_z + dz))


def create_multiple_antennas(start: Vec3):
    """Создаёт различные типы антенн"""
    roof_y = floors * floor_height

    # Главная радиоантенна
    main_x = width // 4
    main_z = depth // 4
    for y in range(12):
        antenna_block = random.choice(antenna_blocks)
        mcw.set_block(antenna_block, start + Vec3(main_x, roof_y + 1 + y, main_z))
        if y % 3 == 0:  # Поперечные элементы
            mcw.set_block("iron bars", start + Vec3(main_x - 1, roof_y + 1 + y, main_z))
            mcw.set_block("iron bars", start + Vec3(main_x + 1, roof_y + 1 + y, main_z))

    # Спутниковые антенны
    dishes = [(width * 3 // 4, depth // 4), (width // 4, depth * 3 // 4), (width * 3 // 4, depth * 3 // 4)]
    for dish_x, dish_z in dishes:
        mcw.set_block("iron block", start + Vec3(dish_x, roof_y + 1, dish_z))
        mcw.set_block("white concrete", start + Vec3(dish_x, roof_y + 2, dish_z))
        # Стойка
        for y in range(3):
            mcw.set_block("iron bars", start + Vec3(dish_x, roof_y + 3 + y, dish_z))


def create_office_interior(floor_start: Vec3):
    """Создаёт офисный интерьер"""
    # Рабочие столы
    for i in range(3):
        desk_x = 3 + i * 8
        desk_z = 3
        mcw.set_block("oak slab", floor_start + Vec3(desk_x, 1, desk_z))
        mcw.set_block("oak slab", floor_start + Vec3(desk_x + 1, 1, desk_z))
        # Стул
        mcw.set_block("oak stairs", floor_start + Vec3(desk_x, 1, desk_z + 1))

    # Конференц-зал
    conf_x, conf_z = width - 8, depth - 8
    conf_pos1 = floor_start + Vec3(conf_x, 1, conf_z)
    conf_pos2 = floor_start + Vec3(conf_x + 5, 1, conf_z + 3)
    mcw.set_block_cube("dark oak slab", conf_pos1, conf_pos2)

    # Стулья вокруг стола
    chair_positions = [(conf_x - 1, conf_z + 1), (conf_x + 6, conf_z + 1),
                       (conf_x + 2, conf_z - 1), (conf_x + 3, conf_z + 4)]
    for chair_x, chair_z in chair_positions:
        mcw.set_block("dark oak stairs", floor_start + Vec3(chair_x, 1, chair_z))


def create_apartment_interior(floor_start: Vec3):
    """Создаёт квартирный интерьер"""
    # Кухня
    kitchen_x, kitchen_z = 2, 2
    mcw.set_block("furnace", floor_start + Vec3(kitchen_x, 1, kitchen_z))
    mcw.set_block("crafting table", floor_start + Vec3(kitchen_x + 1, 1, kitchen_z))
    mcw.set_block("chest", floor_start + Vec3(kitchen_x + 2, 1, kitchen_z))
    mcw.set_block("cauldron", floor_start + Vec3(kitchen_x, 1, kitchen_z + 1))

    # Гостиная
    living_x, living_z = width // 2, depth // 2
    # Диван
    sofa_positions = [(living_x, living_z), (living_x + 1, living_z), (living_x + 2, living_z)]
    for pos_x, pos_z in sofa_positions:
        mcw.set_block("red wool", floor_start + Vec3(pos_x, 1, pos_z))

    # Телевизор
    mcw.set_block("black wool", floor_start + Vec3(living_x + 1, 2, living_z - 2))

    # Спальня
    bedroom_x, bedroom_z = width - 5, depth - 5
    # Имитация кровати (используем два блока шерсти)
    mcw.set_block("red wool", floor_start + Vec3(bedroom_x, 1, bedroom_z))
    mcw.set_block("red wool", floor_start + Vec3(bedroom_x, 1, bedroom_z + 1))
    mcw.set_block("chest", floor_start + Vec3(bedroom_x + 2, 1, bedroom_z))

    # Ванная
    bath_x, bath_z = width - 3, 2
    mcw.set_block("cauldron", floor_start + Vec3(bath_x, 1, bath_z))
    mcw.set_block("white wool", floor_start + Vec3(bath_x + 1, 1, bath_z))


def create_restaurant_interior(floor_start: Vec3):
    """Создаёт ресторанный интерьер"""
    # Столики для посетителей
    for i in range(4):
        table_x = 4 + i * 5
        table_z = 4
        mcw.set_block("spruce fence", floor_start + Vec3(table_x, 1, table_z))
        mcw.set_block("spruce pressure plate", floor_start + Vec3(table_x, 2, table_z))

        # Стулья вокруг стола
        chair_positions = [(table_x - 1, table_z), (table_x + 1, table_z),
                           (table_x, table_z - 1), (table_x, table_z + 1)]
        for chair_x, chair_z in chair_positions:
            mcw.set_block("spruce stairs", floor_start + Vec3(chair_x, 1, chair_z))

    # Кухня ресторана
    kitchen_area_x = width - 8
    kitchen_area_z = 2
    mcw.set_block("furnace", floor_start + Vec3(kitchen_area_x, 1, kitchen_area_z))
    mcw.set_block("furnace", floor_start + Vec3(kitchen_area_x + 1, 1, kitchen_area_z))
    mcw.set_block("smoker", floor_start + Vec3(kitchen_area_x + 2, 1, kitchen_area_z))
    mcw.set_block("blast furnace", floor_start + Vec3(kitchen_area_x, 1, kitchen_area_z + 1))

    # Бар
    bar_x = 2
    bar_z = depth - 3
    bar_pos1 = floor_start + Vec3(bar_x, 1, bar_z)
    bar_pos2 = floor_start + Vec3(bar_x + 7, 2, bar_z)
    mcw.set_block_cube("dark oak slab", bar_pos1, bar_pos2)

    # Барные стулья
    for dx in range(0, 8, 2):
        mcw.set_block("dark oak stairs", floor_start + Vec3(bar_x + dx, 1, bar_z + 1))


def create_gym_interior(floor_start: Vec3):
    """Создаёт интерьер спортзала"""
    # Тренажёры (имитация)
    for i in range(6):
        gym_x = 3 + i * 4
        gym_z = 3
        mcw.set_block("iron block", floor_start + Vec3(gym_x, 1, gym_z))
        mcw.set_block("iron bars", floor_start + Vec3(gym_x, 2, gym_z))
        mcw.set_block("iron bars", floor_start + Vec3(gym_x, 3, gym_z))

    # Зеркальная стена
    mirror_x = 2
    mirror_pos1 = floor_start + Vec3(mirror_x, 2, 2)
    mirror_pos2 = floor_start + Vec3(mirror_x, 3, depth - 3)
    mcw.set_block_cube("white stained glass", mirror_pos1, mirror_pos2)

    # Матрасы для упражнений
    for i in range(4):
        mat_x = width - 6
        mat_z = 3 + i * 3
        mcw.set_block("blue wool", floor_start + Vec3(mat_x, 1, mat_z))
        mcw.set_block("blue wool", floor_start + Vec3(mat_x + 1, 1, mat_z))


def create_library_interior(floor_start: Vec3):
    """Создаёт интерьер библиотеки"""
    # Книжные полки
    for shelf_row in range(3):
        shelf_x = 3 + shelf_row * 8
        for shelf_z in range(2, depth - 2, 3):
            # Полки с обеих сторон
            for side in [-1, 1]:
                shelf_pos1 = floor_start + Vec3(shelf_x + side, 1, shelf_z)
                shelf_pos2 = floor_start + Vec3(shelf_x + side, 3, shelf_z + 1)
                mcw.set_block_cube("bookshelf", shelf_pos1, shelf_pos2)

    # Читальные столы
    reading_x = width // 2
    for i in range(3):
        reading_z = 4 + i * 5
        mcw.set_block("oak slab", floor_start + Vec3(reading_x, 1, reading_z))
        mcw.set_block("oak slab", floor_start + Vec3(reading_x + 1, 1, reading_z))

        # Стулья
        mcw.set_block("oak stairs", floor_start + Vec3(reading_x, 1, reading_z - 1))
        mcw.set_block("oak stairs", floor_start + Vec3(reading_x + 1, 1, reading_z + 1))

        # Лампы
        mcw.set_block("sea lantern", floor_start + Vec3(reading_x, 4, reading_z))


def create_medical_interior(floor_start: Vec3):
    """Создаёт интерьер медицинского центра"""
    # Приёмная
    reception_x, reception_z = 3, 3
    reception_pos1 = floor_start + Vec3(reception_x, 1, reception_z)
    reception_pos2 = floor_start + Vec3(reception_x + 1, 1, reception_z)
    mcw.set_block_cube("white concrete", reception_pos1, reception_pos2)

    # Кабинеты врачей
    for i in range(4):
        office_x = 6 + i * 5
        office_z = depth - 6

        # Кушетка
        mcw.set_block("white wool", floor_start + Vec3(office_x, 1, office_z))
        mcw.set_block("white wool", floor_start + Vec3(office_x + 1, 1, office_z))

        # Медицинский стол
        mcw.set_block("white concrete", floor_start + Vec3(office_x, 1, office_z + 2))
        mcw.set_block("chest", floor_start + Vec3(office_x + 1, 1, office_z + 2))

        # Стул врача
        mcw.set_block("smooth quartz stairs", floor_start + Vec3(office_x - 1, 1, office_z + 2))

    # Лаборатория
    lab_x = width - 8
    lab_z = 3
    mcw.set_block("brewing stand", floor_start + Vec3(lab_x, 1, lab_z))
    mcw.set_block("cauldron", floor_start + Vec3(lab_x + 1, 1, lab_z))
    mcw.set_block("chest", floor_start + Vec3(lab_x + 2, 1, lab_z))


def create_tech_interior(floor_start: Vec3):
    """Создаёт интерьер технологической компании"""
    # Серверная комната
    server_x = 3
    server_z = 3
    server_pos1 = floor_start + Vec3(server_x, 1, server_z)
    server_pos2 = floor_start + Vec3(server_x + 3, 2, server_z + 2)
    mcw.set_block_cube("iron block", server_pos1, server_pos2)

    for dx in range(4):
        for dz in range(3):
            if (dx + dz) % 2 == 0:
                mcw.set_block("redstone lamp", floor_start + Vec3(server_x + dx, 3, server_z + dz))

    # Рабочие места программистов
    for i in range(6):
        dev_x = 10 + i * 3
        dev_z = 8
        mcw.set_block("quartz slab", floor_start + Vec3(dev_x, 1, dev_z))
        mcw.set_block("quartz slab", floor_start + Vec3(dev_x + 1, 1, dev_z))

        # Мониторы (имитация)
        mcw.set_block("black stained glass", floor_start + Vec3(dev_x, 2, dev_z - 1))
        mcw.set_block("black stained glass", floor_start + Vec3(dev_x + 1, 2, dev_z - 1))

        # Стул
        mcw.set_block("quartz stairs", floor_start + Vec3(dev_x, 1, dev_z + 1))

    # Переговорная с проектором
    meeting_x = width - 10
    meeting_z = depth - 8
    meeting_pos1 = floor_start + Vec3(meeting_x, 1, meeting_z)
    meeting_pos2 = floor_start + Vec3(meeting_x + 7, 1, meeting_z + 5)
    mcw.set_block_cube("white concrete", meeting_pos1, meeting_pos2)

    # "Проектор"
    mcw.set_block("observer", floor_start + Vec3(meeting_x + 4, 4, meeting_z))
    # "Экран"
    screen_pos1 = floor_start + Vec3(meeting_x + 2, 2, meeting_z + 6)
    screen_pos2 = floor_start + Vec3(meeting_x + 5, 3, meeting_z + 6)
    mcw.set_block_cube("white concrete", screen_pos1, screen_pos2)


def create_luxury_interior(floor_start: Vec3):
    """Создаёт роскошный интерьер"""
    # Мраморный пол в центре
    center_x = width // 2 - 3
    center_z = depth // 2 - 3
    center_pos1 = floor_start + Vec3(center_x, 0, center_z)
    center_pos2 = floor_start + Vec3(center_x + 5, 0, center_z + 5)
    mcw.set_block_cube("quartz block", center_pos1, center_pos2)

    # Золотые акценты
    for dx in range(6):
        mcw.set_block("gold block", floor_start + Vec3(center_x + dx, 0, center_z))
        mcw.set_block("gold block", floor_start + Vec3(center_x + dx, 0, center_z + 5))
        mcw.set_block("gold block", floor_start + Vec3(center_x, 0, center_z + dx))
        mcw.set_block("gold block", floor_start + Vec3(center_x + 5, 0, center_z + dx))

    # Люстра
    mcw.set_block("gold block", floor_start + Vec3(center_x + 3, 4, center_z + 3))
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            if abs(dx) + abs(dz) == 1:
                mcw.set_block("sea lantern", floor_start + Vec3(center_x + 3 + dx, 3, center_z + 3 + dz))

    # Роскошная мебель
    sofa_x = center_x - 3
    sofa_z = center_z + 2
    sofa_pos1 = floor_start + Vec3(sofa_x, 1, sofa_z)
    sofa_pos2 = floor_start + Vec3(sofa_x + 2, 2, sofa_z)
    mcw.set_block_cube("red wool", sofa_pos1, sofa_pos2)

    # Декоративные колонны
    for corner in [(3, 3), (width - 4, 3), (3, depth - 4), (width - 4, depth - 4)]:
        col_x, col_z = corner
        col_pos1 = floor_start + Vec3(col_x, 1, col_z)
        col_pos2 = floor_start + Vec3(col_x, 4, col_z)
        mcw.set_block_cube("quartz pillar", col_pos1, col_pos2)


def create_atrium(floor_start: Vec3):
    """Создаёт атриум в центре этажа"""
    center_x = width // 2
    center_z = depth // 2

    # Основной световой колодец
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) + abs(dz) <= 2:
                mcw.set_block("glowstone", floor_start + Vec3(center_x + dx, 0, center_z + dz))
                if abs(dx) + abs(dz) == 2:
                    mcw.set_block("sea lantern", floor_start + Vec3(center_x + dx, 1, center_z + dz))


def create_detailed_floor(start: Vec3, floor_num: int, floor_height: int):
    """Создаёт детализированный этаж с рандомным интерьером"""
    floor_shift = Vec3(0, floor_num * floor_height, 0)
    floor_start = start + floor_shift

    # Выбираем материалы для этого этажа
    current_wall = random.choice(wall_blocks)
    current_glass = random.choice(glass_blocks)
    current_floor = random.choice(floor_blocks)
    current_pillar = random.choice(pillar_blocks)

    # Строим пол
    floor_pos1 = floor_start + Vec3(0, 0, 0)
    floor_pos2 = floor_start + Vec3(width - 1, 0, depth - 1)
    mcw.set_block_cube(current_floor, floor_pos1, floor_pos2)

    # Строим стены
    for y in range(1, floor_height):
        # Боковые стены
        for dx in range(width):
            # Северная и южная стены
            for side_z in [0, depth - 1]:
                pos = floor_start + Vec3(dx, y, side_z)
                if dx in (0, width - 1):  # Углы
                    mcw.set_block(current_pillar, pos)
                elif 1 <= y <= floor_height - 2:
                    # Окна с рамами
                    if (dx + floor_num) % 3 == 0:
                        mcw.set_block(current_wall, pos)
                    else:
                        mcw.set_block(current_glass, pos)
                else:
                    mcw.set_block(current_wall, pos)

        for dz in range(1, depth - 1):
            # Западная и восточная стены
            for side_x in [0, width - 1]:
                pos = floor_start + Vec3(side_x, y, dz)
                if 1 <= y <= floor_height - 2:
                    # Окна с рамами
                    if (dz + floor_num) % 3 == 0:
                        mcw.set_block(current_wall, pos)
                    else:
                        mcw.set_block(current_glass, pos)
                else:
                    mcw.set_block(current_wall, pos)

    # Внутренние колонны
    for dx in range(8, width - 8, 8):
        for dz in range(6, depth - 6, 6):
            col_pos1 = floor_start + Vec3(dx, 1, dz)
            col_pos2 = floor_start + Vec3(dx, floor_height - 1, dz)
            mcw.set_block_cube(current_pillar, col_pos1, col_pos2)

    # Добавляем атриум
    create_atrium(floor_start)

    # Выбираем тип интерьера для этажа
    interior_type = random.choice(interior_types)

    # Создаём интерьер в зависимости от типа
    if interior_type == "office":
        create_office_interior(floor_start)
    elif interior_type == "apartment":
        create_apartment_interior(floor_start)
    elif interior_type == "restaurant":
        create_restaurant_interior(floor_start)
    elif interior_type == "gym":
        create_gym_interior(floor_start)
    elif interior_type == "library":
        create_library_interior(floor_start)
    elif interior_type == "medical":
        create_medical_interior(floor_start)
    elif interior_type == "tech":
        create_tech_interior(floor_start)
    elif interior_type == "luxury":
        create_luxury_interior(floor_start)

    # Лифтовые шахты
    elevator_positions = [(2, 2), (width - 3, 2), (2, depth - 3), (width - 3, depth - 3)]
    for elev_x, elev_z in elevator_positions:
        if floor_num == 0:  # Только на первом этаже ставим кнопки
            mcw.set_block("stone button", floor_start + Vec3(elev_x, 2, elev_z))
        mcw.set_block("iron bars", floor_start + Vec3(elev_x, 0, elev_z))


# =================== ОСНОВНАЯ ПРОГРАММА ===================

mc.postToChat("Начинаем строительство детализированного небоскреба...")

# Строим фундамент
foundation_depth = 2
foundation_pos1 = start + Vec3(-3, -foundation_depth, -3)
foundation_pos2 = start + Vec3(width + 3, 0, depth + 3)
mcw.set_block_cube("stone", foundation_pos1, foundation_pos2)

# Верхний слой фундамента из гранита
foundation_top_pos1 = start + Vec3(-3, 0, -3)
foundation_top_pos2 = start + Vec3(width + 3, 0, depth + 3)
mcw.set_block_cube("polished granite", foundation_top_pos1, foundation_top_pos2)

# Строим все этажи
for floor_num in range(floors):
    create_detailed_floor(start, floor_num, floor_height)
    if floor_num % 5 == 0:  # Сообщаем о прогрессе каждые 5 этажей
        mc.postToChat(f"Построено этажей: {floor_num + 1}/{floors}")

# Создаём внешние детали
create_exterior_details(start)

# Строим крышу
create_advanced_roof(start)

# Устанавливаем антенны
create_multiple_antennas(start)

# Добавляем внешнее освещение
for floor_num in range(0, floors, 2):
    floor_y = floor_num * floor_height + 2
    # Фонари по периметру
    light_positions = [(1, 1), (width - 2, 1), (1, depth - 2), (width - 2, depth - 2)]
    for light_x, light_z in light_positions:
        mcw.set_block("sea lantern", start + Vec3(light_x, floor_y, light_z))

# Входная группа (лобби) - создаем проемы для дверей
lobby_start = start + Vec3(width // 2 - 1, 1, 0)
for dx in range(2):
    for dy in range(2):
        mcw.set_block("air", lobby_start + Vec3(dx, dy, 0))

# Информационная стойка в лобби
reception_x = width // 2 - 2
reception_z = 3
reception_pos1 = start + Vec3(reception_x, 1, reception_z)
reception_pos2 = start + Vec3(reception_x + 3, 1, reception_z)
mcw.set_block_cube("polished granite slab", reception_pos1, reception_pos2)

# Выполняем все операции сразу
mcw.draw()

mc.postToChat(f"Строительство завершено! Небоскреб: {width}x{depth}x{floors * floor_height} блоков")
mc.postToChat(f"Всего этажей: {floors}, различных типов интерьеров: {len(interior_types)}")
