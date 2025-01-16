from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from BaseClasses import Item, ItemClassification
from worlds.rac2.data.Weapons import *


class ItemData:
    name: str
    classification: ItemClassification
    max_capacity: int
    id: int
    offset: int

    def __init__(self, name: str, id: int, offset: Optional[int], progression: ItemClassification, max_capacity: int = 1) -> None:
        self.name = name
        self.id = id
        self.offset = offset
        self.classification = progression
        self.max_capacity = max_capacity


class Rac2Item(Item):
    game: str = "Ratchet & Clank 2 - Going Commando"


class ItemName(StrEnum):
    Biker_Helmet = "Biker Helmet"
    Qwark_Statuette = "Qwark Statuette"
    Glider = "Glider"
    Armor_Magnetizer = "Armor Magnetizer"
    Box_Breaker = "Box Breaker"
    Mapper = "Mapper"
    Electrolyzer = "Electrolyzer"
    Infiltrator = "Infiltrator"
    Hydro_Pack = "Hydro-Pack"
    Levitator = "Levitator"
    Swingshot = "Swingshot"
    Dynamo = "Dynamo"
    Thermanator = "Thermanator"
    Tractor_Beam = "Tractor Beam"
    Hypnomatic = "Hypnomatic"
    Heli_Pack = "Heli-Pack"
    Thruster_Pack = "Thruster-Pack"
    Grind_Boots = "Grindboots"
    Gravity_Boots = "Gravity Boots"
    Charge_Boots = "Charge Boots"
    Platinum_Bolt = "Platinum Bolt"
    Nanotech_Boost = "Nanotech Boost"
    Hypnomatic_Part = "Hypnomatic Part"

    # Planet Coords
    Oozla_Coords = "Oozla Coordinates"
    Maktar_Nebula_Coords = "Maktar Nebula Coordinates"
    Endako_Coords = "Endako Coordinates"
    Barlow_Coords = "Barlow Coordinates"
    Feltzin_System_Coords = "Feltzin System Coordinates"
    Notak_Coords = "Notak Coordinates"
    Siberius_Coords = "Siberius Coordinates"
    Tabora_Coords = "Tabora Coordinates"
    Dobbo_Coords = "Dobbo Coordinates"
    Hrugis_Cloud_Coords = "Hrugis Cloud Coordinates"
    Joba_Coords = "Joba Coordinates"
    Todano_Coords = "Todano Coordinates"
    Boldan_Coords = "Boldan Coordinates"
    Aranos_Prison_Coords = "Aranos Prison Coordinates"
    Gorn_Coords = "Gorn Coordinates"
    Snivelak_Coords = "Snivelak Coordinates"
    Smolg_Coords = "Smolg Coordinates"
    Damosel_Coords = "Damosel Coordinates"
    Grelbin_Coords = "Grelbin Coordinates"
    Yeedil_Coords = "Yeedil Coordinates"

    def __str__(self):
        return self.value


equipment_table: dict[str, ItemData] = {
    ItemName.Heli_Pack: ItemData(ItemName.Heli_Pack, 2, 2, ItemClassification.progression),
    ItemName.Thruster_Pack: ItemData(ItemName.Thruster_Pack, 3, 3, ItemClassification.progression),
    ItemName.Hydro_Pack: ItemData(ItemName.Hydro_Pack, 4, 4, ItemClassification.useful),
    ItemName.Mapper: ItemData(ItemName.Mapper, 5, 5, ItemClassification.useful),
    ItemName.Armor_Magnetizer: ItemData(ItemName.Armor_Magnetizer, 7, 7, ItemClassification.useful),
    ItemName.Levitator: ItemData(ItemName.Levitator, 8, 8, ItemClassification.progression),
    ItemName.Swingshot: ItemData(ItemName.Swingshot, 13, 13, ItemClassification.progression),
    ItemName.Gravity_Boots: ItemData(ItemName.Gravity_Boots, 19, 19, ItemClassification.progression),
    ItemName.Grind_Boots: ItemData(ItemName.Grind_Boots, 20, 20, ItemClassification.progression),
    ItemName.Glider: ItemData(ItemName.Glider, 21, 21, ItemClassification.progression),
    ItemName.Dynamo: ItemData(ItemName.Dynamo, 36, 36, ItemClassification.progression),
    ItemName.Electrolyzer: ItemData(ItemName.Electrolyzer, 38, 38, ItemClassification.progression),
    ItemName.Thermanator: ItemData(ItemName.Thermanator, 39, 39, ItemClassification.progression),
    ItemName.Tractor_Beam: ItemData(ItemName.Tractor_Beam, 46, 46, ItemClassification.progression),
    ItemName.Biker_Helmet: ItemData(ItemName.Biker_Helmet, 48, 48, ItemClassification.progression),
    ItemName.Qwark_Statuette: ItemData(ItemName.Qwark_Statuette, 49, 49, ItemClassification.progression),
    ItemName.Box_Breaker: ItemData(ItemName.Box_Breaker, 50, 50, ItemClassification.useful),
    ItemName.Infiltrator: ItemData(ItemName.Infiltrator, 51, 51, ItemClassification.progression),
    ItemName.Charge_Boots: ItemData(ItemName.Charge_Boots, 54, 54, ItemClassification.useful),
    ItemName.Hypnomatic: ItemData(ItemName.Hypnomatic, 55, 55, ItemClassification.progression),
    SHEEPINATOR.name: ItemData(SHEEPINATOR.name, 63, SHEEPINATOR.offset, ItemClassification.useful),
}

