from BaseClasses import CollectionState
from .data import Items
from .Rac2Options import Rac2Options


def can_dynamo(state: CollectionState, player: int) -> bool:
    return state.has(Items.DYNAMO.name, player)


def can_tractor(state: CollectionState, player: int) -> bool:
    return state.has(Items.TRACTOR_BEAM.name, player)


def can_swingshot(state: CollectionState, player: int) -> bool:
    return state.has(Items.SWINGSHOT.name, player)


def can_thermanate(state: CollectionState, player: int) -> bool:
    return state.has(Items.THERMANATOR.name, player)


def can_improved_jump(state: CollectionState, player: int) -> bool:
    return state.has_any([Items.HELI_PACK.name, Items.THRUSTER_PACK.name], player)


def can_heli(state: CollectionState, player: int) -> bool:
    return state.has(Items.HELI_PACK.name, player)


def can_grind(state: CollectionState, player: int) -> bool:
    return state.has(Items.GRIND_BOOTS.name, player)


def can_gravity(state: CollectionState, player: int) -> bool:
    return state.has(Items.GRAVITY_BOOTS.name, player)


def can_charge(state: CollectionState, player: int) -> bool:
    return state.has(Items.CHARGE_BOOTS.name, player)


def can_hypnotize(state: CollectionState, player: int) -> bool:
    return state.has(Items.HYPNOMATIC.name, player)


def can_glide(state: CollectionState, player: int) -> bool:
    return state.has(Items.GLIDER.name, player)


def can_levitate(state: CollectionState, player: int) -> bool:
    return state.has(Items.LEVITATOR.name, player)


def can_electrolyze(state: CollectionState, player: int) -> bool:
    return state.has(Items.ELECTROLYZER.name, player)


def can_infiltrate(state: CollectionState, player: int) -> bool:
    return state.has(Items.INFILTRATOR.name, player)


def can_spiderbot(state: CollectionState, player: int) -> bool:
    if not state.multiworld.worlds[player].options.randomize_megacorp_vendor:
        return state.has(Items.JOBA_COORDS.name, player)

    return state.has(Items.SPIDERBOT_GLOVE.name, player)


def has_qwark_statuette(state: CollectionState, player: int) -> bool:
    return state.has(Items.QWARK_STATUETTE.name, player)


def has_hypnomatic_parts(state: CollectionState, player: int) -> bool:
    return state.has(Items.HYPNOMATIC_PART.name, player, 3)


GLITCH_LOGIC_MEDIUM = 1
GLITCH_LOGIC_HARD = 2
GLITCH_LOGIC_EXPERT = 3


def get_options(state: CollectionState, player: int) -> Rac2Options:
    return state.multiworld.worlds[player].options


