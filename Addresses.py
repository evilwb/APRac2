from dataclasses import dataclass
from typing import Optional, Dict


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
            self.feltzin_ship_challenge_1: int = 0x139619
            self.feltzin_ship_challenge_4: int = 0x13961C
            self.hrugis_ship_challenge_1: int = 0x13961E
            self.hrugis_ship_challenge_4: int = 0x139621
            self.hypnomatic_part1: int = 0x13963C
            self.hypnomatic_part2: int = 0x13963E
            self.hypnomatic_part3: int = 0x139641
            self.unlocked_movie_field0: int = 0x139768
            self.unlocked_movie_field1: int = 0x13976C
            self.unlocked_movie_field2: int = 0x139770
            self.siberius_thief_defeated: int = 0x139771
            self.selectable_planets: int = 0x139948
            self.ratchet_position: int = 0x189EA0
            self.moby_instances_pointer: int = 0x18C0B0
            self.ratchet_state: int = 0x18C0B4
            self.current_nanotech: int = 0x18C2EC
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
            self.wupash_complete_flag: int = 0x1A7C01
            # I use some unused addresses at the end of the platinum bolt table to store some extra data for AP.
            self.platinum_bolt_count: int = self.platinum_bolt_table + 0x6C
            self.nanotech_boost_count: int = self.platinum_bolt_table + 0x6D
            self.hypnomatic_part_count: int = self.platinum_bolt_table + 0x6E

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
                0: PlanetAddresses(
                    segment_pointers=0x1BF140,
                ),
                1: PlanetAddresses(
                    segment_pointers=0x1BF840,
                    planet_switch_trigger=0x1A8F14,
                    next_planet=0x1B2080,
                    skill_point_text=0x1A900A0,
                ),
                2: PlanetAddresses(
                    segment_pointers=0x1C0880,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B30C0,
                    skill_point_text=0x1B9A310,
                ),
                3: PlanetAddresses(
                    segment_pointers=0x1BFD00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2540,
                    skill_point_text=0x1C66600,
                ),
                4: PlanetAddresses(
                    segment_pointers=0x1BFA00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2000,
                    skill_point_text=0x1C8DF50,
                ),
                5: PlanetAddresses(
                    segment_pointers=0x1BFA40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2040,
                    skill_point_text=0x1874090,
                ),
                6: PlanetAddresses(
                    segment_pointers=0x1BFBC0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2340,
                    skill_point_text=0x1C726D0,
                ),
                7: PlanetAddresses(
                    segment_pointers=0x1BF580,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1E00,
                    skill_point_text=0x1981130,
                ),
                8: PlanetAddresses(
                    segment_pointers=0x1BFE80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2500,
                    skill_point_text=0x1C601C0,
                ),
                9: PlanetAddresses(
                    segment_pointers=0x1BFD80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2380,
                    skill_point_text=0x1CCE990,
                ),
                10: PlanetAddresses(
                    segment_pointers=0x1BFA00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2040,
                    skill_point_text=0x1649420,
                ),
                11: PlanetAddresses(
                    segment_pointers=0x1C0C40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B30C0,
                    skill_point_text=0x1C4EAD0,
                ),
                12: PlanetAddresses(
                    segment_pointers=0x1C0180,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B29C0,
                    skill_point_text=0x1C44EF0,
                ),
                13: PlanetAddresses(
                    segment_pointers=0x1BFC40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2440,
                    skill_point_text=0x1CCBA00,
                ),
                14: PlanetAddresses(
                    segment_pointers=0x1BF880,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B20C0,
                    skill_point_text=0x1B5A240,
                ),
                15: PlanetAddresses(
                    segment_pointers=0x1BFB40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2140,
                    skill_point_text=0x16734E0,
                ),
                16: PlanetAddresses(
                    segment_pointers=0x1BFE80,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2640,
                    skill_point_text=0x1CD5660,
                ),
                17: PlanetAddresses(
                    segment_pointers=0x1BFF40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2740,
                    skill_point_text=0x1CEA930,
                ),
                18: PlanetAddresses(
                    segment_pointers=0x1BFB40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2340,
                    skill_point_text=0x1C6B7F0,
                ),
                19: PlanetAddresses(
                    segment_pointers=0x1BFDC0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2500,
                    skill_point_text=0x1C49920,
                ),
                20: PlanetAddresses(
                    segment_pointers=0x1C0340,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2AC0,
                    skill_point_text=0x1C1B010,
                ),
                22: PlanetAddresses(
                    segment_pointers=0x1C0000,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1C40,
                    skill_point_text=0x168B7D0,
                ),
                23: PlanetAddresses(
                    segment_pointers=0x1C09C0,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B22C0,
                    skill_point_text=0x150F110,
                ),
                24: PlanetAddresses(
                    segment_pointers=0x1BEA40,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B12C0,
                    skill_point_text=0xEDE4B0,
                ),
                25: PlanetAddresses(
                    segment_pointers=0x1BF580,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1BC0,
                    skill_point_text=0xE13140,
                ),
                26: PlanetAddresses(
                    segment_pointers=0x1BEF00,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B1740,
                    skill_point_text=0x1171FF0,
                ),
                30: PlanetAddresses(
                    segment_pointers=0x1C0140,
                    planet_switch_trigger=0x1A8ED4,
                    next_planet=0x1B2840,
                ),
            }


@dataclass(frozen=True)
class PlanetAddresses:
    segment_pointers: Optional[int] = None
    planet_switch_trigger: Optional[int] = None
    next_planet: Optional[int] = None
    skill_point_text: Optional[int] = None



