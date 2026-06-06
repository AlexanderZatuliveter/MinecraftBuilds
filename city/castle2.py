import random
from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap
from city.build_params import BuildParams


class UltimateCastle:
    """
    Великий Замок — объединение MedievalCastle и MassiveCastle.

    Архитектура:
    • Глубокий ров с водой (из MedievalCastle, расширен)
    • Скошенный фундамент из deepslate (из MedievalCastle)
    • Массивные внешние стены с аркатурой и пилястрами (из MassiveCastle)
    • Бойницы-амбразуры (из MedievalCastle)
    • 4 круглые угловые башни с конусными крышами (из MedievalCastle, улучшены)
    • 4 дополнительные промежуточные квадратные башни на серединах стен (новое)
    • Надвратная башня с подъёмным мостом и решёткой (из MedievalCastle)
    • Внутренний двор с колодцем, кузницей, кострищем (из MedievalCastle)
    • Центральный донжон (keep) с флагштоком (из MedievalCastle, увеличен)
    • Жилые этажи: тронный зал, оружейная, жилые покои (из MedievalCastle)
    • Цветные комнаты с конкретными стенами внутри (из MassiveCastle)
    • Внутренние колонны с glowstone (из MassiveCastle)
    • Зубчатые крыши с фонарями (из обоих)
    • Готические шпили на крыше (из MassiveCastle)
    • Угловые маяки с кострами (из MassiveCastle)
    • Состаренная текстура стен (псевдослучайная, из MedievalCastle)
    • Атмосферная паутина, бочки, сундуки, книжные полки

    Вдохновение: Замок Кока (Испания) + Замок Нойшванштайн (Германия)
    """

    def __init__(self, mc: Minecraft):
        self.mc = mc
        self.mcw = MinecraftWrap(mc)

        # --- Основные материалы ---
        self.stone_brick    = mc.Block("stone bricks")
        self.cracked_brick  = mc.Block("cracked stone bricks")
        self.mossy_brick    = mc.Block("mossy stone bricks")
        self.chiseled_brick = mc.Block("chiseled stone bricks")
        self.cobble         = mc.Block("cobblestone")
        self.mossy_cobble   = mc.Block("mossy cobblestone")
        self.deepslate      = mc.Block("deepslate bricks")
        self.deepslate_crk  = mc.Block("cracked deepslate bricks")
        self.polished_deep  = mc.Block("polished deepslate")
        self.stone          = mc.Block("stone")
        self.gravel         = mc.Block("gravel")
        self.air            = mc.Block("air")
        self.water          = mc.Block("water")
        self.glowstone      = mc.Block("glowstone")

        # --- Дерево и декор ---
        self.dark_oak_log   = mc.Block("dark oak log")
        self.dark_oak_plank = mc.Block("dark oak planks")
        self.oak_fence      = mc.Block("oak fence")
        self.iron_bars      = mc.Block("iron bars")
        self.glass_pane     = mc.Block("glass pane")
        self.stone_wall     = mc.Block("stone brick wall")
        self.chain          = mc.Block("chain")

        # --- Мебель и реквизит ---
        self.cauldron       = mc.Block("cauldron")
        self.chest          = mc.Block("chest")
        self.barrel         = mc.Block("barrel")
        self.anvil          = mc.Block("anvil")
        self.bookshelf      = mc.Block("bookshelf")
        self.cobweb         = mc.Block("cobweb")
        self.brewing_stand  = mc.Block("brewing stand")

        # Цвета для внутренних комнат
        self.room_colors = [
            "red", "blue", "purple", "cyan",
            "orange", "green", "gray", "brown"
        ]

    # ===========================================================
    #  ПУБЛИЧНЫЙ МЕТОД
    # ===========================================================

    def build(self, build_params: BuildParams):
        self.mc.postToChat("⚔  Возводим Великий Замок... ⚔")
        self.params = build_params
        p = build_params

        # 1. Ров
        self._moat(p)

        # 2. Фундамент
        self._foundation(p)

        # 3. Внешние стены (с аркатурой, пилястрами, бойницами)
        self._outer_walls(p)

        # 4. Четыре круглые угловые башни
        tower_r = 6
        tower_h = p.floors * p.floor_height + 12
        corners = [
            p.start + Vec3(-tower_r,     0, -tower_r),
            p.start + Vec3(p.width - 1 + tower_r, 0, -tower_r),
            p.start + Vec3(-tower_r,     0, p.depth - 1 + tower_r),
            p.start + Vec3(p.width - 1 + tower_r, 0, p.depth - 1 + tower_r),
        ]
        for c in corners:
            self._round_tower(c, tower_r, tower_h)

        # 5. Четыре промежуточные квадратные башни (середины стен)
        mid_tower_h = p.floors * p.floor_height + 6
        mid_positions = [
            p.start + Vec3(p.width // 2, 0, -4),
            p.start + Vec3(p.width // 2, 0, p.depth - 1 + 4),
            p.start + Vec3(-4,           0, p.depth // 2),
            p.start + Vec3(p.width - 1 + 4, 0, p.depth // 2),
        ]
        for mp in mid_positions:
            self._square_mural_tower(mp, 4, mid_tower_h)

        # 6. Главные ворота
        self._gatehouse(p)

        # 7. Внутренний двор
        self._courtyard(p)

        # 8. Внутренние колонны с подсветкой
        self._inner_columns(p)

        # 9. Центральный донжон
        self._keep(p)

        # 10. Жилые этажи
        for f in range(p.floors):
            self._build_floor(f, p)

        # 11. Зубчатая крыша с готическими шпилями
        self._grand_roof(p)

        # 12. Угловые маяки поверх угловых башен
        for c in corners:
            self._beacon_fire(c + Vec3(0, tower_h + 2, 0))

        self.mcw.draw()
        self.mc.postToChat("🏰  Великий Замок возведён! Слава королю! 🏰")

    # ===========================================================
    #  РОВ
    # ===========================================================

    def _moat(self, p: BuildParams):
        moat_w = 5
        x0 = p.start.x - moat_w - 6
        x1 = p.start.x + p.width + moat_w + 6
        z0 = p.start.z - moat_w - 6
        z1 = p.start.z + p.depth + moat_w + 6

        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                inner_x = p.start.x - 6 <= x <= p.start.x + p.width + 6
                inner_z = p.start.z - 6 <= z <= p.start.z + p.depth + 6
                if inner_x and inner_z:
                    continue
                for y in range(-3, 1):
                    pos = Vec3(x, p.start.y + y, z)
                    self.mcw.set_block(self.water if y < 0 else self.stone, pos)

    # ===========================================================
    #  ФУНДАМЕНТ
    # ===========================================================

    def _foundation(self, p: BuildParams):
        for bevel in range(4):
            for dx in range(-bevel, p.width + bevel):
                for dz in range(-bevel, p.depth + bevel):
                    self.mcw.set_block(
                        self.deepslate,
                        p.start + Vec3(dx, -bevel - 1, dz)
                    )

    # ===========================================================
    #  ВНЕШНИЕ СТЕНЫ (аркатура + пилястры + бойницы + стёкла)
    # ===========================================================

    def _outer_walls(self, p: BuildParams):
        wall_h = p.floors * p.floor_height

        for y in range(wall_h):
            for dx in range(p.width):
                for dz in range(p.depth):
                    is_edge = dx in (0, p.width - 1) or dz in (0, p.depth - 1)
                    if not is_edge:
                        continue

                    pos = p.start + Vec3(dx, y, dz)

                    # Пилястры каждые 4 блока на пересечениях рёбер
                    is_pillar = (dx % 4 == 0 and dz % 4 == 0)

                    # Арочный верх секций
                    is_arch_top  = (y == wall_h - 2 and (dx % 4 == 2 or dz % 4 == 2))
                    is_arch_side = (y in (wall_h - 3, wall_h - 4)
                                    and (dx % 4 in (1, 3) or dz % 4 in (1, 3)))

                    # Узкие окна-бойницы
                    is_slit = (y % p.floor_height in (2, 3)
                               and ((dx % 4 == 2 and dz in (0, p.depth - 1))
                                    or (dz % 4 == 2 and dx in (0, p.width - 1))))

                    # Широкие готические окна со стеклом в верхней трети этажа
                    is_window = (y % p.floor_height in (p.floor_height - 3, p.floor_height - 2)
                                 and dx % 8 in (3, 4) and dz in (0, p.depth - 1))
                    is_window = is_window or (
                        y % p.floor_height in (p.floor_height - 3, p.floor_height - 2)
                        and dz % 8 in (3, 4) and dx in (0, p.width - 1)
                    )

                    if is_pillar or is_arch_top or is_arch_side:
                        self.mcw.set_block(self.chiseled_brick, pos)
                    elif is_slit:
                        self.mcw.set_block(self.iron_bars, pos)
                    elif is_window:
                        self.mcw.set_block(self.glass_pane, pos)
                    else:
                        self.mcw.set_block(self._worn_stone(dx, y, dz), pos)

    def _worn_stone(self, dx, y, dz) -> Block:
        val = (dx * 7 + y * 13 + dz * 5) % 20
        if val < 9:
            return self.stone_brick
        elif val < 13:
            return self.cracked_brick
        elif val < 16:
            return self.mossy_brick
        elif val < 18:
            return self.cobble
        else:
            return self.mossy_cobble

    # ===========================================================
    #  КРУГЛАЯ УГЛОВАЯ БАШНЯ
    # ===========================================================

    def _round_tower(self, origin: Vec3, radius: int, height: int):
        for y in range(height):
            for dx in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    dist = (dx ** 2 + dz ** 2) ** 0.5
                    if dist > radius:
                        continue
                    is_shell = dist > radius - 1.8
                    pos = origin + Vec3(dx, y, dz)

                    if is_shell:
                        block = self._worn_stone(dx, y, dz)
                        self.mcw.set_block(block, pos)
                        # Бойницы
                        if y % 6 in (3, 4) and (abs(dx) % 3 == 0 or abs(dz) % 3 == 0):
                            self.mcw.set_block(self.iron_bars, pos)
                        # Окна
                        if y % 6 == 5 and dist < radius and dist > radius - 1:
                            self.mcw.set_block(self.glass_pane, pos)
                    else:
                        if y % 5 == 0:
                            self.mcw.set_block(self.dark_oak_plank, pos)
                        elif y % 5 == 4:
                            # Glowstone-освещение внутри башни
                            if abs(dx) <= 1 and abs(dz) <= 1:
                                self.mcw.set_block(self.glowstone, pos)

        # Конусная крыша
        for layer in range(radius + 3):
            r_cur = radius - layer + 1
            if r_cur < 0:
                break
            for dx in range(-r_cur, r_cur + 1):
                for dz in range(-r_cur, r_cur + 1):
                    if (dx ** 2 + dz ** 2) ** 0.5 <= r_cur:
                        self.mcw.set_block(
                            self.deepslate,
                            origin + Vec3(dx, height + layer, dz)
                        )

        # Зубцы башни
        for dx in range(-radius, radius + 1):
            for dz in [-radius, radius]:
                if (dx ** 2 + dz ** 2) ** 0.5 <= radius and dx % 2 == 0:
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height, dz))
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height + 1, dz))
        for dz in range(-radius, radius + 1):
            for dx in [-radius, radius]:
                if (dx ** 2 + dz ** 2) ** 0.5 <= radius and dz % 2 == 0:
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height, dz))
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height + 1, dz))

        # Фонарь на вершине башни
        top = origin + Vec3(0, height + radius + 3, 0)
        self.mcw.set_block(self.dark_oak_log, top)
        self.mcw.set_block(
            self.mc.Block("lantern").withData({"hanging": False}),
            top + Vec3(0, 1, 0)
        )

    # ===========================================================
    #  ПРОМЕЖУТОЧНАЯ КВАДРАТНАЯ БАШНЯ (на серединах стен)
    # ===========================================================

    def _square_mural_tower(self, origin: Vec3, half_w: int, height: int):
        w = half_w * 2 + 1
        for y in range(height):
            for dx in range(-half_w, half_w + 1):
                for dz in range(-half_w, half_w + 1):
                    is_shell = dx in (-half_w, half_w) or dz in (-half_w, half_w)
                    pos = origin + Vec3(dx, y, dz)
                    if is_shell:
                        self.mcw.set_block(self._worn_stone(dx, y, dz), pos)
                        if y % 5 in (2, 3) and (dx % 3 == 0 or dz % 3 == 0):
                            self.mcw.set_block(self.iron_bars, pos)
                    else:
                        if y % 5 == 0:
                            self.mcw.set_block(self.dark_oak_plank, pos)

        # Плоская крыша с зубцами
        for dx in range(-half_w - 1, half_w + 2):
            for dz in range(-half_w - 1, half_w + 2):
                self.mcw.set_block(self.deepslate, origin + Vec3(dx, height, dz))
        for dx in range(-half_w - 1, half_w + 2):
            if dx % 2 == 0:
                for dz in [-half_w - 1, half_w + 1]:
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height + 1, dz))
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height + 2, dz))
        for dz in range(-half_w - 1, half_w + 2):
            if dz % 2 == 0:
                for dx in [-half_w - 1, half_w + 1]:
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height + 1, dz))
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, height + 2, dz))

    # ===========================================================
    #  НАДВРАТНАЯ БАШНЯ
    # ===========================================================

    def _gatehouse(self, p: BuildParams):
        cx = p.width // 2

        # Проём ворот
        for y in range(5):
            for dx in range(-1, 2):
                pos = p.start + Vec3(cx + dx, y, 0)
                if dx in (-1, 1) and y < 4:
                    self.mcw.set_block(self.chiseled_brick, pos)
                elif y == 4:
                    self.mcw.set_block(self.deepslate, pos)
                else:
                    self.mcw.set_block(self.air, pos)

        # Решётка (portcullis)
        for y in range(1, 4):
            self.mcw.set_block(self.iron_bars, p.start + Vec3(cx - 1, y, 0))
            self.mcw.set_block(self.iron_bars, p.start + Vec3(cx + 1, y, 0))

        # Дубовые ворота
        self.mcw.set_block(
            self.mc.Block("oak door").withData({"facing": "south", "half": "lower"}),
            p.start + Vec3(cx, 1, 0)
        )
        self.mcw.set_block(
            self.mc.Block("oak door").withData({"facing": "south", "half": "upper"}),
            p.start + Vec3(cx, 2, 0)
        )

        # Факелы у ворот
        for side in (-2, 2):
            self.mcw.set_block(
                self.mc.Block("wall torch").withData({"facing": "south"}),
                p.start + Vec3(cx + side, 3, 0)
            )

        # Надвратная башня
        gate_w = 8
        gate_h = p.floors * p.floor_height + 10
        for y in range(gate_h):
            for dx in range(-gate_w // 2, gate_w // 2 + 1):
                for dz in range(-4, 1):
                    is_shell = (dx in (-gate_w // 2, gate_w // 2) or dz in (-4, 0))
                    pos = p.start + Vec3(cx + dx, y, dz)
                    if is_shell:
                        self.mcw.set_block(self._worn_stone(dx, y, dz), pos)

        # Зубцы надвратной башни
        roof_y = gate_h
        for dx in range(-gate_w // 2 - 1, gate_w // 2 + 2):
            for dz in range(-5, 1):
                self.mcw.set_block(self.deepslate, p.start + Vec3(cx + dx, roof_y, dz))
            if dx % 2 == 0:
                for dz in [-5, 0]:
                    self.mcw.set_block(self.deepslate, p.start + Vec3(cx + dx, roof_y + 1, dz))
                    self.mcw.set_block(self.deepslate, p.start + Vec3(cx + dx, roof_y + 2, dz))

        # Флаг над воротами
        flag_base = p.start + Vec3(cx, gate_h + 3, -2)
        for fy in range(4):
            self.mcw.set_block(self.dark_oak_log, flag_base + Vec3(0, fy, 0))

    # ===========================================================
    #  ВНУТРЕННИЙ ДВОР
    # ===========================================================

    def _courtyard(self, p: BuildParams):
        # Мощёный двор
        for dx in range(1, p.width - 1):
            for dz in range(1, p.depth - 1):
                val = (dx * 3 + dz * 7) % 5
                block = self.cobble if val < 3 else self.stone
                self.mcw.set_block(block, p.start + Vec3(dx, 0, dz))

        # Колодец
        well_x = p.width // 2
        well_z = p.depth // 2
        self._well(p.start + Vec3(well_x, 1, well_z))

        # Кострище
        self.mcw.set_block(
            self.mc.Block("campfire").withData({"lit": True}),
            p.start + Vec3(well_x - 4, 1, well_z)
        )

        # Кузница
        self.mcw.set_block(self.anvil, p.start + Vec3(p.width - 3, 1, 3))
        self.mcw.set_block(
            self.mc.Block("campfire").withData({"lit": True}),
            p.start + Vec3(p.width - 4, 1, 3)
        )

        # Бочки и сундуки
        for i in range(4):
            self.mcw.set_block(self.barrel, p.start + Vec3(2 + i * 2, 1, 2))
        for i in range(3):
            self.mcw.set_block(self.chest, p.start + Vec3(2, 1, p.depth - 3 - i))

    def _well(self, pos: Vec3):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                is_corner = abs(dx) == 1 and abs(dz) == 1
                if is_corner:
                    self.mcw.set_block(self.stone_brick, pos + Vec3(dx, 0, dz))
                    self.mcw.set_block(self.stone_brick, pos + Vec3(dx, 1, dz))
                    self.mcw.set_block(self.oak_fence,   pos + Vec3(dx, 2, dz))
                elif not (dx == 0 and dz == 0):
                    self.mcw.set_block(self.stone_brick, pos + Vec3(dx, 0, dz))
                else:
                    self.mcw.set_block(self.water, pos + Vec3(0, -1, 0))
        self.mcw.set_block(self.dark_oak_log, pos + Vec3(0, 2, 0))
        self.mcw.set_block(
            self.mc.Block("lantern").withData({"hanging": True}),
            pos + Vec3(0, 2, 0)
        )

    # ===========================================================
    #  ВНУТРЕННИЕ КОЛОННЫ С GLOWSTONE (из MassiveCastle)
    # ===========================================================

    def _inner_columns(self, p: BuildParams):
        spacing = max(12, p.width // 5)
        for dx in range(spacing, p.width - spacing, spacing):
            for dz in range(spacing, p.depth - spacing, spacing):
                col_height = p.floors * p.floor_height
                for y in range(1, col_height):
                    pos = p.start + Vec3(dx, y, dz)
                    if y == col_height - 1:
                        self.mcw.set_block(self.glowstone, pos)
                    else:
                        self.mcw.set_block(self.chiseled_brick, pos)

    # ===========================================================
    #  ЦЕНТРАЛЬНЫЙ ДОНЖОН (KEEP)
    # ===========================================================

    def _keep(self, p: BuildParams):
        keep_w = 11
        keep_h = p.floors * p.floor_height + 18
        kx = p.width // 2 - keep_w // 2
        kz = p.depth // 2 - keep_w // 2
        origin = p.start + Vec3(kx, 0, kz)

        for y in range(keep_h):
            for dx in range(keep_w):
                for dz in range(keep_w):
                    is_edge = dx in (0, keep_w - 1) or dz in (0, keep_w - 1)
                    is_pillar = (dx in (0, keep_w - 1) and dz in (0, keep_w - 1))
                    pos = origin + Vec3(dx, y, dz)

                    if is_edge:
                        if is_pillar:
                            self.mcw.set_block(self.chiseled_brick, pos)
                        else:
                            self.mcw.set_block(self._worn_stone(dx + kx, y, dz + kz), pos)
                        # Бойницы
                        if y % 6 in (3, 4) and dx % 4 == 2:
                            self.mcw.set_block(self.iron_bars, pos)
                        # Готические окна
                        if y % 6 == 5 and dz % 5 == 2:
                            self.mcw.set_block(self.glass_pane, pos)
                    else:
                        if y % 5 == 0:
                            self.mcw.set_block(self.dark_oak_plank, pos)
                        elif y % 5 == 4 and abs(dx - keep_w // 2) <= 1 and abs(dz - keep_w // 2) <= 1:
                            self.mcw.set_block(self.glowstone, pos)

        # Зубчатая крыша донжона
        roof_y = keep_h
        for dx in range(-1, keep_w + 1):
            for dz in range(-1, keep_w + 1):
                self.mcw.set_block(self.deepslate, origin + Vec3(dx, roof_y, dz))
        for dx in range(-1, keep_w + 1):
            if dx % 2 == 0:
                for dz in [-1, keep_w]:
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, roof_y + 1, dz))
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, roof_y + 2, dz))
        for dz in range(0, keep_w):
            if dz % 2 == 0:
                for dx in [-1, keep_w]:
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, roof_y + 1, dz))
                    self.mcw.set_block(self.deepslate, origin + Vec3(dx, roof_y + 2, dz))

        # Флагшток с тремя поленьями
        flag_y = roof_y + 3
        flag_center = origin + Vec3(keep_w // 2, 0, keep_w // 2)
        for fy in range(5):
            self.mcw.set_block(self.dark_oak_log, flag_center + Vec3(0, flag_y + fy, 0))

    # ===========================================================
    #  ЖИЛЫЕ ЭТАЖИ
    # ===========================================================

    def _build_floor(self, floor: int, p: BuildParams):
        floor_shift = Vec3(0, floor * p.floor_height, 0)
        fs = p.start + floor_shift

        # Деревянный пол
        for dx in range(1, p.width - 1):
            for dz in range(1, p.depth - 1):
                self.mcw.set_block(self.dark_oak_plank, fs + Vec3(dx, 0, dz))

        # Факелы на стенах
        for dx in range(2, p.width - 2, 4):
            self.mcw.set_block(
                self.mc.Block("wall torch").withData({"facing": "south"}),
                fs + Vec3(dx, 2, 1)
            )
            self.mcw.set_block(
                self.mc.Block("wall torch").withData({"facing": "north"}),
                fs + Vec3(dx, 2, p.depth - 2)
            )
        for dz in range(2, p.depth - 2, 4):
            self.mcw.set_block(
                self.mc.Block("wall torch").withData({"facing": "east"}),
                fs + Vec3(1, 2, dz)
            )
            self.mcw.set_block(
                self.mc.Block("wall torch").withData({"facing": "west"}),
                fs + Vec3(p.width - 2, 2, dz)
            )

        # Деревянные балки на потолке
        beam_y = p.floor_height - 1
        for dx in range(2, p.width - 2, 4):
            for dz in range(1, p.depth - 1):
                self.mcw.set_block(self.dark_oak_log, fs + Vec3(dx, beam_y, dz))

        # Цветные комнаты (из MassiveCastle)
        self._colored_rooms(fs, p)

        # Комнаты по типу
        if floor % 3 == 0:
            self._throne_room(fs, p)
        elif floor % 3 == 1:
            self._armory(fs, p)
        else:
            self._living_quarters(fs, p)

    def _colored_rooms(self, fs: Vec3, p: BuildParams):
        """Цветные комнаты внутри (из MassiveCastle)."""
        room_size = max(8, p.width // 6)
        for dx in range(1, p.width - room_size - 1, room_size):
            for dz in range(1, p.depth - room_size - 1, room_size):
                color = random.choice(self.room_colors)
                wall_block = self.mc.Block(f"{color} concrete")
                for rx in range(room_size):
                    for rz in range(room_size):
                        for ry in range(1, p.floor_height - 1):
                            is_r_edge = (rx in (0, room_size - 1) or rz in (0, room_size - 1))
                            is_door   = (is_r_edge and ry in (1, 2)
                                         and (rx == room_size // 2 or rz == room_size // 2))
                            if is_r_edge and not is_door:
                                r_pos = fs + Vec3(dx + rx, ry, dz + rz)
                                self.mcw.set_block(wall_block, r_pos)

    def _throne_room(self, fs: Vec3, p: BuildParams):
        cx = p.width // 2
        # «Трон»
        self.mcw.set_block(
            self.mc.Block("stone brick stairs").withData({"facing": "south"}),
            fs + Vec3(cx, 1, p.depth - 3)
        )
        for ddx in (-1, 0, 1):
            self.mcw.set_block(self.deepslate, fs + Vec3(cx + ddx, 1, p.depth - 2))

        # Фонари на цепях
        for ddx in (cx - 4, cx + 4):
            self.mcw.set_block(self.chain, fs + Vec3(ddx, p.floor_height - 2, p.depth // 2))
            self.mcw.set_block(
                self.mc.Block("lantern").withData({"hanging": True}),
                fs + Vec3(ddx, p.floor_height - 3, p.depth // 2)
            )

        # Книжные полки
        for dz in range(2, min(6, p.depth - 2)):
            self.mcw.set_block(self.bookshelf, fs + Vec3(2, 1, dz))
            self.mcw.set_block(self.bookshelf, fs + Vec3(3, 1, dz))

    def _armory(self, fs: Vec3, p: BuildParams):
        self.mcw.set_block(self.anvil, fs + Vec3(3, 1, 3))
        self.mcw.set_block(
            self.mc.Block("campfire").withData({"lit": True}),
            fs + Vec3(3, 1, 4)
        )
        self.mcw.set_block(self.brewing_stand, fs + Vec3(p.width - 3, 1, 3))
        for i in range(4):
            self.mcw.set_block(
                self.mc.Block("chest").withData({"facing": "south"}),
                fs + Vec3(2 + i, 1, p.depth - 3)
            )
        for i in range(4):
            self.mcw.set_block(self.barrel, fs + Vec3(p.width - 3, 1, 3 + i))
        self.mcw.set_block(self.cobweb, fs + Vec3(2, 2, 2))
        self.mcw.set_block(self.cobweb, fs + Vec3(p.width - 3, 2, p.depth - 3))

    def _living_quarters(self, fs: Vec3, p: BuildParams):
        bed_colors = ["red", "blue", "purple", "brown", "gray", "black"]
        color = random.choice(bed_colors)
        self.mc.setBed(fs + Vec3(2, 1, 2), "north", color)
        self.mc.setBed(fs + Vec3(4, 1, 2), "north", color)

        # Стол
        self.mcw.set_block(self.oak_fence, fs + Vec3(p.width - 4, 1, 3))
        self.mcw.set_block(
            self.mc.Block("dark oak slab").withData({"type": "top"}),
            fs + Vec3(p.width - 4, 2, 3)
        )
        self.mcw.set_block(
            self.mc.Block("lantern").withData({"hanging": False}),
            fs + Vec3(p.width - 4, 3, 3)
        )

        self.mcw.set_block(
            self.mc.Block("chest").withData({"facing": "east"}),
            fs + Vec3(2, 1, p.depth - 3)
        )
        self.mcw.set_block(self.cobweb, fs + Vec3(p.width - 2, 3, 2))

    # ===========================================================
    #  БОЛЬШАЯ ЗУБЧАТАЯ КРЫША С ГОТИЧЕСКИМИ ШПИЛЯМИ
    # ===========================================================

    def _grand_roof(self, p: BuildParams):
        roof_y = p.floors * p.floor_height

        # Сплошное перекрытие
        for dx in range(-1, p.width + 1):
            for dz in range(-1, p.depth + 1):
                self.mcw.set_block(self.deepslate, p.start + Vec3(dx, roof_y, dz))

        # Зубцы по периметру
        for dx in range(-1, p.width + 1):
            for dz in [-1, p.depth]:
                if dx % 2 == 0:
                    self.mcw.set_block(self.deepslate, p.start + Vec3(dx, roof_y + 1, dz))
                    self.mcw.set_block(self.deepslate, p.start + Vec3(dx, roof_y + 2, dz))
        for dz in range(0, p.depth):
            for dx in [-1, p.width]:
                if dz % 2 == 0:
                    self.mcw.set_block(self.deepslate, p.start + Vec3(dx, roof_y + 1, dz))
                    self.mcw.set_block(self.deepslate, p.start + Vec3(dx, roof_y + 2, dz))

        # Фонари на зубцах
        for dx in range(0, p.width, 8):
            for dz_off in (0, p.depth - 1):
                self.mcw.set_block(
                    self.mc.Block("lantern").withData({"hanging": False}),
                    p.start + Vec3(dx, roof_y + 1, dz_off)
                )

        # Готические малые шпили по крыше (из MassiveCastle)
        spacing = max(14, p.width // 5)
        cx = p.width // 2
        cz = p.depth // 2
        for dx in range(spacing, p.width - spacing, spacing):
            for dz in range(spacing, p.depth - spacing, spacing):
                if abs(dx - cx) > 6 or abs(dz - cz) > 6:
                    self._small_spire(p.start + Vec3(dx, roof_y, dz))

    def _small_spire(self, base: Vec3):
        for y in range(5):
            self.mcw.set_block(self.chiseled_brick, base + Vec3(0, y, 0))
        self.mcw.set_block(self.stone_wall, base + Vec3(0, 5, 0))

    # ===========================================================
    #  УГЛОВОЙ МАЯК С КОСТРОМ (из MassiveCastle)
    # ===========================================================

    def _beacon_fire(self, pos: Vec3):
        """Кострище на вершине угловой башни как маяк."""
        for y in range(3):
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    self.mcw.set_block(self.stone_brick, pos + Vec3(dx, y, dz))
        self.mcw.set_block(
            self.mc.Block("campfire").withData({"lit": True}),
            pos + Vec3(0, 3, 0)
        )
        self.mcw.set_block(self.glowstone, pos + Vec3(0, 2, 0))