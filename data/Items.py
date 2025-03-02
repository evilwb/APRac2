from dataclasses import dataclass
from abc import ABC

from typing import Callable, TYPE_CHECKING, Sequence, Optional

if TYPE_CHECKING:
    from ..Rac2Interface import Rac2Interface



@dataclass
class ItemData(ABC):
    item_id: int
    name: str


@dataclass
class EquipmentData(ItemData):
    offset: int
    icon_id: Optional[int] = None


# Gadgets/Items
HELI_PACK = EquipmentData(1, "Heli-Pack", 2, icon_id=0xEA8D)
THRUSTER_PACK = EquipmentData(2, "Thruster-Pack", 3, icon_id=0xEA7E)
MAPPER = EquipmentData(3, "Mapper", 5, icon_id=0xEA9F)
ARMOR_MAGNETIZER = EquipmentData(4, "Armor Magnetizer", 7, icon_id=0xEA9A)
LEVITATOR = EquipmentData(5, "Levitator", 8, icon_id=0xEA90)
SWINGSHOT = EquipmentData(6, "Swingshot", 13, icon_id=0xEA8B)
GRAVITY_BOOTS = EquipmentData(7, "Gravity Boots", 19, icon_id=0xEA88)
GRIND_BOOTS = EquipmentData(8, "Grindboots", 20, icon_id=0xEA8C)
GLIDER = EquipmentData(9, "Glider", 21, icon_id=0xEA91)
DYNAMO = EquipmentData(10, "Dynamo", 36, icon_id=0xEA7F)
ELECTROLYZER = EquipmentData(11, "Electrolyzer", 38, icon_id=0xEA81)
THERMANATOR = EquipmentData(12, "Thermanator", 39, icon_id=0xEA82)
TRACTOR_BEAM = EquipmentData(13, "Tractor Beam", 46, icon_id=0xEA80)
QWARK_STATUETTE = EquipmentData(14, "Qwark Statuette", 49, icon_id=0xEA9C)
BOX_BREAKER = EquipmentData(15, "Box Breaker", 50, icon_id=0xEAA1)
INFILTRATOR = EquipmentData(16, "Infiltrator", 51, icon_id=0xEA83)
CHARGE_BOOTS = EquipmentData(17, "Charge Boots", 54, icon_id=0xEA89)
HYPNOMATIC = EquipmentData(18, "Hypnomatic", 55, icon_id=0xEA84)


@dataclass
class WeaponData(EquipmentData):
    power: int = 0


# Weapons
CLANK_ZAPPER = WeaponData(101, "Clank Zapper", 9, icon_id=0xEA99, power=0,)
BOMB_GLOVE = WeaponData(102, "Bomb Glove", 12, icon_id=0xEA79, power=4)
VISIBOMB_GUN = WeaponData(103, "Visibomb Gun", 14, icon_id=0xEA7D, power=4)
SHEEPINATOR = WeaponData(104, "Sheepinator", 16, icon_id=0xEA77, power=4)
DECOY_GLOVE = WeaponData(105, "Decoy Glove", 17, icon_id=0xEA7B, power=0)
TESLA_CLAW = WeaponData(106, "Tesla Claw", 18, icon_id=0xEA7A, power=4)
CHOPPER = WeaponData(107, "Chopper", 22, icon_id=0xEA66, power=4)
PULSE_RIFLE = WeaponData(108, "Pulse Rifle", 23, icon_id=0xEA68, power=5)
SEEKER_GUN = WeaponData(109, "Seeker Gun", 24, icon_id=0xEA6B, power=5)
HOVERBOMB_GUN = WeaponData(110, "Hoverbomb Gun", 25, icon_id=0xEA72, power=9)
BLITZ_GUN = WeaponData(111, "Blitz Gun", 26, icon_id=0xEA67, power=4)
MINIROCKET_TUBE = WeaponData(112, "Minirocket Tube", 27, icon_id=0xEA70, power=7)
PLASMA_COIL = WeaponData(113, "Plasma Coil", 28, icon_id=0xEA71, power=8)
LAVA_GUN = WeaponData(114, "Lava Gun", 29, icon_id=0xEA69, power=6)
LANCER = WeaponData(115, "Lancer", 30, icon_id=0xEA64, power=3)
SYNTHENOID = WeaponData(116, "Synthenoid", 31, icon_id=0xEA6D, power=7)
SPIDERBOT_GLOVE = WeaponData(117, "Spiderbot Glove", 32, icon_id=0xEA6E, power=4)
BOUNCER = WeaponData(118, "Bouncer", 37, icon_id=0xEA73, power=8)
MINITURRET_GLOVE = WeaponData(119, "Miniturret Glove", 41, icon_id=0xEA6A, power=5)
GRAVITY_BOMB = WeaponData(120, "Gravity Bomb", 42, icon_id=0xEA65, power=3)
ZODIAC = WeaponData(121, "Zodiac", 43, icon_id=0xEA76, power=10)
RYNO_II = WeaponData(122, "RYNO II", 44, icon_id=0xEA6C, power=10)
SHIELD_CHARGER = WeaponData(123, "Shield Charger", 45, icon_id=0xEA74, power=9)
WALLOPER = WeaponData(124, "Walloper", 53, icon_id=0xEA7C, power=4)


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


