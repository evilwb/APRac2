from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Item
from .data import Items, Locations
from .data.Items import CoordData, EquipmentData, ProgressiveUpgradeData
from . import Rac2Options

if TYPE_CHECKING:
    from . import Rac2World


def get_classification(item_name: str) -> ItemClassification:
    item = Items.from_name(item_name)
    if item in Items.COORDS:
        return ItemClassification.progression
    if item in [
        Items.HELI_PACK,
        Items.THRUSTER_PACK,
        Items.LEVITATOR,
        Items.SWINGSHOT,
        Items.GRAVITY_BOOTS,
        Items.GRIND_BOOTS,
        Items.GLIDER,
        Items.DYNAMO,
        Items.ELECTROLYZER,
        Items.THERMANATOR,
        Items.TRACTOR_BEAM,
        Items.QWARK_STATUETTE,
        Items.INFILTRATOR,
        Items.HYPNOMATIC,
        Items.SPIDERBOT_GLOVE,
        Items.HYPNOMATIC_PART,
    ]:
        return ItemClassification.progression
    if item in [
        Items.MAPPER,
        Items.ARMOR_MAGNETIZER,
        Items.BOX_BREAKER,
        Items.CHARGE_BOOTS,
        Items.PLATINUM_BOLT,
        Items.NANOTECH_BOOST,
    ]:
        return ItemClassification.useful
    if item in Items.WEAPONS or item in Items.UPGRADES:
        return ItemClassification.useful

    return ItemClassification.filler
    

def create_planets(world: "Rac2World") -> list["Item"]:
    coords_to_add: list[CoordData] = list(Items.COORDS)
    world.multiworld.random.shuffle(coords_to_add)
    precollected_ids: list[int] = [item.code for item in world.multiworld.precollected_items[world.player]]

    # determine starting coords
    # There should be at least 3 coords that lead to eligible starting planets in the player's starting inventory.
    # If the player manually added any eligible coords to their starting inventory, those will get used first.
    # If there are still less than 3, pick the rest of the starting coords randomly from the eligible coords.
    starting_coords: list[CoordData] = [coord for coord in coords_to_add if coord.item_id in precollected_ids]
    startable_coords: list[CoordData] = [coord for coord in Items.STARTABLE_COORDS if coord not in starting_coords]
    world.multiworld.random.shuffle(startable_coords)
    for coord in startable_coords[:max(3 - len(starting_coords), 0)]:
        starting_coords.append(coord)
        world.multiworld.push_precollected(world.create_item(coord.name))

    coords_to_add = [coord for coord in coords_to_add if coord not in starting_coords]

    return [world.create_item(coord.name) for coord in coords_to_add]


