from typing import Dict, TYPE_CHECKING

from worlds.rac2 import every_location, LocationName, ItemName, item_table
from worlds.rac2.Rac2Interface import PLANET_LIST_SIZE, INVENTORY_SIZE, NANOTECH_BOOST_MAX
from worlds.rac2.data.Planets import Planet
from .data import Weapons

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context

PLANET_UNLOCK_TO_LOCATION_ID: Dict[int, int] = {
    Planet.Maktar_Nebula.number: every_location[LocationName.Oozla_End_Store_Cutscene].id,
    Planet.Endako.number: every_location[LocationName.Maktar_Photo_Booth].id,
    Planet.Barlow.number: every_location[LocationName.Maktar_Deactivate_Jamming_Array].id,
    Planet.Feltzin_System.number: every_location[LocationName.Barlow_Hoverbike_Race_Transmission].id,
    Planet.Notak.number: every_location[LocationName.Feltzin_Defeat_Thug_Ships].id,
    Planet.Siberius.number: every_location[LocationName.Notak_Worker_Bots].id,
    Planet.Tabora.number: every_location[LocationName.Siberius_Defeat_Thief].id,
    Planet.Dobbo.number: every_location[LocationName.Tabora_Meet_Angela].id,
    Planet.Hrugis_Cloud.number: every_location[LocationName.Dobbo_Facility_Terminal].id,
    Planet.Joba.number: every_location[LocationName.Dobbo_Defeat_Thug_Leader].id,
    Planet.Todano.number: every_location[LocationName.Hrugis_Destroy_Defenses].id,
    Planet.Boldan.number: every_location[LocationName.Todano_Search_Rocket_Silo].id,
    Planet.Aranos_Prison.number: every_location[LocationName.Boldan_Find_Fizzwidget].id,
    Planet.Gorn.number: every_location[LocationName.Aranos_Control_Room].id,
    Planet.Snivelak.number: every_location[LocationName.Gorn_Defeat_Thug_Fleet].id,
    Planet.Smolg.number: every_location[LocationName.Snivelak_Rescue_Angela].id,
    Planet.Damosel.number: every_location[LocationName.Smolg_Mutant_Crab].id,
    Planet.Grelbin.number: every_location[LocationName.Smolg_Balloon_Transmission].id,
    Planet.Yeedil.number: every_location[LocationName.Grelbin_Find_Angela].id,
    Planet.Ship_Shack.number: every_location[LocationName.Notak_Top_Pier_Telescreen].id
}

INVENTORY_OFFSET_TO_LOCATION_ID: Dict[int, int] = {
    item_table[ItemName.Heli_Pack].offset: every_location[LocationName.Endako_Rescue_Clank_Heli].id,
    item_table[ItemName.Thruster_Pack].offset: every_location[LocationName.Endako_Rescue_Clank_Thruster].id,
    item_table[ItemName.Mapper].offset: every_location[LocationName.Damosel_Defeat_Mothership].id,
    item_table[ItemName.Armor_Magnetizer].offset: every_location[LocationName.Todano_Stuart_Zurgo_Trade].id,
    item_table[ItemName.Levitator].offset: every_location[LocationName.Joba_Shady_Salesman].id,
    item_table[ItemName.Swingshot].offset: every_location[LocationName.Endako_Clank_Apartment_SS].id,
    item_table[ItemName.Gravity_Boots].offset: every_location[LocationName.Joba_Arena_Battle].id,
    item_table[ItemName.Grind_Boots].offset: every_location[LocationName.Endako_Clank_Apartment_GB].id,
    item_table[ItemName.Glider].offset: every_location[LocationName.Tabora_Underground_Mines_End].id,
    item_table[ItemName.Dynamo].offset: every_location[LocationName.Oozla_Outside_Megacorp_Store].id,
    item_table[ItemName.Electrolyzer].offset: every_location[LocationName.Maktar_Arena_Challenge].id,
    item_table[ItemName.Thermanator].offset: every_location[LocationName.Barlow_Inventor].id,
    item_table[ItemName.Tractor_Beam].offset: every_location[LocationName.Oozla_Megacorp_Scientist].id,
    item_table[ItemName.Qwark_Statuette].offset: every_location[LocationName.Aranos_Plumber].id,
    item_table[ItemName.Box_Breaker].offset: every_location[LocationName.Oozla_Swamp_MonsterII].id,
    item_table[ItemName.Infiltrator].offset: every_location[LocationName.Joba_Arena_Cage_Match].id,
    item_table[ItemName.Charge_Boots].offset: every_location[LocationName.Joba_First_Hoverbike_Race].id,
    item_table[ItemName.Hypnomatic].offset: every_location[LocationName.Damosel_Hypnotist].id,
    item_table[Weapons.SHEEPINATOR.name].offset: every_location[LocationName.Todano_Facility_Interior].id
}