weapon_table: dict[str, ItemData] = {
    CLANK_ZAPPER.name: ItemData(CLANK_ZAPPER.name, 60, CLANK_ZAPPER.offset, ItemClassification.useful),
    BOMB_GLOVE.name: ItemData(BOMB_GLOVE.name, 61, BOMB_GLOVE.offset, ItemClassification.useful),
    VISIBOMB_GUN.name: ItemData(VISIBOMB_GUN.name, 62, VISIBOMB_GUN.name, ItemClassification.useful),
    SHEEPINATOR.name: ItemData(SHEEPINATOR.name, 63, SHEEPINATOR.offset, ItemClassification.useful),
    DECOY_GLOVE.name: ItemData(DECOY_GLOVE.name, 64, DECOY_GLOVE.offset, ItemClassification.useful),
    TESLA_CLAW.name: ItemData(TESLA_CLAW.name, 65, TESLA_CLAW.offset, ItemClassification.useful),
    CHOPPER.name: ItemData(CHOPPER.name, 66, CHOPPER.offset, ItemClassification.useful),
    PULSE_RIFLE.name: ItemData(PULSE_RIFLE.name, 67, PULSE_RIFLE.offset, ItemClassification.useful),
    SEEKER_GUN.name: ItemData(SEEKER_GUN.name, 68, SEEKER_GUN.offset, ItemClassification.useful),
    HOVERBOMB_GUN.name: ItemData(HOVERBOMB_GUN.name, 69, HOVERBOMB_GUN.offset, ItemClassification.useful),
    BLITZ_GUN.name: ItemData(BLITZ_GUN.name, 70, BLITZ_GUN.offset, ItemClassification.useful),
    MINIROCKET_TUBE.name: ItemData(MINIROCKET_TUBE.name, 71, MINIROCKET_TUBE.offset, ItemClassification.useful),
    PLASMA_COIL.name: ItemData(PLASMA_COIL.name, 72, PLASMA_COIL.offset, ItemClassification.useful),
    LAVA_GUN.name: ItemData(LAVA_GUN.name, 73, LAVA_GUN.offset, ItemClassification.useful),
    LANCER.name: ItemData(LANCER.name, 74, LANCER.offset, ItemClassification.useful),
    SYNTHENOID.name: ItemData(SYNTHENOID.name, 75, SYNTHENOID.offset, ItemClassification.useful),
    SPIDERBOT_GLOVE.name: ItemData(SPIDERBOT_GLOVE.name, 76, SPIDERBOT_GLOVE.offset, ItemClassification.progression),
    BOUNCER.name: ItemData(BOUNCER.name, 77, BOUNCER.offset, ItemClassification.useful),
    MINITURRET_GLOVE.name: ItemData(MINITURRET_GLOVE.name, 78, MINITURRET_GLOVE.offset, ItemClassification.useful),
    GRAVITY_BOMB.name: ItemData(GRAVITY_BOMB.name, 79, GRAVITY_BOMB.offset, ItemClassification.useful),
    ZODIAC.name: ItemData(ZODIAC.name, 80, ZODIAC.offset, ItemClassification.useful),
    RYNO_II.name: ItemData(RYNO_II.name, 81, RYNO_II.offset, ItemClassification.useful),
    SHIELD_CHARGER.name: ItemData(SHIELD_CHARGER.name, 82, SHIELD_CHARGER.offset, ItemClassification.useful),
    WALLOPER.name: ItemData(WALLOPER.name, 83, WALLOPER.offset, ItemClassification.useful),
}