def create_equipment(world: "Rac2World") -> list["Item"]:
    equipment_to_add: list[EquipmentData] = list(Items.EQUIPMENT) + list(Items.WEAPONS)
    weapons: list[EquipmentData] = []
    # Starting Weapons
    if world.options.starting_weapons == world.options.starting_weapons.option_vanilla:
        equipment_to_add.remove(Items.LANCER)
        equipment_to_add.remove(Items.GRAVITY_BOMB)
    else:
        if world.options.starting_weapons == world.options.starting_weapons.option_balanced:
            weapons = [weapon for weapon in Items.WEAPONS if weapon.power <= 5]
        if world.options.starting_weapons == world.options.starting_weapons.option_non_broken:
            weapons = [weapon for weapon in Items.WEAPONS if weapon.power < 10]
        if world.options.starting_weapons == world.options.starting_weapons.option_all:
            weapons = list(Items.WEAPONS)
    
        world.multiworld.random.shuffle(weapons)
        world.push_precollected(world.create_item(weapons[0].name))
        world.push_precollected(world.create_item(weapons[1].name))
        world.starting_weapons = [weapons[0], weapons[1]]
        equipment_to_add -= world.starting_weapons

    # Gadgetron Vendor
    if not world.options.randomize_gadgetron_vendor:
        locations: list[Locations.LocationData] = [
            Locations.BARLOW_GADGETRON_1, Locations.BARLOW_GADGETRON_2, Locations.BARLOW_GADGETRON_3,
            Locations.BARLOW_GADGETRON_4, Locations.BARLOW_GADGETRON_5, Locations.BARLOW_GADGETRON_6,
        ]
        for location, weapon in zip(locations, Items.GADGETRON_VENDOR_WEAPONS):
            world.get_location(location.name).place_locked_item(world.create_item(weapon.name))
            equipment_to_add.remove(weapon)

    # Megacorp Vendor
    if not world.options.randomize_megacorp_vendor:
        locations: list[Locations.LocationData] = [
            Locations.OOZLA_NEW_WEAPON_1, Locations.OOZLA_NEW_WEAPON_2, Locations.BARLOW_NEW_WEAPON,
            Locations.ENDAKO_NEW_WEAPON_1, Locations.ENDAKO_NEW_WEAPON_2, Locations.NOTAK_NEW_WEAPON,
            Locations.TABORA_NEW_WEAPON_1, Locations.TABORA_NEW_WEAPON_2, Locations.DOBBO_NEW_WEAPON,
            Locations.JOBA_NEW_WEAPON_1, Locations.JOBA_NEW_WEAPON_2, Locations.TODANO_NEW_WEAPON,
            Locations.ARANOS_NEW_WEAPON_1, Locations.ARANOS_NEW_WEAPON_2
        ]
        for location, weapon in zip(locations, list(Items.MEGACORP_VENDOR_WEAPONS)):
            world.get_location(location.name).place_locked_item(world.create_item(weapon.name))
            if weapon in equipment_to_add:
                equipment_to_add.remove(weapon)

    precollected_ids: list[int] = [item.code for item in world.multiworld.precollected_items[world.player]]
    equipment_to_add = [equipment for equipment in equipment_to_add if equipment.item_id not in precollected_ids]

    return [world.create_item(equipment.name) for equipment in equipment_to_add]


def create_collectables(world: "Rac2World") -> list["Item"]:
    collectable_items: list["Item"] = []

    for _ in range(20):
        collectable_items.append(world.create_item(Items.PLATINUM_BOLT.name))

    precollected_nanotech_boosts: int = len([
        item for item in world.multiworld.precollected_items[world.player]
        if item.code == Items.NANOTECH_BOOST.item_id
    ])
    assert precollected_nanotech_boosts <= Items.NANOTECH_BOOST.max_capacity, "Added to many Nanotech Boosts to Start Inventory"
    for _ in range(Items.NANOTECH_BOOST.max_capacity - precollected_nanotech_boosts):
        collectable_items.append(world.create_item(Items.NANOTECH_BOOST.name))

    precollected_hypnomatic_parts: int = len([
        item for item in world.multiworld.precollected_items[world.player]
        if item.code == Items.HYPNOMATIC_PART.item_id
    ])
    assert precollected_hypnomatic_parts <= Items.HYPNOMATIC_PART.max_capacity, "Added to many Hypnomatic Parts to Start Inventory"
    for _ in range(Items.HYPNOMATIC_PART.max_capacity - precollected_hypnomatic_parts):
        collectable_items.append(world.create_item(Items.HYPNOMATIC_PART.name))

    return collectable_items


def create_upgrades(world: "Rac2World") -> list["Item"]:
    upgrades_to_add: list[ProgressiveUpgradeData] = list(Items.UPGRADES)
    # There are two wrench upgrades, add one more
    upgrades_to_add.append(Items.WRENCH_UPGRADE)

    # Remove the armor upgrade from the pool, as it currently is only for debug purpose
    # TODO: Remove this line once armor locations get implemented
    upgrades_to_add.remove(Items.ARMOR_UPGRADE)

    return [world.create_item(upgrade.name) for upgrade in upgrades_to_add]