PLAT_BOLT_OFFSET_TO_LOCATION_ID: Dict[int, int] = {
    Planet.Oozla.number * 4 + 1: every_location[LocationName.Oozla_Swamp_Ruins_PB].id,
    Planet.Oozla.number * 4 + 2: every_location[LocationName.Oozla_Tractor_Puzzle_PB].id,
    Planet.Maktar_Nebula.number * 4 + 1: every_location[LocationName.Maktar_Crane_PB].id,
    Planet.Jamming_Array.number * 4 + 1: every_location[LocationName.Maktar_Jamming_Array_PB].id,
    Planet.Endako.number * 4 + 1: every_location[LocationName.Endako_Crane_PB].id,
    Planet.Endako.number * 4 + 3: every_location[LocationName.Endako_Ledge_PB].id,
    Planet.Barlow.number * 4: every_location[LocationName.Barlow_Hound_Cave_PB].id,
    Planet.Barlow.number * 4 + 1: every_location[LocationName.Barlow_Hoverbike_Race_PB].id,
    Planet.Feltzin_System.number * 4: every_location[LocationName.Feltzin_Race_PB].id,
    Planet.Notak.number * 4: every_location[LocationName.Notak_Timed_Dynamo_PB].id,
    Planet.Notak.number * 4 + 1: every_location[LocationName.Notak_Promenade_Sign_PB].id,
    Planet.Notak.number * 4 + 2: every_location[LocationName.Notak_Behind_Building_PB].id,
    Planet.Siberius.number * 4: every_location[LocationName.Siberius_Flamebot_Ledge_PB].id,
    Planet.Siberius.number * 4 + 1: every_location[LocationName.Siberius_Fenced_Area_PB].id,
    Planet.Tabora.number * 4: every_location[LocationName.Tabora_Canyon_Glide_PB].id,
    Planet.Tabora.number * 4 + 1: every_location[LocationName.Tabora_Northeast_Desert_PB].id,
    Planet.Tabora.number * 4 + 2: every_location[LocationName.Tabora_Underground_Mines_PB].id,
    Planet.Dobbo.number * 4 + 1: every_location[LocationName.Dobbo_Spiderbot_Room_PB].id,
    Planet.Dobbo.number * 4 + 3: every_location[LocationName.Dobbo_Facility_Glide_PB].id,
    Planet.Hrugis_Cloud.number * 4: every_location[LocationName.Hrugis_Race_PB].id,
    Planet.Joba.number * 4: every_location[LocationName.Joba_Hidden_Cliff_PB].id,
    Planet.Joba.number * 4 + 1: every_location[LocationName.Joba_Levitator_Tower_PB].id,
    Planet.Todano.number * 4: every_location[LocationName.Todano_Spiderbot_Conveyor_PB].id,
    Planet.Todano.number * 4 + 1: every_location[LocationName.Todano_End_Tour_PB].id,
    Planet.Todano.number * 4 + 2: every_location[LocationName.Todano_Near_Stuart_Zurgo_PB].id,
    Planet.Boldan.number * 4: every_location[LocationName.Boldan_Floating_Platform_PB].id,
    Planet.Boldan.number * 4 + 1: every_location[LocationName.Boldan_Spiderbot_Alley_PB].id,
    Planet.Boldan.number * 4 + 3: every_location[LocationName.Boldan_Upper_Dome_PB].id,
    Planet.Aranos_Prison.number * 4: every_location[LocationName.Aranos_Under_Ship_PB].id,
    Planet.Gorn.number * 4: every_location[LocationName.Gorn_Race_PB].id,
    Planet.Snivelak.number * 4: every_location[LocationName.Snivelak_Dynamo_Platforms_PB].id,
    Planet.Smolg.number * 4 + 1: every_location[LocationName.Smolg_Warehouse_PB].id,
    Planet.Smolg.number * 4 + 2: every_location[LocationName.Smolg_Floating_Platform_PB].id,
    Planet.Damosel.number * 4: every_location[LocationName.Damosel_Frozen_Fountain_PB].id,
    Planet.Damosel.number * 4 + 1: every_location[LocationName.Damosel_Pyramid_PB].id,
    Planet.Grelbin.number * 4 + 1: every_location[LocationName.Grelbin_Underwater_Tunnel_PB].id,
    Planet.Grelbin.number * 4 + 2: every_location[LocationName.Grelbin_Yeti_Cave_PB].id,
    Planet.Grelbin.number * 4 + 3: every_location[LocationName.Grelbin_Ice_Plains_PB].id,
    Planet.Yeedil.number * 4 + 1: every_location[LocationName.Yeedil_Tractor_Pillar_PB].id,
    Planet.Yeedil.number * 4 + 2: every_location[LocationName.Yeedil_Bridge_Grindrail_PB].id,
}

