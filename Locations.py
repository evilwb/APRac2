from enum import StrEnum
from typing import Optional, Callable

from BaseClasses import Location, CollectionState
from worlds.rac2.Logic import can_dynamo, can_tractor, can_gravity, can_electrolyze, can_infiltrate, can_swingshot, \
    can_pack, can_therminate, can_glide, can_levitate, has_qwark_statuette, can_grind, can_hypnotize, \
    has_hypnomatic_parts


class Rac2Location(Location):
    game: str = "Ratchet & Clank 2"


class LocationData:
    name: str
    id: int
    access_rule: Optional[Callable[[CollectionState, int], bool]]

    def __init__(self, name, id, access_rule=lambda state, player: True):
        self.name = name
        self.id = id
        self.access_rule = access_rule


class LocationName(StrEnum):
    Oozla_Outside_Megacorp_Store = "Oozla: Outside Megacorp Store - Dynamo"
    Oozla_End_Store_Cutscene = "Oozla: End of Store Cutscene"
    Oozla_Megacorp_Scientist = "Oozla: Megacorp Scientist - Tractor Beam"
    Oozla_Tractor_Puzzle_PB = "Oozla: Tractor Puzzle - Platinum Bolt"
    Oozla_Swamp_Ruins_PB = "Oozla: Swamp Ruins - Platinum Bolt"
    Oozla_Swamp_MonsterII = "Oozla: Swamp Monster II - Box Breaker"
    Maktar_Arena_Challenge = "Maktar: Arena Challenge - Electrolyzer"
    Maktar_Photo_Booth = "Maktar: Photo Booth"
    Maktar_Deactivate_Jamming_Array = "Maktar: Deactivate Jamming Array"
    Maktar_Jamming_Array_PB = "Maktar: Jamming Array - Platinum Bolt"
    Maktar_Crane_PB = "Maktar: Crane - Platinum Bolt"
    Endako_Clank_Apartment_SS = "Endako: Clank's Apartment - Swingshot"
    Endako_Clank_Apartment_GB = "Endako: Clank's Apartment - Grindboots"
    Endako_Rescue_Clank_Heli = "Endako: Rescue Clank Heli-Pack"
    Endako_Rescue_Clank_Thruster = "Endako: Rescue Clank Thruster-Pack"
    Endako_Rescue_Clank_Hydro = "Endako: Rescue Clank Hydro-Pack"
    Endako_Ledge_PB = "Endako: Ledge - Platinum Bolt"
    Endako_Crane_PB = "Endako: Crane - Platinum Bolt"
    Endako_Crane_NT = "Endako: Crane - Nanotech Boost"
    Barlow_Inventor = "Barlow: Inventor - Thermanator"
    Barlow_Hoverbike_Race_Transmission = "Barlow: Hoverbike Race Transmission"
    Barlow_Hoverbike_Race_Helmet = "Barlow: Hoverbike Race - Biker Helmet"
    Barlow_Hoverbike_Race_PB = "Barlow: Hoverbike Race - Platinum Bolt"
    Barlow_Hound_Cave_PB = "Barlow: Hound Cave - Platinum Bolt"
    Feltzin_Defeat_Thug_Ships = "Feltzin: Defeat Thug Ships"
    Feltzin_Race_PB = "Feltzin: Race - Platinum Bolt"
    Feltzin_Cargo_Bay_NT = "Feltzin: Cargo Bay - Nanotech Boost"
    Notak_Top_Pier_Telescreen = "Notak: Top of Pier Telescreen"
    Notak_Worker_Bots = "Notak: Worker Bots"
    Notak_Behind_Building_PB = "Notak: Behind Building - Platinum Bolt"
    Notak_Promenade_Sign_PB = "Notak: Promenade Sign - Platinum Bolt"
    Notak_Timed_Dynamo_PB = "Notak: Timed Dynamo - Platinum Bolt"
    Notak_Promenade_End_NT = "Notak: Promenade End - Nanotech Boost"
    Siberius_Defeat_Thief = "Siberius: Defeat Thief"
    Siberius_Flamebot_Ledge_PB = "Siberius: Flamebot Ledge - Platinum Bolt"
    Siberius_Fenced_Area_PB = "Siberius: Fenced Area - Platinum Bolt"
    Tabora_OmniWrench_10000 = "Tabora: OmniWrench 10000"
    Tabora_Meet_Angela = "Tabora: Meet Angela"
    Tabora_Underground_Mines_End = "Tabora: Underground Mines - Glider"
    Tabora_Underground_Mines_PB = "Tabora: Underground Mines - Platinum Bolt"
    Tabora_Canyon_Glide_PB = "Tabora: Canyon Glide - Platinum Bolt"
    Tabora_Northeast_Desert_PB = "Tabora: Northeast Desert - Platinum Bolt"
    Tabora_Canyon_Glide_Pillar_NT = "Tabora: Canyon Glide Pillar - Nanotech Boost"
    Dobbo_Defeat_Thug_Leader = "Dobbo: Defeat Thug Leader"
    Dobbo_Facility_Terminal = "Dobbo: Facility Terminal"
    Dobbo_Spiderbot_Room_PB = "Dobbo: Spiderbot Room - Platinum Bolt"
    Dobbo_Facility_Glide_PB = "Dobbo: Facility Glide End - Platinum Bolt"
    Dobbo_Facility_Glide_NT = "Dobbo: Facility Glide Beginning - Nanotech Boost"
    Hrugis_Destroy_Defenses = "Hrugis Cloud: Destroy Defenses"
    Hrugis_Race_PB = "Hrugis Cloud: Race - Platinum Bolt"
    Joba_First_Hoverbike_Race = "Joba: First Hoverbike Race - Charge Boots"
    Joba_Shady_Salesman = "Joba: Shady Salesman - Levitator"
    Joba_Arena_Battle = "Joba: Arena Battle - Gravity Boots"
    Joba_Arena_Cage_Match = "Joba: Arena Cage Match - Infiltrator"
    Joba_Hidden_Cliff_PB = "Joba: Hidden Cliff - Platinum Bolt"
    Joba_Levitator_Tower_PB = "Joba: Levitator Tower - Platinum Bolt"
    Joba_Hoverbike_Race_Shortcut_NT = "Joba: Hoverbike Race Shortcut - Nanotech Boost"
    Joba_Timed_Dynamo_NT = "Joba: Timed Dynamo Course - Nanotech Boost"
    Todano_Search_Rocket_Silo = "Todano: Search Rocket Silo"
    Todano_Stuart_Zurgo_Trade = "Todano: Stuart Zurgo Trade - Armor Magnetizer"
    Todano_Near_Stuart_Zurgo_PB = "Todano: Near Stuart Zurgo - Platinum Bolt"
    Todano_End_Tour_PB = "Todano: End of Tour - Platinum Bolt"
    Todano_Spiderbot_Conveyor_PB = "Todano: Spiderbot Conveyor - Platinum Bolt"
    Todano_Rocket_Silo_NT = "Todano: Rocket Silo - Nanotech Boost"
    Boldan_Find_Fizzwidget = "Boldan: Find Fizzwidget"
    Boldan_Spiderbot_Alley_PB = "Boldan: Spiderbot Alley - Platinum Bolt"
    Boldan_Floating_Platform_PB = "Boldan: Floating Platform - Platinum Bolt"
    Boldan_Upper_Dome_PB = "Boldan: Upper Dome - Platinum Bolt"
    Boldan_Fountain_NT = "Boldan: Fountain - Nanotech Boost"
    Aranos_Control_Room = "Aranos: Control Room"
    Aranos_Plumber = "Aranos: Plumber - Qwark Statuette"
    Aranos_Under_Ship_PB = "Aranos: Under Ship - Platinum Bolt"
    Gorn_Defeat_Thug_Fleet = "Gorn: Defeat Thug Fleet"
    Gorn_Race_PB = "Gorn: Race - Platinum Bolt"
    Snivelak_Rescue_Angela = "Snivelak: Rescue Angela"
    Snivelak_Dynamo_Platforms_PB = "Snivelak: Dynamo Platforms - Platinum Bolt"
    Snivelak_Swingshot_Tower_NT = "Snivelak: Swingshot Tower - Nanotech Boost"
    Smolg_Balloon_Transmission = "Smolg: Balloon Transmission"
    Smolg_Distribution_Facility_End = "Smolg: Distribution Facility End - Hypnomatic Part"
    Smolg_Mutant_Crab = "Smolg: Mutant Crab"
    Smolg_Floating_Platform_PB = "Smolg: Floating Platform - Platinum Bolt"
    Smolg_Warehouse_PB = "Smolg: Warehouse - Platinum Bolt"
    Damosel_Hypnotist = "Damosel: Hypnotist"
    Damosel_Train_Rails = "Damosel: Train Rails - Hypnomatic Part"
    Damosel_Defeat_Mothership = "Damosel: Defeat Mothership - Mapper"
    Damosel_Frozen_Fountain_PB = "Damosel: Frozen Fountain - Platinum Bolt"
    Damosel_Pyramid_PB = "Damosel: Pyramid - Platinum Bolt"
    Grelbin_Find_Angela = "Grelbin: Find Angela"
    Grelbin_Mystic_More_Moonstones = "Grelbin: Mystic More Moonstones - Hypnomatic Part"
    Grelbin_Ice_Plains_PB = "Grelbin: Ice Plains - Platinum Bolt"
    Grelbin_Underwater_Tunnel_PB = "Grelbin: Underwater Tunnel - Platinum Bolt"
    Grelbin_Yeti_Cave_PB = "Grelbin: Yeti Cave - Platinum Bolt"
    Yeedil_Defeat_Mutated_Protopet = "Yeedil: Defeat Mutated Protopet"
    Yeedil_Bridge_Grindrail_PB = "Yeedil: Bridge Grindrail - Platinum Bolt"
    Yeedil_Tractor_Pillar_PB = "Yeedil: Tractor Pillar - Platinum Bolt"