planet_coord_table: dict[str, ItemData] = {
    ItemName.Oozla_Coords: ItemData(ItemName.Oozla_Coords, 101, 1, ItemClassification.progression),
    ItemName.Maktar_Nebula_Coords: ItemData(ItemName.Maktar_Nebula_Coords, 102, 2, ItemClassification.progression),
    ItemName.Endako_Coords: ItemData(ItemName.Endako_Coords, 103, 3, ItemClassification.progression),
    ItemName.Barlow_Coords: ItemData(ItemName.Barlow_Coords, 104, 4, ItemClassification.progression),
    ItemName.Feltzin_System_Coords: ItemData(ItemName.Feltzin_System_Coords, 105, 5, ItemClassification.progression),
    ItemName.Notak_Coords: ItemData(ItemName.Notak_Coords, 106, 6, ItemClassification.progression),
    ItemName.Siberius_Coords: ItemData(ItemName.Siberius_Coords, 107, 7, ItemClassification.progression),
    ItemName.Tabora_Coords: ItemData(ItemName.Tabora_Coords, 108, 8, ItemClassification.progression),
    ItemName.Dobbo_Coords: ItemData(ItemName.Dobbo_Coords, 109, 9, ItemClassification.progression),
    ItemName.Hrugis_Cloud_Coords: ItemData(ItemName.Hrugis_Cloud_Coords, 110, 10, ItemClassification.progression),
    ItemName.Joba_Coords: ItemData(ItemName.Joba_Coords, 111, 11, ItemClassification.progression),
    ItemName.Todano_Coords: ItemData(ItemName.Todano_Coords, 112, 12, ItemClassification.progression),
    ItemName.Boldan_Coords: ItemData(ItemName.Boldan_Coords, 113, 13, ItemClassification.progression),
    ItemName.Aranos_Prison_Coords: ItemData(ItemName.Aranos_Prison_Coords, 114, 14, ItemClassification.progression),
    ItemName.Gorn_Coords: ItemData(ItemName.Gorn_Coords, 115, 15, ItemClassification.progression),
    ItemName.Snivelak_Coords: ItemData(ItemName.Snivelak_Coords, 116, 16, ItemClassification.progression),
    ItemName.Smolg_Coords: ItemData(ItemName.Smolg_Coords, 117, 17, ItemClassification.progression),
    ItemName.Damosel_Coords: ItemData(ItemName.Damosel_Coords, 118, 18, ItemClassification.progression),
    ItemName.Grelbin_Coords: ItemData(ItemName.Grelbin_Coords, 119, 19, ItemClassification.progression),
    ItemName.Yeedil_Coords: ItemData(ItemName.Yeedil_Coords, 120, 20, ItemClassification.progression),
}

misc_table: dict[str, ItemData] = {
    ItemName.Platinum_Bolt: ItemData(ItemName.Platinum_Bolt, 80, None, ItemClassification.useful, 40),
    ItemName.Nanotech_Boost: ItemData(ItemName.Nanotech_Boost, 81, None, ItemClassification.filler, 10),
    ItemName.Hypnomatic_Part: ItemData(ItemName.Hypnomatic_Part, 82, None, ItemClassification.progression, 3),
}

item_table: dict[str, ItemData] = {
    **equipment_table,
    **planet_coord_table,
    **misc_table,
}

CLANK_PACKS: list[str] = [
    ItemName.Heli_Pack,
    ItemName.Thruster_Pack,
    ItemName.Hydro_Pack,
]
QUICK_SELECTABLE: list[str] = [
    ItemName.Swingshot,
    ItemName.Dynamo,
    ItemName.Thermanator,
    ItemName.Tractor_Beam,
    ItemName.Hypnomatic,
]
