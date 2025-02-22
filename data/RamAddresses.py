from .Planets import *


class Addresses:
    def __init__(self, game_version: str):
        if game_version == "SCUS-97268":
            # Global addresses
            self.controller_input: int = 0x138320
            self.endako_ratchet_freed: int = 0x1395C0
            self.endako_apartment_visited: int = 0x1395C1
            self.thermanator_tutorial_complete: int = 0x1395CA
            self.bought_from_worker_bots: int = 0x1395CD
            self.ship_shack_discovered: int = 0x1395CF
            self.dobbo_defeat_thug_leader: int = 0x1395E6
            self.electrolyzer_battle_victories: int = 0x1395E9
            self.barlow_hoverbike_race_victories: int = 0x139605
            self.feltzin_challenge_wins: int = 0x139619
            self.hrugis_challenge_wins: int = 0x13961E
            self.gorn_challenge_wins: int = 0x139623
            self.hypnomatic_part1: int = 0x13963C
            self.hypnomatic_part2: int = 0x13963E
            self.hypnomatic_part3: int = 0x139641
            self.unlocked_movie_field0: int = 0x139768
            self.unlocked_movie_field1: int = 0x13976C
            self.unlocked_movie_field2: int = 0x139770
            self.siberius_thief_defeated: int = 0x139771
            self.selectable_planets: int = 0x139948
            self.ratchet_position: int = 0x189EA0
            self.current_moby_instance_pointer: int = 0x18C0B0
            self.raritanium_count: int = 0x1A79FC
            self.ratchet_state: int = 0x18C0B4
            self.current_nanotech: int = 0x18C2EC
            self.current_bolts: int = 0x1A79F8
            self.current_bolt_multiplier: int = 0x1A7A32
            self.current_ratchet_xp: int = 0x1A7A0C
            self.challenge_mode_flag: int = 0x1A7A0A
            self.wrench_weapon_id: int = 0x139572
            self.current_armor_level: int = 0x1A7A18
            self.joba_hoverbike_1_victories: int = 0x13960F
            self.clank_disabled: int = 0x18C31C
            self.platinum_bolt_table: int = 0x19B278
            self.checkpoint_data: int = 0x19B2E8
            self.planet_state: int = 0x19B4A8
            self.loaded_flag: int = 0x1A7BE5
            self.quickselect: int = 0x1A73B8
            self.current_planet: int = 0x1A79F0
            self.nanotech_boost_table: int = 0x1A7A28
            self.skill_point_table: int = 0x1A7A60
            self.ship_upgrades: int = 0x1A7AF0
            self.inventory: int = 0x1A7AF8
            self.secondary_inventory: int = 0x1A7B30
            self.unlocked_planets: int = 0x1A7BC8
            self.highlighted_planets: int = 0x1A7BE8
            self.wupash_complete_flag: int = 0x1A7C01
            # I use some unused addresses at the end of the platinum bolt table to store some extra data for AP.
            self.platinum_bolt_count: int = self.platinum_bolt_table + 0x6C
            self.nanotech_boost_count: int = self.platinum_bolt_table + 0x6D
            self.hypnomatic_part_count: int = self.platinum_bolt_table + 0x6E
            self.tabora_wrench_cutscene_flag: int = self.platinum_bolt_table + 0x6F
            self.aranos_wrench_cutscene_flag: int = self.platinum_bolt_table + 0x70

            # Pause state is at 0x1A8F00 on all planets except for Oozla where it's at 0x1A8F40.
            self.pause_state: int = 0x1A8F00
            self.oozla_pause_state: int = 0x1A8F40

            # Addresses for data that only exists on certain planets
            self.oozla_box_breaker_func: int = 0x416440
            self.endako_free_ratchet_func: int = 0x3D20F8
            self.hrugis_race_controller_func: int = 0x42D1F0

            # Addresses for data that exists on all/most planets but has a different address per planet
            self.planet: Dict[int, PlanetAddresses] = {
                -1: PlanetAddresses(
                    segment_pointers=0x1BAEC0,
                ),
                ARANOS_TUTORIAL.number: PlanetAddresses(
                    segment_pointers=0x1BF140,
                ),
                OOZLA.number: PlanetAddresses(
                    segment_pointers=0x1BF840,
                    planet_switch_trigger=0x1A8F14,
                    next_planet=0x1B2080,
                    skill_point_text=0x1A900A0,
                ),
                MAKTAR_NEBULA.number: PlanetAddresses(
                    segment_pointers=0x1C0880,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B30C0,
                    skill_point_text=0x1B9A310,
                ),
                ENDAKO.number: PlanetAddresses(
                    segment_pointers=0x1BFD00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2540,
                    skill_point_text=0x1C66600,
                ),
                BARLOW.number: PlanetAddresses(
                    segment_pointers=0x1BFA00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2000,
                    skill_point_text=0x1C8DF50,
                ),
                FELTZIN_SYSTEM.number: PlanetAddresses(
                    segment_pointers=0x1BFA40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2040,
                    skill_point_text=0x1874090,
                    camara_state=0x1B1B20,
                ),
                NOTAK.number: PlanetAddresses(
                    segment_pointers=0x1BFBC0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2340,
                    skill_point_text=0x1C726D0,
                ),
                SIBERIUS.number: PlanetAddresses(
                    segment_pointers=0x1BF580,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1E00,
                    skill_point_text=0x1981130,
                ),
                TABORA.number: PlanetAddresses(
                    segment_pointers=0x1BFE80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2500,
                    skill_point_text=0x1C601C0,
                ),
                DOBBO.number: PlanetAddresses(
                    segment_pointers=0x1BFD80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2380,
                    skill_point_text=0x1CCE990,
                ),
                HRUGIS_CLOUD.number: PlanetAddresses(
                    segment_pointers=0x1BFA00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2040,
                    skill_point_text=0x1649420,
                    camara_state=0x1B1B20,
                ),
                JOBA.number: PlanetAddresses(
                    segment_pointers=0x1C0C40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B30C0,
                    skill_point_text=0x1C4EAD0,
                ),
                TODANO.number: PlanetAddresses(
                    segment_pointers=0x1C0180,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B29C0,
                    skill_point_text=0x1C44EF0,
                ),
                BOLDAN.number: PlanetAddresses(
                    segment_pointers=0x1BFC40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2440,
                    skill_point_text=0x1CCBA00,
                ),
                ARANOS_PRISON.number: PlanetAddresses(
                    segment_pointers=0x1BF880,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B20C0,
                    skill_point_text=0x1B5A240,
                ),
                GORN.number: PlanetAddresses(
                    segment_pointers=0x1BFB40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2140,
                    skill_point_text=0x16734E0,
                    camara_state=0x1B1BF0,
                ),
                SNIVELAK.number: PlanetAddresses(
                    segment_pointers=0x1BFE80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2640,
                    skill_point_text=0x1CD5660,
                ),
                SMOLG.number: PlanetAddresses(
                    segment_pointers=0x1BFF40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2740,
                    skill_point_text=0x1CEA930,
                ),
                DAMOSEL.number: PlanetAddresses(
                    segment_pointers=0x1BFB40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2340,
                    skill_point_text=0x1C6B7F0,
                ),
                GRELBIN.number: PlanetAddresses(
                    segment_pointers=0x1BFDC0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2500,
                    skill_point_text=0x1C49920,
                ),
                YEEDIL.number: PlanetAddresses(
                    segment_pointers=0x1C0340,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2AC0,
                    skill_point_text=0x1C1B010,
                ),
                DOBBO_ORBIT.number: PlanetAddresses(
                    segment_pointers=0x1C0000,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1C40,
                    skill_point_text=0x168B7D0,
                ),
                DAMOSEL_ORBIT.number: PlanetAddresses(
                    segment_pointers=0x1C09C0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B22C0,
                    skill_point_text=0x150F110,
                ),
                SHIP_SHACK.number: PlanetAddresses(
                    segment_pointers=0x1BEA40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B12C0,
                    skill_point_text=0xEDE4B0,
                ),
                WUPASH_NEBULA.number: PlanetAddresses(
                    segment_pointers=0x1BF580,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1BC0,
                    skill_point_text=0xE13140,
                    camara_state=0x1B1670,
                ),
                JAMMING_ARRAY.number: PlanetAddresses(
                    segment_pointers=0x1BEF00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1740,
                    skill_point_text=0x1171FF0,
                ),
                INSOMNIAC_MUSEUM.number: PlanetAddresses(
                    segment_pointers=0x1C0140,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2840,
                ),
            }


class PlanetAddresses(NamedTuple):
    segment_pointers: Optional[int] = None
    planet_switch_trigger: Optional[int] = None
    next_planet: Optional[int] = None
    skill_point_text: Optional[int] = None
    camara_state: Optional[int] = None