oozla_location_table = {
    LocationName.Oozla_Outside_Megacorp_Store: LocationData(LocationName.Oozla_Outside_Megacorp_Store, 10),
    LocationName.Oozla_End_Store_Cutscene: LocationData(LocationName.Oozla_End_Store_Cutscene, 11, can_dynamo),
    LocationName.Oozla_Megacorp_Scientist: LocationData(LocationName.Oozla_Megacorp_Scientist, 12),
    LocationName.Oozla_Tractor_Puzzle_PB: LocationData(LocationName.Oozla_Tractor_Puzzle_PB, 13, can_tractor),
    LocationName.Oozla_Swamp_Ruins_PB: LocationData(LocationName.Oozla_Swamp_Ruins_PB, 14, can_dynamo),
    LocationName.Oozla_Swamp_MonsterII: LocationData(
        LocationName.Oozla_Swamp_MonsterII, 15,
        lambda state, player: can_dynamo(state, player) and can_gravity(state, player)
    ),
}

maktar_location_table = {
    LocationName.Maktar_Arena_Challenge: LocationData(LocationName.Maktar_Arena_Challenge, 20),
    LocationName.Maktar_Photo_Booth: LocationData(LocationName.Maktar_Photo_Booth, 21, can_electrolyze),
    LocationName.Maktar_Deactivate_Jamming_Array: LocationData(LocationName.Maktar_Deactivate_Jamming_Array, 22,
                                                               can_tractor),
    LocationName.Maktar_Jamming_Array_PB: LocationData(LocationName.Maktar_Jamming_Array_PB, 23, can_tractor),
    LocationName.Maktar_Crane_PB: LocationData(LocationName.Maktar_Crane_PB, 24),
}

