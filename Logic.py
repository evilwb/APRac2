from BaseClasses import CollectionState
from .data import Items


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
