class WeaponType:
    TYPE_SWORD = 0


weapons_data = [
    {'name': '', 'type': WeaponType.TYPE_SWORD, 'damage': 1, 'animation_code': 0}
]


class Weapon:
    def __init__(self, weapon_id):
        weapon_info = weapons_data[weapon_id]
        self.name = weapon_info['name']
        self.type = weapon_info['type']
        self.damage = weapon_info['damage']