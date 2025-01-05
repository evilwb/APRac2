from typing import TYPE_CHECKING

from .Rac2Interface import Rac2Planet
from .Items import ItemName, equipment_table

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


def update(ctx: 'Rac2Context', ap_connected: bool):
    """Called continuously when as long as a planet is loaded"""

    game_interface = ctx.game_interface
    planet = ctx.current_planet

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
        has_heli_pack = game_interface.get_inventory_item(equipment_table[ItemName.Heli_Pack]).current_amount > 0
        has_swingshot = game_interface.get_inventory_item(equipment_table[ItemName.Swingshot]).current_amount > 0
        if not (has_heli_pack and has_swingshot):
            if ctx.notification_manager.queue_size() == 0:
                ctx.notification_manager.queue_notification(unstuck_message, 1.0)
    if planet == Rac2Planet.Aranos_Prison:
        has_gravity_boots = game_interface.get_inventory_item(equipment_table[ItemName.Gravity_Boots]).current_amount > 0
        has_levitator = game_interface.get_inventory_item(equipment_table[ItemName.Levitator]).current_amount > 0
        has_infiltrator = game_interface.get_inventory_item(equipment_table[ItemName.Infiltrator]).current_amount > 0
        if not (has_gravity_boots and has_levitator and has_infiltrator):
            if ctx.notification_manager.queue_size() == 0:
                ctx.notification_manager.queue_notification(unstuck_message, 1.0)


def init(ctx: 'Rac2Context', ap_connected: bool):
    """Called once when a new planet is loaded"""

