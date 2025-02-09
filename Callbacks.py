from typing import TYPE_CHECKING

from . import Locations
from .Rac2Interface import Rac2Planet
from .data import Items

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


def update(ctx: 'Rac2Context', ap_connected: bool):
    """Called continuously as long as a planet is loaded"""

    game_interface = ctx.game_interface
    planet = ctx.current_planet

    if planet is Rac2Planet.Title_Screen or planet is None:
        return

    if ap_connected:
        replace_text(ctx)

    # Replace "Short Cut" button text with "Ship Shack"
    text_address = ctx.game_interface.get_text_address(0x3202)
    if text_address:
        new_text = "Ship Shack"
        ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode() + b'\x00')

    # Force Clank and Hydro-Pack to be enabled at all times.
    game_interface.pcsx2_interface.write_int8(game_interface.addresses.clank_disabled, 0)
    game_interface.pcsx2_interface.write_int8(game_interface.addresses.inventory + 4, 1)

    # Ship Wupash if option is enabled.
    if ap_connected and ctx.slot_data.get("skip_wupash_nebula", False):
        game_interface.pcsx2_interface.write_int8(game_interface.addresses.wupash_complete_flag, 1)

    button_input: int = game_interface.pcsx2_interface.read_int16(game_interface.addresses.controller_input)
    if button_input == 0x10F:  # L1 + L2 + R1 + R2 + SELECT
        if game_interface.switch_planet(Rac2Planet.Ship_Shack):
            game_interface.logger.info("Resetting to Ship Shack")

    if not ap_connected:
        if ctx.notification_manager.queue_size() == 0:
            ctx.notification_manager.queue_notification("\14Warning!\10 Not connected to Archipelago server", 1.0)

    unstuck_message: str = (
        "It appears that you don't have the required equipment to escape this area.\1\1"
        "Hold: \24+\25+\26+\27+SELECT to fly back to the \12Ship Shack\10."
    )
    if planet == Rac2Planet.Tabora:
        has_heli_pack = game_interface.count_inventory_item(Items.HELI_PACK) > 0
        has_swingshot = game_interface.count_inventory_item(Items.SWINGSHOT) > 0
        if not (has_heli_pack and has_swingshot):
            if ctx.notification_manager.queue_size() == 0:
                ctx.notification_manager.queue_notification(unstuck_message, 1.0)

    if planet == Rac2Planet.Aranos_Prison:
        has_gravity_boots = game_interface.count_inventory_item(Items.GRAVITY_BOOTS) > 0
        has_levitator = game_interface.count_inventory_item(Items.LEVITATOR) > 0
        has_infiltrator = game_interface.count_inventory_item(Items.INFILTRATOR) > 0
        if not (has_gravity_boots and has_levitator and has_infiltrator):
            if ctx.notification_manager.queue_size() == 0:
                ctx.notification_manager.queue_notification(unstuck_message, 1.0)


def init(ctx: 'Rac2Context', ap_connected: bool):
    """Called once when a new planet is loaded."""


