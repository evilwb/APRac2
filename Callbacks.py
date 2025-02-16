from typing import TYPE_CHECKING

from . import Locations
from .Rac2Interface import Rac2Planet
from .TextManager import TextManager, get_rich_item_name_from_location
from .data import Items

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


def update(ctx: 'Rac2Context', ap_connected: bool):
    """Called continuously as long as a planet is loaded"""

    game_interface = ctx.game_interface
    planet = ctx.current_planet

    if planet is Rac2Planet.Title_Screen or planet is None:
        return

    replace_text(ctx, ap_connected)

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


def replace_text(ctx: 'Rac2Context', ap_connected: bool):
    try:
        manager = TextManager(ctx)

        # Handle HUD notifications
        if ctx.notification_manager.has_message_to_display() and ctx.game_interface.can_trigger_hud_notification():
            manager.set_hud_notification_text(ctx.notification_manager.pop_message_from_queue())
            ctx.game_interface.trigger_hud_notification_display()

        # Replace "Short Cuts" button text with "Go to Ship Shack", since that's what the button does now
        manager.inject(0x3202, "Go to Ship Shack")

        if not ap_connected:
            return

        if ctx.current_planet is Rac2Planet.Oozla:
            item_name = get_rich_item_name_from_location(ctx, Locations.OOZLA_MEGACORP_SCIENTIST.location_id)
            manager.inject(0x27AE, f"You need %d bolts for {item_name}")
            manager.inject(0x27AC, f"\x12 Buy {item_name} for %d bolts")

        elif ctx.current_planet is Rac2Planet.Maktar_Nebula:
            item_name = get_rich_item_name_from_location(ctx, Locations.MAKTAR_ARENA_CHALLENGE.location_id)
            manager.inject(0x2F46, f"You have earned {item_name}")

        elif ctx.current_planet is Rac2Planet.Barlow:
            item_name = get_rich_item_name_from_location(ctx, Locations.BARLOW_INVENTOR.location_id)
            manager.inject(0x27A0, f"You need %d bolts for {item_name}")
            manager.inject(0x279F, f"\x12 Buy {item_name} for %d bolts")

        elif ctx.current_planet is Rac2Planet.Feltzin_System:
            item_name = get_rich_item_name_from_location(ctx, Locations.FELTZIN_DEFEAT_THUG_SHIPS.location_id)
            manager.inject(0x11F5, f"Received {item_name}")
            item_name = get_rich_item_name_from_location(ctx, Locations.FELTZIN_RACE_PB.location_id)
            manager.inject(0x2FDF, f"Perfect Ring Bonus: {item_name}")

        elif ctx.current_planet is Rac2Planet.Notak:
            item_name = get_rich_item_name_from_location(ctx, Locations.NOTAK_WORKER_BOTS.location_id)
            manager.inject(0x27CE, f"You need %d bolts for {item_name}")
            manager.inject(0x27CF, f"\x12 Buy {item_name} for %d bolts")

        elif ctx.current_planet is Rac2Planet.Hrugis_Cloud:
            item_name = get_rich_item_name_from_location(ctx, Locations.HRUGIS_DESTROY_DEFENSES.location_id)
            manager.inject(0x11FB, f"Received {item_name}")
            item_name = get_rich_item_name_from_location(ctx, Locations.HRUGIS_RACE_PB.location_id)
            manager.inject(0x2FEB, f"Perfect Ring Bonus: {item_name}")

        elif ctx.current_planet is Rac2Planet.Joba:
            item_name = get_rich_item_name_from_location(ctx, Locations.JOBA_SHADY_SALESMAN.location_id)
            manager.inject(0x27BB, f"\x12 Buy {item_name} for %d bolts")
            manager.inject(0x27BC, f"You need %d bolts for {item_name}")
            item_name = get_rich_item_name_from_location(ctx, Locations.JOBA_ARENA_BATTLE.location_id)
            manager.inject(0x2F66, f"Battle for {item_name}")
            manager.inject(0x2F96, f"You have earned {item_name}")
            item_name = get_rich_item_name_from_location(ctx, Locations.JOBA_ARENA_CAGE_MATCH.location_id)
            manager.inject(0x2F67, f"Cage Match for {item_name}")
            manager.inject(0x2F97, f"You have earned {item_name}")

        elif ctx.current_planet is Rac2Planet.Todano:
            item_name = get_rich_item_name_from_location(ctx, Locations.TODANO_STUART_ZURGO_TRADE.location_id)
            manager.inject(0x27D3, f"You need the Qwark action figure for {item_name}")
            manager.inject(0x27D4, f"Trade Qwark action figure for {item_name}")

        elif ctx.current_planet is Rac2Planet.Aranos_Prison:
            item_name = get_rich_item_name_from_location(ctx, Locations.ARANOS_PLUMBER.location_id)
            manager.inject(0x27D5, f"You need %d bolts for {item_name}")
            manager.inject(0x27D6, f"\x12 Buy {item_name} for %d bolts")

        elif ctx.current_planet is Rac2Planet.Gorn:
            item_name = get_rich_item_name_from_location(ctx, Locations.GORN_DEFEAT_THUG_FLEET.location_id)
            manager.inject(0x11FF, f"Received {item_name}")
            item_name = get_rich_item_name_from_location(ctx, Locations.GORN_RACE_PB.location_id)
            manager.inject(0x2FF2, f"Perfect Ring Bonus: {item_name}")

        elif ctx.current_planet is Rac2Planet.Smolg:
            item_name = get_rich_item_name_from_location(ctx, Locations.SMOLG_MUTANT_CRAB.location_id)
            manager.inject(0x27D7, f"You need %d bolts for {item_name}")
            manager.inject(0x27D8, f"\x12 Buy {item_name} for %d bolts")

        elif ctx.current_planet is Rac2Planet.Damosel:
            item_name = get_rich_item_name_from_location(ctx, Locations.DAMOSEL_HYPNOTIST.location_id)
            manager.inject(0x27DA, f"You need %d bolts for {item_name}")
            manager.inject(0x27DB, f"\x12 Trade parts and %d bolts for {item_name}")

        elif ctx.current_planet is Rac2Planet.Grelbin:
            item_name = get_rich_item_name_from_location(ctx, Locations.GRELBIN_MYSTIC_MORE_MOONSTONES.location_id)
            manager.inject(0x27DE, f"You need 16 \x0CMoonstones\x08 for {item_name}")
            manager.inject(0x27DF, f"\x12 Trade 16 \x0CMoonstones\x08 for {item_name}")
    except TypeError:
        return
