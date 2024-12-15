
from typing import TYPE_CHECKING, Optional

from NetUtils import NetworkItem

from .Rac2Interface import InventoryItemData
from .Items import item_table, ItemName

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


async def handle_receive_items(ctx: 'Rac2Context', current_items: dict[str, InventoryItemData]):
    remove_extra_items(ctx, current_items)
    for network_item in ctx.items_received:
        item_data = inventory_item_by_network_id(network_item.item, current_items)

        # Handle Single Item Upgrades
        if item_data.max_capacity == 1:
            await give_item_if_not_owned(ctx, item_data, network_item)
        elif item_data.max_capacity > 1:
            continue

    await handle_receive_platinum_bolts(ctx, current_items)
    await handle_receive_nanotech_boosts(ctx, current_items)
    await handle_receive_hypnomatic_parts(ctx, current_items)


async def give_item_if_not_owned(ctx: 'Rac2Context', item_data: InventoryItemData, network_item: NetworkItem):
    """Gives the item and notifies"""
    if item_data.current_amount == 0:
        ctx.game_interface.give_item_to_player(item_data, 1, 1)
        message = f"Received \14{item_data.name}\10"
        if network_item.location == -2:
            message += " (Starting Planet)"
        elif network_item.player != ctx.slot:
            message += f" from {ctx.player_names[network_item.player]}"
        ctx.notification_manager.queue_notification(message)


def remove_extra_items(ctx: 'Rac2Context', current_items: dict[str, InventoryItemData]):
    for item_data in current_items.values():
        if item_data.current_amount > 0 and item_data.id not in [net_item.item for net_item in ctx.items_received]:
            ctx.game_interface.give_item_to_player(item_data, 0, 1)


async def handle_receive_platinum_bolts(ctx: 'Rac2Context', current_items: dict[str, InventoryItemData]):
    plat_bolt_item = current_items[ItemName.Platinum_Bolt]
    bolts_received = 0
    sender = None
    for network_item in ctx.items_received:
        item_data = inventory_item_by_network_id(network_item.item, current_items)
        if item_data is None:
            continue

        if item_data.id == item_table[ItemName.Platinum_Bolt].id:
            bolts_received += 1
            sender = network_item.player

    diff = bolts_received - plat_bolt_item.current_amount
    if diff > 0 and plat_bolt_item.current_amount < plat_bolt_item.max_capacity:
        new_amount = min(bolts_received, plat_bolt_item.max_capacity)
        ctx.game_interface.give_item_to_player(plat_bolt_item, new_amount)
        message = f"Received {diff} \14Platinum Bolts\10" if diff > 1 else f"Received a \14Platinum Bolt\10"
        if sender != ctx.slot and diff == 1:
            message += f" ({ctx.player_names[sender]})"
        ctx.notification_manager.queue_notification(message)


async def handle_receive_nanotech_boosts(ctx: 'Rac2Context', current_items: dict[str, InventoryItemData]):
    nanotech_boost_item = current_items[ItemName.Nanotech_Boost]
    boosts_received = 0
    sender = None
    for network_item in ctx.items_received:
        item_data = inventory_item_by_network_id(network_item.item, current_items)
        if item_data is None:
            continue

        if item_data.id == item_table[ItemName.Nanotech_Boost].id:
            boosts_received += 1
            sender = network_item.player

    diff = boosts_received - nanotech_boost_item.current_amount
    if diff > 0 and nanotech_boost_item.current_amount < nanotech_boost_item.max_capacity:
        new_amount = min(boosts_received, nanotech_boost_item.max_capacity)
        ctx.game_interface.give_item_to_player(nanotech_boost_item, new_amount)
        message = f"Received {diff} \14Nanotech Boosts\10" if diff > 1 else f"Received a \14Nanotech Boost\10"
        if sender != ctx.slot and diff == 1:
            message += f" ({ctx.player_names[sender]})"
        ctx.notification_manager.queue_notification(message)


async def handle_receive_hypnomatic_parts(ctx: 'Rac2Context', current_items: dict[str, InventoryItemData]):
    hypnomatic_part_item = current_items[ItemName.Hypnomatic_Part]
    parts_received = 0
    sender = None
    for network_item in ctx.items_received:
        item_data = inventory_item_by_network_id(network_item.item, current_items)
        if item_data is None:
            continue

        if item_data.id == item_table[ItemName.Hypnomatic_Part].id:
            parts_received += 1
            sender = network_item.player

    diff = parts_received - hypnomatic_part_item.current_amount
    if diff > 0 and hypnomatic_part_item.current_amount < hypnomatic_part_item.max_capacity:
        new_amount = min(parts_received, hypnomatic_part_item.max_capacity)
        ctx.game_interface.give_item_to_player(hypnomatic_part_item, new_amount)
        message = f"Received {diff} \14Hypnomatic Parts\10" if diff > 1 else f"Received a \14Hypnomatic Part\10"
        if sender != ctx.slot and diff == 1:
            message += f" ({ctx.player_names[sender]})"
        ctx.notification_manager.queue_notification(message)


def inventory_item_by_network_id(network_id: int,
                                 current_inventory: dict[str, InventoryItemData]) -> Optional[InventoryItemData]:
    for item in current_inventory.values():
        if item.id == network_id:
            return item

    return None