endako_location_table = {
    LocationName.Endako_Clank_Apartment_SS: LocationData(LocationName.Endako_Clank_Apartment_SS, 30),
    LocationName.Endako_Clank_Apartment_GB: LocationData(LocationName.Endako_Clank_Apartment_GB, 31),
    LocationName.Endako_Rescue_Clank_Heli: LocationData(LocationName.Endako_Rescue_Clank_Heli, 32, can_electrolyze),
    LocationName.Endako_Rescue_Clank_Thruster: LocationData(LocationName.Endako_Rescue_Clank_Thruster, 33, can_electrolyze),
    LocationName.Endako_Rescue_Clank_Hydro: LocationData(LocationName.Endako_Rescue_Clank_Hydro, 34, can_electrolyze),
    LocationName.Endako_Ledge_PB: LocationData(LocationName.Endako_Ledge_PB, 35),
    LocationName.Endako_Crane_PB: LocationData(LocationName.Endako_Crane_PB, 36, can_electrolyze),
    LocationName.Endako_Crane_NT: LocationData(
        LocationName.Endako_Crane_NT, 37,
        lambda state, player: can_electrolyze(state, player) and can_infiltrate(state, player)
    ),
}

barlow_location_table = {
    LocationName.Barlow_Inventor: LocationData(LocationName.Barlow_Inventor, 40, can_swingshot),
    LocationName.Barlow_Hoverbike_Race_Transmission: LocationData(
        LocationName.Barlow_Hoverbike_Race_Transmission, 41, can_pack
    ),
    LocationName.Barlow_Hoverbike_Race_Helmet: LocationData(
        LocationName.Barlow_Hoverbike_Race_Helmet, 42,
        lambda state, player: can_pack(state, player) and can_electrolyze(state, player)
    ),
    LocationName.Barlow_Hoverbike_Race_PB: LocationData(
        LocationName.Barlow_Hoverbike_Race_PB, 43,
        lambda state, player: can_pack(state, player) and can_electrolyze(state, player)
    ),
    LocationName.Barlow_Hound_Cave_PB: LocationData(LocationName.Barlow_Hound_Cave_PB, 44, can_swingshot),
}