@dataclass
class ProgressiveUpgradeData(ItemData):
    progressive_names: list[str]
    get_level_func: Callable[['Rac2Interface'], int]
    set_level_func: Callable[['Rac2Interface', int], bool]


WRENCH_UPGRADE = ProgressiveUpgradeData(401, "OmniWrench Upgrade", ["OmniWrench 10000", "OmniWrench 12000"],
                                        lambda interface: interface.get_wrench_level(),
                                        lambda interface, level: interface.set_wrench_level(level))

ARMOR_UPGRADE = ProgressiveUpgradeData(402, "Armor Upgrade", ["Tetrafiber Armor", "Duraplate Armor",
                                                              "Electrosteel Armor", "Carbonox Armor"],
                                       lambda interface: interface.get_armor_level(),
                                       lambda interface, level: interface.set_armor_level(level))

EQUIPMENT: Sequence[EquipmentData] = [
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
# Keep in the correct order
MEGACORP_VENDOR_WEAPONS: Sequence[EquipmentData] = [
    CHOPPER,
    BLITZ_GUN,
    PULSE_RIFLE,
    MINITURRET_GLOVE,
    SEEKER_GUN,
    SYNTHENOID,
    LAVA_GUN,
    BOUNCER,
    MINIROCKET_TUBE,
    SPIDERBOT_GLOVE,
    PLASMA_COIL,
    HOVERBOMB_GUN,
    SHIELD_CHARGER,
    ZODIAC,
    CLANK_ZAPPER,
]
# Keep in the correct order
GADGETRON_VENDOR_WEAPONS: Sequence[EquipmentData] = [
    BOMB_GLOVE,
    VISIBOMB_GUN,
    TESLA_CLAW,
    DECOY_GLOVE,
    RYNO_II,
    WALLOPER,
]
WEAPONS: Sequence[WeaponData] = [
    *MEGACORP_VENDOR_WEAPONS,
    *GADGETRON_VENDOR_WEAPONS,
    LANCER,
    GRAVITY_BOMB,
    SHEEPINATOR,
]
COORDS: Sequence[CoordData] = [
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
STARTABLE_COORDS: Sequence[CoordData] = [
    OOZLA_COORDS,
    MAKTAR_NEBULA_COORDS,
    ENDAKO_COORDS,
    FELTZIN_SYSTEM_COORDS,
    NOTAK_COORDS,
    TODANO_COORDS,
]
COLLECTABLES: Sequence[CollectableData] = [
    PLATINUM_BOLT,
    NANOTECH_BOOST,
    HYPNOMATIC_PART,
]
UPGRADES: Sequence[ProgressiveUpgradeData] = [
    WRENCH_UPGRADE,
    ARMOR_UPGRADE
]
ALL: Sequence[ItemData] = [*EQUIPMENT, *WEAPONS, *COORDS, *COLLECTABLES, *UPGRADES]
QUICK_SELECTABLE: Sequence[ItemData] = [
    *WEAPONS,
    SWINGSHOT,
    DYNAMO,
    THERMANATOR,
    TRACTOR_BEAM,
    HYPNOMATIC,
]


def from_id(item_id: int) -> ItemData:
    matching = [item for item in ALL if item.item_id == item_id]
    if len(matching) == 0:
        raise ValueError(f"No item data for item id '{item_id}'")
    assert len(matching) < 2, f"Multiple item data with id '{item_id}'. Please report."
    return matching[0]


def from_name(item_name: str) -> ItemData:
    matching = [item for item in ALL if item.name == item_name]
    if len(matching) == 0:
        raise ValueError(f"No item data for '{item_name}'")
    assert len(matching) < 2, f"Multiple item data with name '{item_name}'. Please report."
    return matching[0]


def from_offset(item_offset: int) -> EquipmentData:
    matching = [item for item in [*EQUIPMENT, *WEAPONS] if item.offset == item_offset]
    assert len(matching) > 0, f"No item data with offset '{item_offset}'."
    assert len(matching) < 2, f"Multiple item data with offset '{item_offset}'. Please report."
    return matching[0]


def coord_for_planet(number: int) -> CoordData:
    matching = [coord for coord in COORDS if coord.planet_number == number]
    assert len(matching) > 0, f"No coords for planet number '{number}'."
    assert len(matching) < 2, f"Multiple coords for planet number '{number}'. Please report."
    return matching[0]
