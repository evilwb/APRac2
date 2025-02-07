from typing import TYPE_CHECKING

from . import Rac2World
from .data import Items
from .data.Items import EquipmentData, CoordData, ProgressiveUpgradeData

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


async def handle_received_items(ctx: 'Rac2Context', current_items: dict[str, int]):
    for network_item in ctx.items_received:
        item = Items.from_id(network_item.item)

        if isinstance(item, EquipmentData) and current_items[item.name] == 0:
            ctx.game_interface.give_equipment_to_player(item)
            message = f"Received \14{item.name}\10"
            if network_item.player != ctx.slot:
                message += f" from {ctx.player_names[network_item.player]}"
            ctx.notification_manager.queue_notification(message)

        if isinstance(item, CoordData) and current_items[item.name] == 0:
            ctx.game_interface.unlock_planet(item.planet_number)
            message = f"Received \14{item.name}\10"
            if network_item.location == -2:
                message += " (Starting Planet)"
            elif network_item.player != ctx.slot:
                message += f" from {ctx.player_names[network_item.player]}"
            ctx.notification_manager.queue_notification(message)

        if isinstance(item, ProgressiveUpgradeData):
            current_level = item.get_level_func(ctx.game_interface)
            max_level = len(item.progressive_names)
            received_count = len([recv for recv in ctx.items_received if recv.item == item.item_id])
            new_level = min(received_count, max_level)
            if current_level != new_level:
                item.set_level_func(ctx.game_interface, new_level)
            if current_level < new_level:
                message = f"Received \14{item.progressive_names[new_level - 1]}\10"
                ctx.notification_manager.queue_notification(message)

    handle_received_collectables(ctx, current_items)


def handle_received_collectables(ctx: 'Rac2Context', current_items: dict[str, int]):
    for item in Items.COLLECTABLES:
        item_id = Rac2World.item_name_to_id[item.name]
        received_collectable = [received_item for received_item in ctx.items_received if received_item.item == item_id]
        in_game_amount = current_items[item.name]
        received_amount = len(received_collectable)
        if received_amount < 1:
            continue
        last_sender = received_collectable[-1].player

        diff = received_amount - in_game_amount
        if diff > 0 and in_game_amount < item.max_capacity:
            new_amount = min(received_amount, item.max_capacity)
            ctx.game_interface.give_collectable_to_player(item, new_amount)
            message = f"Received {diff} \14{item.name}\10"
            if diff == 1 and last_sender != ctx.slot:
                message += f" ({ctx.player_names[last_sender]})"
            ctx.notification_manager.queue_notification(message)