feltzin_location_table = {
    LocationName.Feltzin_Defeat_Thug_Ships: LocationData(LocationName.Feltzin_Defeat_Thug_Ships, 50),
    LocationName.Feltzin_Race_PB: LocationData(LocationName.Feltzin_Race_PB, 51),
    LocationName.Feltzin_Cargo_Bay_NT: LocationData(LocationName.Feltzin_Cargo_Bay_NT, 52),

}

notak_location_table = {
    # TODO: Double check requirements on these locations
    LocationName.Notak_Top_Pier_Telescreen: LocationData(
        LocationName.Notak_Top_Pier_Telescreen, 60,
        lambda state, player: can_pack(state, player) and can_therminate(state, player)
    ),
    LocationName.Notak_Worker_Bots: LocationData(
        LocationName.Notak_Worker_Bots, 61,
        lambda state, player: can_pack(state, player) and can_therminate(state, player)
    ),
    LocationName.Notak_Behind_Building_PB: LocationData(LocationName.Notak_Behind_Building_PB, 62),
    LocationName.Notak_Promenade_Sign_PB: LocationData(LocationName.Notak_Promenade_Sign_PB, 63),
    LocationName.Notak_Timed_Dynamo_PB: LocationData(
        LocationName.Notak_Timed_Dynamo_PB, 64,
        lambda state, player: can_pack(state, player) and can_therminate(state, player) and can_dynamo(state, player)),
    LocationName.Notak_Promenade_End_NT: LocationData(LocationName.Notak_Promenade_End_NT, 65),
}

siberius_location_table = {
    LocationName.Siberius_Defeat_Thief: LocationData(LocationName.Siberius_Defeat_Thief, 70, can_swingshot),
    LocationName.Siberius_Flamebot_Ledge_PB: LocationData(
        LocationName.Siberius_Flamebot_Ledge_PB, 72,
        lambda state, player: can_pack(state, player) or can_tractor(state, player)
    ),
    LocationName.Siberius_Fenced_Area_PB: LocationData(LocationName.Siberius_Fenced_Area_PB, 73, can_pack),
}

# NOTICE: Clank pack and Swingshot are already logically required in order to access this planet
tabora_location_table = {
    # LocationName.Tabora_OmniWrench_10000: LocationData(LocationName.Tabora_OmniWrench_10000, 80),
    LocationName.Tabora_Meet_Angela: LocationData(LocationName.Tabora_Meet_Angela, 81),
    LocationName.Tabora_Underground_Mines_End: LocationData(
        LocationName.Tabora_Underground_Mines_End, 82, can_therminate
    ),
    LocationName.Tabora_Underground_Mines_PB: LocationData(
        LocationName.Tabora_Underground_Mines_PB, 83, can_therminate
    ),
    LocationName.Tabora_Canyon_Glide_PB: LocationData(
        LocationName.Tabora_Canyon_Glide_PB, 84,
        lambda state, player: can_therminate(state, player) and can_glide(state, player)
    ),
    LocationName.Tabora_Northeast_Desert_PB: LocationData(LocationName.Tabora_Northeast_Desert_PB, 85),
    LocationName.Tabora_Canyon_Glide_Pillar_NT: LocationData(
        LocationName.Tabora_Canyon_Glide_Pillar_NT, 86,
        lambda state, player: can_therminate(state, player) and can_glide(state, player)
    ),
}

