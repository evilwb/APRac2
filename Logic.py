from BaseClasses import CollectionState
from .Items import ItemName
import typing

from .data import Weapons

if typing.TYPE_CHECKING:
    from .Rac2Options import Rac2Options


def _get_options(state: CollectionState, player: int) -> 'Rac2Options':
    return state.multiworld.worlds[player].options


def can_dynamo(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Dynamo, player)


def can_tractor(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Tractor_Beam, player)


def can_swingshot(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Swingshot, player)


def can_therminate(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Thermanator, player)


def can_improved_jump(state: CollectionState, player: int) -> bool:
    return state.has_any([ItemName.Heli_Pack, ItemName.Thruster_Pack], player)


def can_heli(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Heli_Pack, player)


def can_grind(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Grind_Boots, player)


def can_gravity(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Gravity_Boots, player)


def can_charge(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Charge_Boots, player)


def can_hypnotize(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Hypnomatic, player)


def can_glide(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Glider, player)


def can_levitate(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Levitator, player)


def can_electrolyze(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Electrolyzer, player)


def can_infiltrate(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Infiltrator, player)


def can_spiderbot(state: CollectionState, player: int) -> bool:
    return state.has(Weapons.SPIDERBOT_GLOVE.name, player)


def has_qwark_statuette(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Qwark_Statuette, player)


def has_hypnomatic_parts(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.Hypnomatic_Part, player, 3)
