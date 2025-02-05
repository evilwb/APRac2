from dataclasses import dataclass
from abc import ABC


@dataclass
class ItemData(ABC):
    item_id: int
    name: str


@dataclass
class EquipmentData(ItemData):
    offset: int


# Gadgets/Items
HELI_PACK = EquipmentData(1, "Heli-Pack", 2)
THRUSTER_PACK = EquipmentData(2, "Thruster-Pack", 3)
MAPPER = EquipmentData(3, "Mapper", 5)
ARMOR_MAGNETIZER = EquipmentData(4, "Armor Magnetizer", 7)
LEVITATOR = EquipmentData(5, "Levitator", 8)
SWINGSHOT = EquipmentData(6, "Swingshot", 13)
GRAVITY_BOOTS = EquipmentData(7, "Gravity Boots", 19)
GRIND_BOOTS = EquipmentData(8, "Grindboots", 20)
GLIDER = EquipmentData(9, "Glider", 21)
DYNAMO = EquipmentData(10, "Dynamo", 36)
ELECTROLYZER = EquipmentData(11, "Electrolyzer", 38)
THERMANATOR = EquipmentData(12, "Thermanator", 39)
TRACTOR_BEAM = EquipmentData(13, "Tractor Beam", 46)
QWARK_STATUETTE = EquipmentData(14, "Qwark Statuette", 49)
BOX_BREAKER = EquipmentData(15, "Box Breaker", 50)
INFILTRATOR = EquipmentData(16, "Infiltrator", 51)
CHARGE_BOOTS = EquipmentData(17, "Charge Boots", 54)
HYPNOMATIC = EquipmentData(18, "Hypnomatic", 55)


@dataclass
class WeaponData(EquipmentData):
    pass


# Weapons
CLANK_ZAPPER = WeaponData(101, "Clank Zapper", 9)
BOMB_GLOVE = WeaponData(102, "Bomb Glove", 12)
VISIBOMB_GUN = WeaponData(103, "Visibomb Gun", 14)
SHEEPINATOR = WeaponData(104, "Sheepinator", 16)
DECOY_GLOVE = WeaponData(105, "Decoy Glove", 17)
TESLA_CLAW = WeaponData(106, "Tesla Claw", 18)
CHOPPER = WeaponData(107, "Chopper", 22)
PULSE_RIFLE = WeaponData(108, "Pulse Rifle", 23)
SEEKER_GUN = WeaponData(109, "Seeker Gun", 24)
HOVERBOMB_GUN = WeaponData(110, "Hoverbomb Gun", 25)
BLITZ_GUN = WeaponData(111, "Blitz Gun", 26)
MINIROCKET_TUBE = WeaponData(112, "Minirocket Tube", 27)
PLASMA_COIL = WeaponData(113, "Plasma Coil", 28)
LAVA_GUN = WeaponData(114, "Lava Gun", 29)
LANCER = WeaponData(115, "Lancer", 30)
SYNTHENOID = WeaponData(116, "Synthenoid", 31)
SPIDERBOT_GLOVE = WeaponData(117, "Spiderbot Glove", 32)
BOUNCER = WeaponData(118, "Bouncer", 37)
MINITURRET_GLOVE = WeaponData(119, "Miniturret Glove", 41)
GRAVITY_BOMB = WeaponData(120, "Gravity Bomb", 42)
ZODIAC = WeaponData(121, "Zodiac", 43)
RYNO_II = WeaponData(122, "RYNO II", 44)
SHIELD_CHARGER = WeaponData(123, "Shield Charger", 45)
WALLOPER = WeaponData(124, "Walloper", 53)


@dataclass
class CoordData(ItemData):
    planet_number: int


# Coordinates
OOZLA_COORDS = CoordData(201, "Oozla Coordinates", 1)
MAKTAR_NEBULA_COORDS = CoordData(202, "Maktar Nebula Coordinates", 2)
ENDAKO_COORDS = CoordData(203, "Endako Coordinates", 3)
BARLOW_COORDS = CoordData(204, "Barlow Coordinates", 4)
FELTZIN_SYSTEM_COORDS = CoordData(205, "Feltzin System Coordinates", 5)
NOTAK_COORDS = CoordData(206, "Notak Coordinates", 6)
SIBERIUS_COORDS = CoordData(207, "Siberius Coordinates", 7)
TABORA_COORDS = CoordData(208, "Tabora Coordinates", 8)
DOBBO_COORDS = CoordData(209, "Dobbo Coordinates", 9)
HRUGIS_CLOUD_COORDS = CoordData(210, "Hrugis Cloud Coordinates", 10)
JOBA_COORDS = CoordData(211, "Joba Coordinates", 11)
TODANO_COORDS = CoordData(212, "Todano Coordinates", 12)
BOLDAN_COORDS = CoordData(213, "Boldan Coordinates", 13)
ARANOS_PRISON_COORDS = CoordData(214, "Aranos Prison Coordinates", 14)
GORN_COORDS = CoordData(215, "Gorn Coordinates", 15)
SNIVELAK_COORDS = CoordData(216, "Snivelak Coordinates", 16)
SMOLG_COORDS = CoordData(217, "Smolg Coordinates", 17)
DAMOSEL_COORDS = CoordData(218, "Damosel Coordinates", 18)
GRELBIN_COORDS = CoordData(219, "Grelbin Coordinates", 19)
YEEDIL_COORDS = CoordData(220, "Yeedil Coordinates", 20)