dobbo_location_table = {
    LocationName.Dobbo_Defeat_Thug_Leader: LocationData(
        LocationName.Dobbo_Defeat_Thug_Leader, 90,
        lambda state, player: can_pack(state, player) and can_dynamo(state, player) and can_swingshot(state, player)
    ),
    # TODO: Check if clank is needed
    LocationName.Dobbo_Facility_Terminal: LocationData(
        LocationName.Dobbo_Facility_Terminal, 91,
        lambda state, player: can_dynamo(state, player) and can_swingshot(state, player) and
                              can_glide(state, player) and can_infiltrate(state, player)
    ),
    LocationName.Dobbo_Spiderbot_Room_PB: LocationData(
        LocationName.Dobbo_Spiderbot_Room_PB, 92,
        lambda state, player: can_dynamo(state, player) and can_swingshot(state, player)
    ),
    # TODO: Check if clank is needed
    LocationName.Dobbo_Facility_Glide_PB: LocationData(
        LocationName.Dobbo_Facility_Glide_PB, 93,
        lambda state, player: can_dynamo(state, player) and can_swingshot(state, player) and can_glide(state, player)
    ),
    # TODO: Check if clank is needed
    LocationName.Dobbo_Facility_Glide_NT: LocationData(
        LocationName.Dobbo_Facility_Glide_NT, 94,
        lambda state, player: can_dynamo(state, player) and can_swingshot(state, player) and can_glide(state, player)
    ),
}

hrugis_location_table = {
    LocationName.Hrugis_Destroy_Defenses: LocationData(LocationName.Hrugis_Destroy_Defenses, 100),
    LocationName.Hrugis_Race_PB: LocationData(LocationName.Hrugis_Race_PB, 101),
}

joba_location_table = {
    LocationName.Joba_First_Hoverbike_Race: LocationData(
        LocationName.Joba_First_Hoverbike_Race, 110,
        lambda state, player: can_swingshot(state, player)
    ),
    LocationName.Joba_Shady_Salesman: LocationData(LocationName.Joba_Shady_Salesman, 111, can_dynamo),
    LocationName.Joba_Arena_Battle: LocationData(
        LocationName.Joba_Arena_Battle, 112,
        lambda state, player: can_dynamo(state, player) and can_pack(state, player)
    ),
    LocationName.Joba_Arena_Cage_Match: LocationData(
        LocationName.Joba_Arena_Cage_Match, 113,
        lambda state, player: can_dynamo(state, player) and can_pack(state, player) and can_levitate(state, player)
    ),
    LocationName.Joba_Hidden_Cliff_PB: LocationData(
        LocationName.Joba_Hidden_Cliff_PB, 114,
        lambda state, player: can_dynamo(state, player) and can_swingshot(state, player)
    ),
    LocationName.Joba_Levitator_Tower_PB: LocationData(
        LocationName.Joba_Levitator_Tower_PB, 115,
        lambda state, player: can_dynamo(state, player) and can_pack(state, player) and can_levitate(state, player)
    ),
    LocationName.Joba_Hoverbike_Race_Shortcut_NT: LocationData(
        LocationName.Joba_Hoverbike_Race_Shortcut_NT, 116,
        lambda state, player: can_swingshot(state, player)
    ),
    LocationName.Joba_Timed_Dynamo_NT: LocationData(LocationName.Joba_Timed_Dynamo_NT, 117, can_dynamo),
}

todano_location_table = {
    LocationName.Todano_Search_Rocket_Silo: LocationData(
        LocationName.Todano_Search_Rocket_Silo, 120,
        lambda state, player:
            can_pack(state, player)
            and can_electrolyze(state, player)
            and can_infiltrate(state, player)
            and can_pack(state, player)
    ),
    LocationName.Todano_Stuart_Zurgo_Trade: LocationData(
        # TODO: Double check if clank is needed
        LocationName.Todano_Stuart_Zurgo_Trade, 121,
        lambda state, player:  can_electrolyze(state, player) and can_tractor(state, player) and
                               has_qwark_statuette(state, player)
    ),
    LocationName.Todano_Near_Stuart_Zurgo_PB: LocationData(
        # TODO: Double check if clank is needed
        LocationName.Todano_Near_Stuart_Zurgo_PB, 122,
        lambda state, player:  can_electrolyze(state, player) and can_tractor(state, player)
    ),
    LocationName.Todano_End_Tour_PB: LocationData(LocationName.Todano_End_Tour_PB, 123),
    LocationName.Todano_Spiderbot_Conveyor_PB: LocationData(
        LocationName.Todano_Spiderbot_Conveyor_PB, 124,
        lambda state, player: can_electrolyze(state, player) and can_tractor(state, player)
    ),
    LocationName.Todano_Rocket_Silo_NT: LocationData(
        LocationName.Todano_Rocket_Silo_NT, 125,
        lambda state, player: can_electrolyze(state, player) and can_infiltrate(state, player)
    ),
}