def replace_text(ctx: 'Rac2Context'):
    try:
        if ctx.current_planet is Rac2Planet.Oozla:
            net_item = ctx.locations_info[Locations.OOZLA_MEGACORP_SCIENTIST.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27AE)
            new_text = f"You need %d bolts for \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:42] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x27AC)
            new_text = f"\x12 Buy \x0C{item_name}\x08 for %d bolts."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:34] + b'\x00')

        if ctx.current_planet is Rac2Planet.Maktar_Nebula:
            net_item = ctx.locations_info[Locations.MAKTAR_ARENA_CHALLENGE.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x2F46)
            new_text = f"You have earned \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:34] + b'\x00')

        if ctx.current_planet is Rac2Planet.Barlow:
            net_item = ctx.locations_info[Locations.BARLOW_INVENTOR.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27A0)
            new_text = f"You need %d bolts for \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:42] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x279F)
            new_text = f"\x12 Buy \x0C{item_name}\x08 for %d bolts"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:34] + b'\x00')

        if ctx.current_planet is Rac2Planet.Feltzin_System:
            net_item = ctx.locations_info[Locations.FELTZIN_DEFEAT_THUG_SHIPS.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x11F5)
            new_text = f"Received \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:54] + b'\00')

            net_item = ctx.locations_info[Locations.FELTZIN_RACE_PB.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x2FDF)
            new_text = f"Perfect Ring Bonus: \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:114] + b'\00')

        if ctx.current_planet is Rac2Planet.Notak:
            net_item = ctx.locations_info[Locations.NOTAK_WORKER_BOTS.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27CE)
            new_text = f"You need %d bolts for \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:38] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x27CF)
            new_text = f"\x12 Buy \x0C{item_name}\x08 for %d bolts"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:34] + b'\x00')

        if ctx.current_planet is Rac2Planet.Hrugis_Cloud:
            net_item = ctx.locations_info[Locations.HRUGIS_DESTROY_DEFENSES.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x11FB)
            new_text = f"Received \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:58] + b'\00')

            net_item = ctx.locations_info[Locations.HRUGIS_RACE_PB.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x2FEB)
            new_text = f"Perfect Ring Bonus: \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:114] + b'\00')

        if ctx.current_planet is Rac2Planet.Joba:
            net_item = ctx.locations_info[Locations.JOBA_SHADY_SALESMAN.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27BB)
            new_text = f"\x12 Buy \x0C{item_name}\x08 for %d bolts"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:28] + b'\00')
            text_address = ctx.game_interface.get_text_address(0x27BC)
            new_text = f"You need %d bolts for \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:38] + b'\00')

            net_item = ctx.locations_info[Locations.JOBA_ARENA_BATTLE.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x2F66)
            new_text = f"Battle for \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:30] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x2F96)
            new_text = f"You have earned \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:34] + b'\x00')

            net_item = ctx.locations_info[Locations.JOBA_ARENA_CAGE_MATCH.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x2F67)
            new_text = f"Cage Match for \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:31] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x2F97)
            new_text = f"You have earned \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:32] + b'\x00')

        if ctx.current_planet is Rac2Planet.Todano:
            net_item = ctx.locations_info[Locations.TODANO_STUART_ZURGO_TRADE.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27D4)
            new_text = f"Trade Qwark action figure for \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:50] + b'\x00')

        if ctx.current_planet is Rac2Planet.Aranos_Prison:
            net_item = ctx.locations_info[Locations.ARANOS_PLUMBER.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27D5)
            new_text = f"You need %d bolts for \01 \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:58] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x27D6)
            new_text = f"\x12 Buy \x0C{item_name}\x08 for %d bolts."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:44] + b'\x00')

        if ctx.current_planet is Rac2Planet.Gorn:
            net_item = ctx.locations_info[Locations.GORN_DEFEAT_THUG_FLEET.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x11FF)
            new_text = f"Received \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:62] + b'\00')

            net_item = ctx.locations_info[Locations.GORN_RACE_PB.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x2FF2)
            new_text = f"Perfect Ring Bonus: \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:110] + b'\00')

        if ctx.current_planet is Rac2Planet.Smolg:
            net_item = ctx.locations_info[Locations.SMOLG_MUTANT_CRAB.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27D7)
            new_text = f"You need %d bolts for \01 \x0C{item_name}"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:46] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x27D8)
            new_text = f"\x12 Buy \x0C{item_name}\x08 for %d bolts"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:42] + b'\x00')

        if ctx.current_planet is Rac2Planet.Damosel:
            net_item = ctx.locations_info[Locations.DAMOSEL_HYPNOTIST.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27DA)
            new_text = f"You need %d bolts for \01 \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:38] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x27DB)
            new_text = f"\x12 Trade parts and %d bolts for \x0C{item_name}\x08 for %d bolts"
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:40] + b'\x00')

        if ctx.current_planet is Rac2Planet.Grelbin:
            net_item = ctx.locations_info[Locations.GRELBIN_MYSTIC_MORE_MOONSTONES.location_id]
            item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
            text_address = ctx.game_interface.get_text_address(0x27DE)
            new_text = f"You need 16 \x0CMoonstones\x08 for \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:50] + b'\x00')
            text_address = ctx.game_interface.get_text_address(0x27DF)
            new_text = f"\x12 Trade 16 \x0CMoonstones\x08 for \x0C{item_name}\x08."
            ctx.game_interface.pcsx2_interface.write_bytes(text_address, new_text.encode()[:44] + b'\x00')
    except TypeError:
        return
