from mcpq import Minecraft, Vec3
import random

mc = Minecraft('192.168.1.77')

start = Vec3(-320, 63, -360)

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
                mc.setBlock(
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
                mc.setBlock(
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
    for dx in range(-2, width + 3):
        for dz in range(-2, depth + 3):
            mc.setBlock(roof_block, start + Vec3(dx, roof_y, dz))

    # Вентиляционные шахты
    for i in range(4):
        vent_x = random.randint(3, width - 4)
        vent_z = random.randint(3, depth - 4)
        for y in range(3):
            mc.setBlock("stone bricks", start + Vec3(vent_x, roof_y + 1 + y, vent_z))
            mc.setBlock("stone bricks", start + Vec3(vent_x + 1, roof_y + 1 + y, vent_z))
            mc.setBlock("stone bricks", start + Vec3(vent_x, roof_y + 1 + y, vent_z + 1))
            mc.setBlock("stone bricks", start + Vec3(vent_x + 1, roof_y + 1 + y, vent_z + 1))
        # Вентилятор сверху
        mc.setBlock("iron trapdoor", start + Vec3(vent_x, roof_y + 4, vent_z))

    # Водонапорная башня
    tower_x = width // 2
    tower_z = depth // 2
    for y in range(8):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if abs(dx) + abs(dz) <= 1:  # Крестообразная форма
                    mc.setBlock("iron block", start + Vec3(tower_x + dx, roof_y + 1 + y, tower_z + dz))

    # Резервуар
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) <= 1 and abs(dz) <= 1:
                mc.setBlock("iron block", start + Vec3(tower_x + dx, roof_y + 9, tower_z + dz))


def create_multiple_antennas(start: Vec3):
    """Создаёт различные типы антенн"""
    roof_y = floors * floor_height

    # Главная радиоантенна
    main_x = width // 4
    main_z = depth // 4
    for y in range(12):
        antenna_block = random.choice(antenna_blocks)
        mc.setBlock(antenna_block, start + Vec3(main_x, roof_y + 1 + y, main_z))
        if y % 3 == 0:  # Поперечные элементы
            mc.setBlock("iron bars", start + Vec3(main_x - 1, roof_y + 1 + y, main_z))
            mc.setBlock("iron bars", start + Vec3(main_x + 1, roof_y + 1 + y, main_z))

    # Спутниковые антенны
    dishes = [(width * 3 // 4, depth // 4), (width // 4, depth * 3 // 4), (width * 3 // 4, depth * 3 // 4)]
    for dish_x, dish_z in dishes:
        mc.setBlock("iron block", start + Vec3(dish_x, roof_y + 1, dish_z))
        mc.setBlock("white concrete", start + Vec3(dish_x, roof_y + 2, dish_z))
        # Стойка
        for y in range(3):
            mc.setBlock("iron bars", start + Vec3(dish_x, roof_y + 3 + y, dish_z))


def create_office_interior(floor_start: Vec3):
    """Создаёт офисный интерьер"""
    # Рабочие столы
    for i in range(3):
        desk_x = 3 + i * 8
        desk_z = 3
        mc.setBlock("oak slab", floor_start + Vec3(desk_x, 1, desk_z))
        mc.setBlock("oak slab", floor_start + Vec3(desk_x + 1, 1, desk_z))
        # Стул
        mc.setBlock("oak stairs", floor_start + Vec3(desk_x, 1, desk_z + 1))
        # Компьютер (имитация)
        # mc.setBlock("item frame", floor_start + Vec3(desk_x, 2, desk_z))

    # Конференц-зал
    conf_x, conf_z = width - 8, depth - 8
    for dx in range(6):
        for dz in range(4):
            mc.setBlock("dark oak slab", floor_start + Vec3(conf_x + dx, 1, conf_z + dz))

    # Стулья вокруг стола
    chair_positions = [(conf_x - 1, conf_z + 1), (conf_x + 6, conf_z + 1),
                       (conf_x + 2, conf_z - 1), (conf_x + 3, conf_z + 4)]
    for chair_x, chair_z in chair_positions:
        mc.setBlock("dark oak stairs", floor_start + Vec3(chair_x, 1, chair_z))


def create_apartment_interior(floor_start: Vec3):
    """Создаёт квартирный интерьер"""
    # Кухня
    kitchen_x, kitchen_z = 2, 2
    mc.setBlock("furnace", floor_start + Vec3(kitchen_x, 1, kitchen_z))
    mc.setBlock("crafting table", floor_start + Vec3(kitchen_x + 1, 1, kitchen_z))
    mc.setBlock("chest", floor_start + Vec3(kitchen_x + 2, 1, kitchen_z))
    mc.setBlock("cauldron", floor_start + Vec3(kitchen_x, 1, kitchen_z + 1))

    # Гостиная
    living_x, living_z = width // 2, depth // 2
    # Диван
    sofa_positions = [(living_x, living_z), (living_x + 1, living_z), (living_x + 2, living_z)]
    for pos_x, pos_z in sofa_positions:
        mc.setBlock("red wool", floor_start + Vec3(pos_x, 1, pos_z))

    # Телевизор
    mc.setBlock("black wool", floor_start + Vec3(living_x + 1, 2, living_z - 2))
    # mc.setBlock("item frame", floor_start + Vec3(living_x + 1, 3, living_z - 2))

    # Спальня
    bedroom_x, bedroom_z = width - 5, depth - 5
    mc.setBed(floor_start + Vec3(bedroom_x, 1, bedroom_z), "north")
    mc.setBlock("chest", floor_start + Vec3(bedroom_x + 2, 1, bedroom_z))

    # Ванная
    bath_x, bath_z = width - 3, 2
    mc.setBlock("cauldron", floor_start + Vec3(bath_x, 1, bath_z))
    mc.setBlock("white wool", floor_start + Vec3(bath_x + 1, 1, bath_z))


def create_restaurant_interior(floor_start: Vec3):
    """Создаёт ресторанный интерьер"""
    # Столики для посетителей
    for i in range(4):
        table_x = 4 + i * 5
        table_z = 4
        mc.setBlock("spruce fence", floor_start + Vec3(table_x, 1, table_z))
        mc.setBlock("spruce pressure plate", floor_start + Vec3(table_x, 2, table_z))

        # Стулья вокруг стола
        chair_positions = [(table_x - 1, table_z), (table_x + 1, table_z),
                           (table_x, table_z - 1), (table_x, table_z + 1)]
        for chair_x, chair_z in chair_positions:
            mc.setBlock("spruce stairs", floor_start + Vec3(chair_x, 1, chair_z))

    # Кухня ресторана
    kitchen_area_x = width - 8
    kitchen_area_z = 2
    mc.setBlock("furnace", floor_start + Vec3(kitchen_area_x, 1, kitchen_area_z))
    mc.setBlock("furnace", floor_start + Vec3(kitchen_area_x + 1, 1, kitchen_area_z))
    mc.setBlock("smoker", floor_start + Vec3(kitchen_area_x + 2, 1, kitchen_area_z))
    mc.setBlock("blast furnace", floor_start + Vec3(kitchen_area_x, 1, kitchen_area_z + 1))

    # Бар
    bar_x = 2
    bar_z = depth - 3
    for dx in range(8):
        mc.setBlock("dark oak slab", floor_start + Vec3(bar_x + dx, 1, bar_z))
        mc.setBlock("dark oak slab", floor_start + Vec3(bar_x + dx, 2, bar_z))

    # Барные стулья
    for dx in range(0, 8, 2):
        mc.setBlock("dark oak stairs", floor_start + Vec3(bar_x + dx, 1, bar_z + 1))


def create_gym_interior(floor_start: Vec3):
    """Создаёт интерьер спортзала"""
    # Тренажёры (имитация)
    for i in range(6):
        gym_x = 3 + i * 4
        gym_z = 3
        mc.setBlock("iron block", floor_start + Vec3(gym_x, 1, gym_z))
        mc.setBlock("iron bars", floor_start + Vec3(gym_x, 2, gym_z))
        mc.setBlock("iron bars", floor_start + Vec3(gym_x, 3, gym_z))

    # Зеркальная стена
    mirror_x = 2
    for dz in range(2, depth - 2):
        mc.setBlock("white stained glass", floor_start + Vec3(mirror_x, 2, dz))
        mc.setBlock("white stained glass", floor_start + Vec3(mirror_x, 3, dz))

    # Матрасы для упражнений
    for i in range(4):
        mat_x = width - 6
        mat_z = 3 + i * 3
        mc.setBlock("blue wool", floor_start + Vec3(mat_x, 1, mat_z))
        mc.setBlock("blue wool", floor_start + Vec3(mat_x + 1, 1, mat_z))


def create_library_interior(floor_start: Vec3):
    """Создаёт интерьер библиотеки"""
    # Книжные полки
    for shelf_row in range(3):
        shelf_x = 3 + shelf_row * 8
        for shelf_z in range(2, depth - 2, 3):
            # Полки с обеих сторон
            for side in [-1, 1]:
                for y in range(3):
                    mc.setBlock("bookshelf", floor_start + Vec3(shelf_x + side, 1 + y, shelf_z))
                    mc.setBlock("bookshelf", floor_start + Vec3(shelf_x + side, 1 + y, shelf_z + 1))

    # Читальные столы
    reading_x = width // 2
    for i in range(3):
        reading_z = 4 + i * 5
        mc.setBlock("oak slab", floor_start + Vec3(reading_x, 1, reading_z))
        mc.setBlock("oak slab", floor_start + Vec3(reading_x + 1, 1, reading_z))

        # Стулья
        mc.setBlock("oak stairs", floor_start + Vec3(reading_x, 1, reading_z - 1))
        mc.setBlock("oak stairs", floor_start + Vec3(reading_x + 1, 1, reading_z + 1))

        # Лампы
        mc.setBlock("sea lantern", floor_start + Vec3(reading_x, 4, reading_z))


def create_medical_interior(floor_start: Vec3):
    """Создаёт интерьер медицинского центра"""
    # Приёмная
    reception_x, reception_z = 3, 3
    mc.setBlock("white concrete", floor_start + Vec3(reception_x, 1, reception_z))
    mc.setBlock("white concrete", floor_start + Vec3(reception_x + 1, 1, reception_z))
    # mc.setBlock("item frame", floor_start + Vec3(reception_x, 2, reception_z))

    # Кабинеты врачей
    for i in range(4):
        office_x = 6 + i * 5
        office_z = depth - 6

        # Кушетка
        mc.setBlock("white wool", floor_start + Vec3(office_x, 1, office_z))
        mc.setBlock("white wool", floor_start + Vec3(office_x + 1, 1, office_z))

        # Медицинский стол
        mc.setBlock("white concrete", floor_start + Vec3(office_x, 1, office_z + 2))
        mc.setBlock("chest", floor_start + Vec3(office_x + 1, 1, office_z + 2))

        # Стул врача
        mc.setBlock("smooth quartz stairs", floor_start + Vec3(office_x - 1, 1, office_z + 2))

    # Лаборатория
    lab_x = width - 8
    lab_z = 3
    mc.setBlock("brewing stand", floor_start + Vec3(lab_x, 1, lab_z))
    mc.setBlock("cauldron", floor_start + Vec3(lab_x + 1, 1, lab_z))
    mc.setBlock("chest", floor_start + Vec3(lab_x + 2, 1, lab_z))


def create_tech_interior(floor_start: Vec3):
    """Создаёт интерьер технологической компании"""
    # Серверная комната
    server_x = 3
    server_z = 3
    for dx in range(4):
        for dz in range(3):
            mc.setBlock("iron block", floor_start + Vec3(server_x + dx, 1, server_z + dz))
            mc.setBlock("iron block", floor_start + Vec3(server_x + dx, 2, server_z + dz))
            if (dx + dz) % 2 == 0:
                mc.setBlock("redstone lamp", floor_start + Vec3(server_x + dx, 3, server_z + dz))

    # Рабочие места программистов
    for i in range(6):
        dev_x = 10 + i * 3
        dev_z = 8
        mc.setBlock("quartz slab", floor_start + Vec3(dev_x, 1, dev_z))
        mc.setBlock("quartz slab", floor_start + Vec3(dev_x + 1, 1, dev_z))

        # Мониторы (имитация)
        mc.setBlock("black stained glass", floor_start + Vec3(dev_x, 2, dev_z - 1))
        mc.setBlock("black stained glass", floor_start + Vec3(dev_x + 1, 2, dev_z - 1))

        # Стул
        mc.setBlock("quartz stairs", floor_start + Vec3(dev_x, 1, dev_z + 1))

    # Переговорная с проектором
    meeting_x = width - 10
    meeting_z = depth - 8
    for dx in range(8):
        for dz in range(6):
            mc.setBlock("white concrete", floor_start + Vec3(meeting_x + dx, 1, meeting_z + dz))

    # "Проектор"
    mc.setBlock("observer", floor_start + Vec3(meeting_x + 4, 4, meeting_z))
    # "Экран"
    for dx in range(4):
        for dy in range(2):
            mc.setBlock("white concrete", floor_start + Vec3(meeting_x + dx + 2, 2 + dy, meeting_z + 6))


def create_luxury_interior(floor_start: Vec3):
    """Создаёт роскошный интерьер"""
    # Мраморный пол в центре
    center_x = width // 2 - 3
    center_z = depth // 2 - 3
    for dx in range(6):
        for dz in range(6):
            mc.setBlock("quartz block", floor_start + Vec3(center_x + dx, 0, center_z + dz))

    # Золотые акценты
    for dx in range(6):
        mc.setBlock("gold block", floor_start + Vec3(center_x + dx, 0, center_z))
        mc.setBlock("gold block", floor_start + Vec3(center_x + dx, 0, center_z + 5))
        mc.setBlock("gold block", floor_start + Vec3(center_x, 0, center_z + dx))
        mc.setBlock("gold block", floor_start + Vec3(center_x + 5, 0, center_z + dx))

    # Люстра
    mc.setBlock("gold block", floor_start + Vec3(center_x + 3, 4, center_z + 3))
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            if abs(dx) + abs(dz) == 1:
                mc.setBlock("sea lantern", floor_start + Vec3(center_x + 3 + dx, 3, center_z + 3 + dz))

    # Роскошная мебель
    sofa_x = center_x - 3
    sofa_z = center_z + 2
    for dx in range(3):
        mc.setBlock("red wool", floor_start + Vec3(sofa_x + dx, 1, sofa_z))
        mc.setBlock("red wool", floor_start + Vec3(sofa_x + dx, 2, sofa_z))

    # Декоративные колонны
    for corner in [(3, 3), (width - 4, 3), (3, depth - 4), (width - 4, depth - 4)]:
        col_x, col_z = corner
        for y in range(1, 5):
            mc.setBlock("quartz pillar", floor_start + Vec3(col_x, y, col_z))


def create_atrium(floor_start: Vec3):
    """Создаёт атриум в центре этажа"""
    center_x = width // 2
    center_z = depth // 2

    # Основной световой колодец
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) + abs(dz) <= 2:
                mc.setBlock("glowstone", floor_start + Vec3(center_x + dx, 0, center_z + dz))
                if abs(dx) + abs(dz) == 2:
                    mc.setBlock("sea lantern", floor_start + Vec3(center_x + dx, 1, center_z + dz))


def create_detailed_floor(start: Vec3, floor_num: int, floor_height: int):
    """Создаёт детализированный этаж с рандомным интерьером"""
    floor_shift = Vec3(0, floor_num * floor_height, 0)
    floor_start = start + floor_shift

    # Выбираем материалы для этого этажа
    current_wall = random.choice(wall_blocks)
    current_glass = random.choice(glass_blocks)
    current_floor = random.choice(floor_blocks)
    current_pillar = random.choice(pillar_blocks)

    # Строим структуру этажа
    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                pos = floor_start + Vec3(dx, y, dz)

                # Определяем тип блока
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                is_corner = (dx in (0, width - 1)) and (dz in (0, depth - 1))
                is_pillar = (dx % 8 == 0 and dz % 6 == 0) and not is_edge

                if is_edge:
                    if is_corner:
                        mc.setBlock(current_pillar, pos)
                    elif 1 <= y <= floor_height - 2:
                        # Окна с рамами
                        if (dx + dz + floor_num) % 3 == 0:
                            mc.setBlock(current_wall, pos)
                        else:
                            mc.setBlock(current_glass, pos)
                    else:
                        mc.setBlock(current_wall, pos)
                elif is_pillar and y > 0:
                    mc.setBlock(current_pillar, pos)
                elif y == 0:
                    mc.setBlock(current_floor, pos)
                # Остальное пространство остаётся воздухом

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
            mc.setBlock("stone button", floor_start + Vec3(elev_x, 2, elev_z))
        mc.setBlock("iron bars", floor_start + Vec3(elev_x, 0, elev_z))
        for y in range(1, floor_height):
            mc.setBlock("air", floor_start + Vec3(elev_x, y, elev_z))

# =================== ОСНОВНАЯ ПРОГРАММА ===================


mc.postToChat("Начинаем строительство детализированного небоскреба...")

# Очистка области (опционально)
# for dx in range(-5, width + 6):
#     for dz in range(-5, depth + 6):
#         for dy in range(floors * floor_height + 20):
#             mc.setBlock("air", start + Vec3(dx, dy, dz))

# Строим фундамент
foundation_depth = 2
for dx in range(-3, width + 4):
    for dz in range(-3, depth + 4):
        for dy in range(-foundation_depth, 1):
            if dy == 0:
                mc.setBlock("polished granite", start + Vec3(dx, dy, dz))
            else:
                mc.setBlock("stone", start + Vec3(dx, dy, dz))

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
        mc.setBlock("sea lantern", start + Vec3(light_x, floor_y, light_z))

# Входная группа (лобби)
lobby_start = start + Vec3(0, 0, 0)
# Двойные двери
mc.setBlock("air", lobby_start + Vec3(width // 2 - 1, 1, 0))
mc.setBlock("air", lobby_start + Vec3(width // 2, 1, 0))
mc.setBlock("air", lobby_start + Vec3(width // 2 - 1, 2, 0))
mc.setBlock("air", lobby_start + Vec3(width // 2, 2, 0))

# Информационная стойка в лобби
reception_x = width // 2 - 2
reception_z = 3
mc.setBlock("polished granite slab", lobby_start + Vec3(reception_x, 1, reception_z))
mc.setBlock("polished granite slab", lobby_start + Vec3(reception_x + 1, 1, reception_z))
mc.setBlock("polished granite slab", lobby_start + Vec3(reception_x + 2, 1, reception_z))
mc.setBlock("polished granite slab", lobby_start + Vec3(reception_x + 3, 1, reception_z))

mc.postToChat(f"Строительство завершено! Небоскреб: {width}x{depth}x{floors * floor_height} блоков")
mc.postToChat(f"Всего этажей: {floors}, различных типов интерьеров: {len(interior_types)}")