boldan_location_table = {
    LocationName.Boldan_Find_Fizzwidget: LocationData(
        LocationName.Boldan_Find_Fizzwidget, 130,
        lambda state, player: can_levitate(state, player) and can_gravity(state, player) and can_swingshot(state, player)
    ),
    LocationName.Boldan_Spiderbot_Alley_PB: LocationData(
        LocationName.Boldan_Spiderbot_Alley_PB, 131,
        lambda state, player: can_levitate(state, player)
    ),
    LocationName.Boldan_Floating_Platform_PB: LocationData(
        LocationName.Boldan_Floating_Platform_PB, 132,
        lambda state, player: can_levitate(state, player) and can_gravity(state, player)
    ),
    LocationName.Boldan_Upper_Dome_PB: LocationData(
        LocationName.Boldan_Upper_Dome_PB, 133,
        lambda state, player: can_levitate(state, player) and can_gravity(state, player) and can_swingshot(state, player)
    ),
    LocationName.Boldan_Fountain_NT: LocationData(
        LocationName.Boldan_Fountain_NT, 134,
        lambda state, player: can_levitate(state, player)
    ),
}

# NOTICE: Gravity Boots, Levitator and Infiltrator are already logically required in order to access this planet
aranos_location_table = {
    LocationName.Aranos_Control_Room: LocationData(LocationName.Aranos_Control_Room, 140),
    LocationName.Aranos_Plumber: LocationData(LocationName.Aranos_Plumber, 141),
    LocationName.Aranos_Under_Ship_PB: LocationData(
        LocationName.Aranos_Under_Ship_PB, 142,
        lambda state, player: can_pack(state, player)
    ),
}

gorn_location_table = {
    LocationName.Gorn_Defeat_Thug_Fleet: LocationData(LocationName.Gorn_Defeat_Thug_Fleet, 150),
    LocationName.Gorn_Race_PB: LocationData(LocationName.Gorn_Race_PB, 151),
}

snivelak_location_table = {
    LocationName.Snivelak_Rescue_Angela: LocationData(
        LocationName.Snivelak_Rescue_Angela, 160,
        lambda state, player: can_swingshot(state, player) and can_grind(state, player) and
                              can_gravity(state, player) and can_dynamo(state, player)
    ),
    LocationName.Snivelak_Dynamo_Platforms_PB: LocationData(
        LocationName.Snivelak_Dynamo_Platforms_PB, 161,
        lambda state, player: can_swingshot(state, player) and can_grind(state, player) and
                              can_gravity(state, player) and can_dynamo(state, player) and can_pack(state, player)
    ),
    LocationName.Snivelak_Swingshot_Tower_NT: LocationData(
        LocationName.Snivelak_Swingshot_Tower_NT, 162,
        # TODO: Try without Clank
        lambda state, player: can_swingshot(state, player) and can_pack(state, player)
    ),
}

smolg_location_table = {
    LocationName.Smolg_Balloon_Transmission: LocationData(
        LocationName.Smolg_Balloon_Transmission, 170,
        # TODO: Try without Clank
        lambda state, player: can_pack(state, player) and can_dynamo(state, player) and can_electrolyze(state, player)
    ),
    LocationName.Smolg_Distribution_Facility_End: LocationData(
        LocationName.Smolg_Distribution_Facility_End, 171,
        # TODO: Check what infiltrator does
        lambda state, player: can_pack(state, player) and can_dynamo(state, player) and
                              can_electrolyze(state, player) and can_grind(state, player)
    ),
    LocationName.Smolg_Mutant_Crab: LocationData(
        LocationName.Smolg_Mutant_Crab, 172,
        # TODO: Try without Clank
        lambda state, player: can_swingshot(state, player) and can_pack(state, player) and can_levitate(state, player)
    ),
    LocationName.Smolg_Floating_Platform_PB: LocationData(
        LocationName.Smolg_Floating_Platform_PB, 173,
        # TODO: Try without Clank
        lambda state, player: can_swingshot(state, player) and can_pack(state, player) and can_levitate(state, player)
    ),
    LocationName.Smolg_Warehouse_PB: LocationData(
        LocationName.Smolg_Warehouse_PB, 174,
        # TODO: Try without Clank
        lambda state, player: can_pack(state, player) and can_dynamo(state, player)
    ),
}

