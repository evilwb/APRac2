from BaseClasses import CollectionState
from .data.Items import *
import typing


def can_dynamo(state: CollectionState, player: int) -> bool:
    return state.has(DYNAMO.name, player)


def can_tractor(state: CollectionState, player: int) -> bool:
    return state.has(TRACTOR_BEAM.name, player)


def can_swingshot(state: CollectionState, player: int) -> bool:
    return state.has(SWINGSHOT.name, player)


def can_thermanate(state: CollectionState, player: int) -> bool:
    return state.has(THERMANATOR.name, player)


def can_improved_jump(state: CollectionState, player: int) -> bool:
    return state.has_any([HELI_PACK.name, THRUSTER_PACK.name], player)


def can_heli(state: CollectionState, player: int) -> bool:
    return state.has(HELI_PACK.name, player)


def can_grind(state: CollectionState, player: int) -> bool:
    return state.has(GRIND_BOOTS.name, player)


def can_gravity(state: CollectionState, player: int) -> bool:
    return state.has(GRAVITY_BOOTS.name, player)


def can_charge(state: CollectionState, player: int) -> bool:
    return state.has(CHARGE_BOOTS.name, player)


def can_hypnotize(state: CollectionState, player: int) -> bool:
    return state.has(HYPNOMATIC.name, player)


def can_glide(state: CollectionState, player: int) -> bool:
    return state.has(GLIDER.name, player)


def can_levitate(state: CollectionState, player: int) -> bool:
    return state.has(LEVITATOR.name, player)


def can_electrolyze(state: CollectionState, player: int) -> bool:
    return state.has(ELECTROLYZER.name, player)


def can_infiltrate(state: CollectionState, player: int) -> bool:
    return state.has(INFILTRATOR.name, player)


def can_spiderbot(state: CollectionState, player: int) -> bool:
    return state.has(SPIDERBOT_GLOVE.name, player)


def has_qwark_statuette(state: CollectionState, player: int) -> bool:
    return state.has(QWARK_STATUETTE.name, player)


def has_hypnomatic_parts(state: CollectionState, player: int) -> bool:
    return state.has(HYPNOMATIC_PART.name, player, 3)