NANOTECH_OFFSET_TO_LOCATION_ID: Dict[int, int] = {
    0: every_location[LocationName.Notak_Promenade_End_NT].id,
    1: every_location[LocationName.Endako_Crane_NT].id,
    2: every_location[LocationName.Tabora_Canyon_Glide_Pillar_NT].id,
    3: every_location[LocationName.Joba_Timed_Dynamo_NT].id,
    4: every_location[LocationName.Joba_Hoverbike_Race_Shortcut_NT].id,
    5: every_location[LocationName.Snivelak_Swingshot_Tower_NT].id,
    6: every_location[LocationName.Feltzin_Cargo_Bay_NT].id,
    7: every_location[LocationName.Todano_Rocket_Silo_NT].id,
    8: every_location[LocationName.Boldan_Fountain_NT].id,
    9: every_location[LocationName.Dobbo_Facility_Glide_NT].id,
}


async def handle_checked_location(ctx: 'Rac2Context'):
    cleared_locations = set()
    if ctx.current_planet == -1:
        return

    # check planet unlocks table to see which coordinate locations have been checked.
    planet_table_start = ctx.game_interface.addresses.unlocked_planets
    for i, address in enumerate(range(planet_table_start, planet_table_start + PLANET_LIST_SIZE)):
        if i in PLANET_UNLOCK_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(PLANET_UNLOCK_TO_LOCATION_ID[i])

    # check secondary inventory table to see which equipment locations have been checked.
    inventory_start = ctx.game_interface.addresses.secondary_inventory
    for i, address in enumerate(range(inventory_start, inventory_start + INVENTORY_SIZE)):
        if i in INVENTORY_OFFSET_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(INVENTORY_OFFSET_TO_LOCATION_ID[i])

    # check platinum bolts table to see which platinum bolts locations have been checked.
    plat_bolt_table_start = ctx.game_interface.addresses.platinum_bolt_table
    for i, address in enumerate(range(plat_bolt_table_start, plat_bolt_table_start + 0x70)):
        if i in PLAT_BOLT_OFFSET_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(PLAT_BOLT_OFFSET_TO_LOCATION_ID[i])

    # check nanotech boosts table to see which boost locations have been checked.
    nanotech_table_start = ctx.game_interface.addresses.nanotech_boost_table
    for i, address in enumerate(range(nanotech_table_start, nanotech_table_start + NANOTECH_BOOST_MAX)):
        if i in NANOTECH_OFFSET_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(NANOTECH_OFFSET_TO_LOCATION_ID[i])

    # check for hypnomatic parts
    if ctx.game_interface.pcsx2_interface.read_int8(ctx.game_interface.addresses.hypnomatic_part1) == 1:
        cleared_locations.add(every_location[LocationName.Smolg_Distribution_Facility_End].id)
    if ctx.game_interface.pcsx2_interface.read_int8(ctx.game_interface.addresses.hypnomatic_part2) == 1:
        cleared_locations.add(every_location[LocationName.Damosel_Train_Rails].id)
    if ctx.game_interface.pcsx2_interface.read_int8(ctx.game_interface.addresses.hypnomatic_part3) == 1:
        cleared_locations.add(every_location[LocationName.Grelbin_Mystic_More_Moonstones].id)

    cleared_locations = cleared_locations.difference(ctx.checked_locations)
    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared_locations}])
    for location_number in cleared_locations:
        location_name = [location.name for location in every_location.values() if location.id == location_number].pop()
        ctx.game_interface.logger.info(f"Location checked: {location_name}")