def oozla_end_store_cutscene_rule(state: CollectionState, player: int) -> bool:
    if can_dynamo(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def oozla_tractor_puzzle_pb_rule(state: CollectionState, player: int) -> bool:
    if can_tractor(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def oozla_swamp_ruins_pb_rule(state: CollectionState, player: int) -> bool:
    if can_dynamo(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def oozla_swamp_monster_ii_rule(state: CollectionState, player: int) -> bool:
    return (can_dynamo(state, player)
            and can_gravity(state, player))


def maktar_photo_booth_rule(state: CollectionState, player: int) -> bool:
    if can_electrolyze(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_heli(state, player)
                or can_charge(state, player))

    return False


def maktar_deactivate_jamming_array_rule(state: CollectionState, player: int) -> bool:
    if can_tractor(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_charge(state, player)

    return False


def maktar_jamming_array_pb_rule(state: CollectionState, player: int) -> bool:
    if can_tractor(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_charge(state, player)

    return False


def endako_rescue_clank_rule(state: CollectionState, player: int) -> bool:
    return can_electrolyze(state, player)


def endako_crane_pb_rule(state: CollectionState, player: int) -> bool:
    return can_electrolyze(state, player)


def endako_crane_nt_rule(state: CollectionState, player: int) -> bool:
    return (can_electrolyze(state, player)
            and can_infiltrate(state, player))


def barlow_inventor_rule(state: CollectionState, player: int) -> bool:
    if can_swingshot(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def barlow_overbike_race_rule(state: CollectionState, player: int) -> bool:
    if (can_improved_jump(state, player)
            and can_electrolyze(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_electrolyze(state, player)

    return False


def barlow_hound_cave_pb_rule(state: CollectionState, player: int) -> bool:
    return can_swingshot(state, player)


def notak_top_pier_telescreen_rule(state: CollectionState, player: int) -> bool:
    if (can_improved_jump(state, player)
            and can_thermanate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def notak_worker_bots_rule(state: CollectionState, player: int) -> bool:
    if (can_heli(state, player)
            and can_thermanate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def notak_timed_dynamo_rule(state: CollectionState, player: int) -> bool:
    if (can_thermanate(state, player)
            and can_improved_jump(state, player)
            and can_dynamo(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def siberius_defeat_thief_rule(state: CollectionState, player: int) -> bool:
    return can_swingshot(state, player)


def siberius_flamebot_ledge_pb_rule(state: CollectionState, player: int) -> bool:
    if can_tractor(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def siberius_fenced_area_pb_rule(state: CollectionState, player: int) -> bool:
    if can_heli(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def tabora_meet_angelar_rule(state: CollectionState, player: int) -> bool:
    return (can_heli(state, player)
            and can_swingshot(state, player))


def tabora_underground_mines_end_rule(state: CollectionState, player: int) -> bool:
    if (can_heli(state, player)
            and can_swingshot(state, player)
            and can_thermanate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_heli(state, player)
                and can_swingshot(state, player))

    return False


def tabora_canyon_glide_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_heli(state, player)
            and can_swingshot(state, player)
            and can_thermanate(state, player)
            and can_glide(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_heli(state, player)
                and can_swingshot(state, player)
                and can_glide(state, player))

    return False


def tabora_northeast_desert_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_heli(state, player)
            and can_swingshot(state, player))


def tabora_canyon_glide_pillar_nt_rule(state: CollectionState, player: int) -> bool:
    if (can_heli(state, player)
            and can_swingshot(state, player)
            and can_thermanate(state, player)
            and can_glide(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_heli(state, player)
                and can_swingshot(state, player))

    return False


def dobbo_defeat_thug_leader_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_dynamo(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_swingshot(state, player)

    return False


def dobbo_facility_terminal_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_glide(state, player)
            and can_dynamo(state, player)
            and can_electrolyze(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def dobbo_spiderbot_room_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_dynamo(state, player)
            and can_swingshot(state, player)
            and can_spiderbot(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_swingshot(state, player)

    return False


def dobbo_facility_glide_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_glide(state, player)
            and can_dynamo(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def dobbo_facility_glide_nt_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_glide(state, player)
            and can_dynamo(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def joba_hoverbike_race_rule(state: CollectionState, player: int) -> bool:
    if can_swingshot(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_charge(state, player)

    return False


def joba_shady_salesman_rule(state: CollectionState, player: int) -> bool:
    if (can_dynamo(state, player)
            and can_improved_jump(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def joba_arena_battle_rule(state: CollectionState, player: int) -> bool:
    if (can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_levitate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_levitate(state, player)

    return False


def joba_hidden_cliff_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_dynamo(state, player)
            and can_swingshot(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def joba_levitator_tower_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_levitate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_levitate(state, player)

    return False


def joba_timed_dynamo_nt_rule(state: CollectionState, player: int) -> bool:
    if can_dynamo(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def todano_search_rocket_silo_rule(state: CollectionState, player: int) -> bool:
    if (can_electrolyze(state, player)
            and can_infiltrate(state, player)
            and can_improved_jump(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def todano_stuart_zurgo_trade_rule(state: CollectionState, player: int) -> bool:
    if (can_electrolyze(state, player)
            and can_tractor(state, player)
            and has_qwark_statuette(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return has_qwark_statuette(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_tractor(state, player)
                and has_qwark_statuette(state, player))

    return False


def todano_facility_interior_rule(state: CollectionState, player: int) -> bool:
    if (can_electrolyze(state, player)
            and can_tractor(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return True

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_tractor(state, player)

    return False


def todano_near_stuart_zurgo_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_electrolyze(state, player)
            and can_tractor(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return True

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_tractor(state, player)

    return False


def todano_spiderbot_conveyor_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_electrolyze(state, player)
            and can_tractor(state, player)
            and can_improved_jump(state, player)
            and can_spiderbot(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_tractor(state, player)
                and can_spiderbot(state, player))

    return False


def todano_rocket_silo_nt_rule(state: CollectionState, player: int) -> bool:
    if (can_electrolyze(state, player)
            and can_infiltrate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def boldan_find_fizzwidget_rule(state: CollectionState, player: int) -> bool:
    if (can_levitate(state, player)
            and can_swingshot(state, player)
            and can_gravity(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return True

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_gravity(state, player)

    return False


def boldan_spiderbot_alley_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_levitate(state, player)
            and can_spiderbot(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def boldan_floating_platform_rule(state: CollectionState, player: int) -> bool:
    if (can_levitate(state, player)
            and can_gravity(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def boldan_fountain_nt_rule(state: CollectionState, player: int) -> bool:
    if can_levitate(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def aranos_control_room_rule(state: CollectionState, player: int) -> bool:
    if (can_gravity(state, player)
            and can_infiltrate(state, player)
            and can_levitate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return True

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return (can_infiltrate(state, player)
                and can_levitate(state, player))

    return False


def aranos_plumber_rule(state: CollectionState, player: int) -> bool:
    if (can_gravity(state, player)
            and can_levitate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def aranos_under_ship_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_gravity(state, player)
            and can_heli(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_heli(state, player)

    return False


def aranos_omniwrench_12000_rule(state: CollectionState, player: int) -> bool:
    if can_gravity(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def snivelak_rescue_angelak_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_grind(state, player)
            and can_gravity(state, player)
            and can_dynamo(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_swingshot(state, player)

    return False


def snivelak_dynamo_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_grind(state, player)
            and can_gravity(state, player)
            and can_dynamo(state, player)
            and can_heli(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_swingshot(state, player)

    return False


def snivelak_swingshot_tower_nt_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_heli(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_swingshot(state, player)

    return False


def smolg_balloon_transmission_rule(state: CollectionState, player: int) -> bool:
    if (can_improved_jump(state, player)
            and can_dynamo(state, player)
            and can_electrolyze(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_electrolyze(state, player)

    return False


def smolg_distribution_facility_end_rule(state: CollectionState, player: int) -> bool:
    if (can_improved_jump(state, player)
            and can_dynamo(state, player)
            and can_electrolyze(state, player)
            and can_grind(state, player)
            and can_infiltrate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return can_electrolyze(state, player)

    return False


def smolg_mutant_crab_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_levitate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not can_levitate(state, player):
            return False

        return (can_swingshot(state, player)
                or can_charge(state, player)
                or can_electrolyze(state, player))

    return False


def smolg_floating_platform_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_levitate(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not can_levitate(state, player):
            return False

        return (can_swingshot(state, player)
                or can_charge(state, player)
                or can_electrolyze(state, player))

    return False


def smolg_warehouse_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_dynamo(state, player)
            or can_improved_jump(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def damosel_hypnotist_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_thermanate(state, player)
            and has_hypnomatic_parts(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not has_hypnomatic_parts(state, player):
            return False

        return (can_charge(state, player)
                or (can_swingshot(state, player)
                    and can_thermanate(state, player)))

    return False


def damosel_train_rails_rule(state: CollectionState, player: int) -> bool:
    return can_grind(state, player)


def damosel_frozen_mountain_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_thermanate(state, player)
            and can_grind(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not can_grind(state, player):
            return False

        return (can_charge(state, player)
                or can_thermanate(state, player))

    return False


def damosel_pyramid_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_hypnotize(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not can_hypnotize(state, player):
            return False

        return (can_charge(state, player)
                or can_swingshot(state, player))

    return False


def grelbin_find_angela_rule(state: CollectionState, player: int) -> bool:
    if can_hypnotize(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def grelbin_mystic_more_moonstones_rule(state: CollectionState, player: int) -> bool:
    return (can_glide(state, player)
            and can_infiltrate(state, player))


def grelbin_ice_plains_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_glide(state, player)
            and can_infiltrate(state, player))


def grelbin_underwater_tunnel_pb_rule(state: CollectionState, player: int) -> bool:
    return can_hypnotize(state, player)


def grelbin_yeti_cave_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_glide(state, player)
            and can_infiltrate(state, player)
            and can_hypnotize(state, player))


def yeedil_defeat_mutated_protopet_rule(state: CollectionState, player: int) -> bool:
    if (can_hypnotize(state, player)
            and can_swingshot(state, player)
            and can_infiltrate(state, player)
            and can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_electrolyze(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return can_infiltrate(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not can_infiltrate(state, player):
            return False

        return (can_charge(state, player)
                or (can_hypnotize(state, player)
                    and can_swingshot(state, player)))

    return False


def yeedil_bridge_grindrail_pb_rule(state: CollectionState, player: int) -> bool:
    if can_grind(state, player):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        return True

    return False


def yeedil_tractor_pillar_pb_rule(state: CollectionState, player: int) -> bool:
    if (can_hypnotize(state, player)
            and can_swingshot(state, player)
            and can_infiltrate(state, player)
            and can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_electrolyze(state, player)
            and can_tractor(state, player)
            and can_grind(state, player)):
        return True

    options = get_options(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_EXPERT:
        return can_infiltrate(state, player)

    if options.glitch_logic_difficulty >= GLITCH_LOGIC_HARD:
        if not can_infiltrate(state, player):
            return False

        return (can_charge(state, player)
                or (can_hypnotize(state, player)
                    and can_swingshot(state, player)))

    return False