@dataclass
class CollectableData(ItemData):
    max_capacity: int


# Collectables
PLATINUM_BOLT = CollectableData(301, "Platinum Bolt", 40)
NANOTECH_BOOST = CollectableData(302, "Nanotech Boost", 10)
HYPNOMATIC_PART = CollectableData(303, "Hypnomatic Part", 3)

EQUIPMENT: list[EquipmentData] = [
    HELI_PACK,
    THRUSTER_PACK,
    MAPPER,
    ARMOR_MAGNETIZER,
    LEVITATOR,
    SWINGSHOT,
    GRAVITY_BOOTS,
    GRIND_BOOTS,
    GLIDER,
    DYNAMO,
    ELECTROLYZER,
    THERMANATOR,
    TRACTOR_BEAM,
    QWARK_STATUETTE,
    BOX_BREAKER,
    INFILTRATOR,
    CHARGE_BOOTS,
    HYPNOMATIC,
]
WEAPONS: list[EquipmentData] = [
    CLANK_ZAPPER,
    BOMB_GLOVE,
    VISIBOMB_GUN,
    SHEEPINATOR,
    DECOY_GLOVE,
    TESLA_CLAW,
    CHOPPER,
    PULSE_RIFLE,
    SEEKER_GUN,
    HOVERBOMB_GUN,
    BLITZ_GUN,
    MINIROCKET_TUBE,
    PLASMA_COIL,
    LAVA_GUN,
    LANCER,
    SYNTHENOID,
    SPIDERBOT_GLOVE,
    BOUNCER,
    MINITURRET_GLOVE,
    GRAVITY_BOMB,
    ZODIAC,
    RYNO_II,
    SHIELD_CHARGER,
    WALLOPER
]
COORDS: list[CoordData] = [
    OOZLA_COORDS,
    MAKTAR_NEBULA_COORDS,
    ENDAKO_COORDS,
    BARLOW_COORDS,
    FELTZIN_SYSTEM_COORDS,
    NOTAK_COORDS,
    SIBERIUS_COORDS,
    TABORA_COORDS,
    DOBBO_COORDS,
    HRUGIS_CLOUD_COORDS,
    JOBA_COORDS,
    TODANO_COORDS,
    BOLDAN_COORDS,
    ARANOS_PRISON_COORDS,
    GORN_COORDS,
    SNIVELAK_COORDS,
    SMOLG_COORDS,
    DAMOSEL_COORDS,
    GRELBIN_COORDS,
    YEEDIL_COORDS,
]
STARTABLE_COORDS: list[CoordData] = [
    OOZLA_COORDS,
    MAKTAR_NEBULA_COORDS,
    ENDAKO_COORDS,
    FELTZIN_SYSTEM_COORDS,
    NOTAK_COORDS,
    TODANO_COORDS,
]
COLLECTABLES: list[CollectableData] = [
    PLATINUM_BOLT,
    NANOTECH_BOOST,
    HYPNOMATIC_PART,
]
ALL: list[ItemData] = [*EQUIPMENT, *WEAPONS, *COORDS, *COLLECTABLES]
QUICK_SELECTABLE: list[ItemData] = [
    *WEAPONS,
    SWINGSHOT,
    DYNAMO,
    THERMANATOR,
    TRACTOR_BEAM,
    HYPNOMATIC,
]


def from_id(item_id: int) -> ItemData:
    matching = [item for item in ALL if item.item_id == item_id]
    assert len(matching) > 0, f"No item data with id '{item_id}'."
    assert len(matching) < 2, f"Multiple item data with id '{item_id}'. Please report."
    return matching[0]


def from_name(item_name: str) -> ItemData:
    matching = [item for item in ALL if item.name == item_name]
    assert len(matching) > 0, f"No item data with name '{item_name}'."
    assert len(matching) < 2, f"Multiple item data with name '{item_name}'. Please report."
    return matching[0]


def coord_for_planet(number: int) -> CoordData:
    matching = [coord for coord in COORDS if coord.planet_number == number]
    assert len(matching) > 0, f"No coords for planet number '{number}'."
    assert len(matching) < 2, f"Multiple coords for planet number '{number}'. Please report."
    return matching[0]