damosel_location_table = {
    LocationName.Damosel_Hypnotist: LocationData(
        LocationName.Damosel_Hypnotist, 180,
        lambda state, player: can_swingshot(state, player) and can_pack(state, player) and
                              can_therminate(state, player) and has_hypnomatic_parts(state, player)
    ),
    LocationName.Damosel_Train_Rails: LocationData(LocationName.Damosel_Train_Rails, 181, can_grind),
    LocationName.Damosel_Defeat_Mothership: LocationData(LocationName.Damosel_Defeat_Mothership, 182),
    LocationName.Damosel_Frozen_Fountain_PB: LocationData(
        LocationName.Damosel_Frozen_Fountain_PB, 183,
        lambda state, player: can_swingshot(state, player) and can_pack(state, player) and
                              can_therminate(state, player) and can_grind(state, player)
    ),
    LocationName.Damosel_Pyramid_PB: LocationData(
        LocationName.Damosel_Pyramid_PB, 184,
        lambda state, player: can_swingshot(state, player) and can_pack(state, player) and
                              can_therminate(state, player) and can_hypnotize(state, player)
    ),
}

grelbin_location_table = {
    LocationName.Grelbin_Find_Angela: LocationData(LocationName.Grelbin_Find_Angela, 190, can_hypnotize),
    LocationName.Grelbin_Mystic_More_Moonstones: LocationData(
        LocationName.Grelbin_Mystic_More_Moonstones, 191,
        lambda state, player: can_glide(state, player) and can_infiltrate(state, player)
    ),
    LocationName.Grelbin_Ice_Plains_PB: LocationData(
        LocationName.Grelbin_Ice_Plains_PB, 192,
        lambda state, player: can_glide(state, player) and can_infiltrate(state, player)
    ),
    LocationName.Grelbin_Underwater_Tunnel_PB: LocationData(LocationName.Grelbin_Underwater_Tunnel_PB, 193, can_hypnotize),
    LocationName.Grelbin_Yeti_Cave_PB: LocationData(
        LocationName.Grelbin_Yeti_Cave_PB, 194,
        lambda state, player: can_glide(state, player) and can_infiltrate(state, player) and can_hypnotize(state, player)
    ),
}

yeedil_location_table = {
    LocationName.Yeedil_Bridge_Grindrail_PB: LocationData(LocationName.Yeedil_Bridge_Grindrail_PB, 200, can_grind),
    LocationName.Yeedil_Tractor_Pillar_PB: LocationData(
        LocationName.Yeedil_Tractor_Pillar_PB, 201,
        lambda state, player: can_swingshot(state, player) and can_hypnotize(state, player) and
                              can_pack(state, player) and can_dynamo(state, player) and
                              can_infiltrate(state, player) and can_electrolyze(state, player) and
                              can_tractor(state, player) and can_grind(state, player)
    ),
    LocationName.Yeedil_Defeat_Mutated_Protopet: LocationData(
        LocationName.Yeedil_Defeat_Mutated_Protopet, None,
        lambda state, player: can_swingshot(state, player) and can_hypnotize(state, player) and
                              can_pack(state, player) and can_dynamo(state, player) and
                              can_infiltrate(state, player) and can_electrolyze(state, player)
    ),
}

every_location: dict[str, LocationData] = {
    **oozla_location_table,
    **maktar_location_table,
    **endako_location_table,
    **barlow_location_table,
    **feltzin_location_table,
    **notak_location_table,
    **siberius_location_table,
    **tabora_location_table,
    **dobbo_location_table,
    **hrugis_location_table,
    **joba_location_table,
    **todano_location_table,
    **boldan_location_table,
    **aranos_location_table,
    **gorn_location_table,
    **snivelak_location_table,
    **smolg_location_table,
    **damosel_location_table,
    **grelbin_location_table,
    **yeedil_location_table
}
