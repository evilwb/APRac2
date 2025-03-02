from typing import TYPE_CHECKING, Optional, Sequence

from . import Locations
from .Rac2Interface import Rac2Planet, Rac2Interface
from .TextManager import TextManager, get_rich_item_name_from_location
from .data import Items
from .ClientCheckLocations import INVENTORY_OFFSET_TO_LOCATION_ID
from .Rac2Interface import Rac2Planet, PauseState, Vendor
from .TextManager import TextManager
from .data import Items, Planets
from .data.Items import EquipmentData
from .data.Locations import LocationData
from .data.RamAddresses import Addresses
from .pcsx2_interface.pine import Pine

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


def update(ctx: 'Rac2Context', ap_connected: bool):
    """Called continuously as long as a planet is loaded"""

    game_interface = ctx.game_interface
    planet = ctx.current_planet

    if planet is Rac2Planet.Title_Screen or planet is None:
        return

    replace_text(ctx, ap_connected)

    if ap_connected:
        handle_vendor(ctx)

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


def init(ctx: 'Rac2Context', ap_connected: bool):
    # TODO: Make these warnings better
    unstuck_message: str = (
        "It appears that you don't have the required equipment to escape this area.\1\1"
        "Select Go to Ship Shack from the Special menu to fly back to the \12Ship Shack\10."
    )
    if ctx.current_planet == Rac2Planet.Tabora:
        has_heli_pack = ctx.game_interface.count_inventory_item(Items.HELI_PACK) > 0
        has_swingshot = ctx.game_interface.count_inventory_item(Items.SWINGSHOT) > 0
        if not (has_heli_pack and has_swingshot):
            ctx.notification_manager.queue_notification(unstuck_message, 5.0)

    if ctx.current_planet == Rac2Planet.Aranos_Prison:
        has_gravity_boots = ctx.game_interface.count_inventory_item(Items.GRAVITY_BOOTS) > 0
        has_levitator = ctx.game_interface.count_inventory_item(Items.LEVITATOR) > 0
        has_infiltrator = ctx.game_interface.count_inventory_item(Items.INFILTRATOR) > 0
        if not (has_gravity_boots and has_levitator and has_infiltrator):
            ctx.notification_manager.queue_notification(unstuck_message, 5.0)


def replace_text(ctx: 'Rac2Context', ap_connected: bool):
    try:
        manager = TextManager(ctx)

        # Replace "Short Cuts" button text with "Go to Ship Shack", since that's what the button does now
        manager.inject(0x3202, "Go to Ship Shack")

        if not ap_connected:
            return

        process_vendor_text(manager, ctx)

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
            manager.inject(0x27D4, f"\x12 Trade Qwark action figure for {item_name}")

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


def handle_vendor(ctx: "Rac2Context"):
    interface: Rac2Interface = ctx.game_interface
    addresses: Addresses = ctx.game_interface.addresses

    if interface.get_pause_state() == PauseState.VENDOR.value:
        if interface.vendor.mode is Vendor.Mode.CLOSED:
            if interface.vendor.is_megacorp():
                interface.vendor.change_mode(ctx, Vendor.Mode.MEGACORP)
            else:
                interface.vendor.change_mode(ctx, Vendor.Mode.GADGETRON)

    if interface.get_pause_state() != PauseState.VENDOR.value and interface.vendor.mode is not Vendor.Mode.CLOSED:
        interface.vendor.change_mode(ctx, Vendor.Mode.CLOSED)

    # Use Down/Up to toggle between ammo/weapon mode
    holding_down: bool = interface.pcsx2_interface.read_int16(addresses.controller_input) == 0x4000
    holding_up: bool = interface.pcsx2_interface.read_int16(addresses.controller_input) == 0x1000
    if holding_down and interface.vendor.mode is Vendor.Mode.MEGACORP:
        interface.vendor.change_mode(ctx, Vendor.Mode.AMMO)
    if holding_up and interface.vendor.mode is Vendor.Mode.AMMO:
        interface.vendor.change_mode(ctx, Vendor.Mode.MEGACORP)


def process_vendor_text(manager: TextManager, ctx: "Rac2Context") -> None:
    equipment_data: int = ctx.game_interface.addresses.planet[ctx.current_planet].equipment_data
    if not equipment_data:
        return

    vendor: Vendor = ctx.game_interface.vendor
    if vendor.mode is Vendor.Mode.MEGACORP:
        locations: Sequence[LocationData] = Locations.MEGACORP_VENDOR_LOCATIONS
        weapons: Sequence[EquipmentData] = Items.MEGACORP_VENDOR_WEAPONS
        for i in range(len(locations)):
            text_id = ctx.game_interface.pcsx2_interface.read_int32(equipment_data + weapons[i].offset * 0xE0 + 0x08)
            location_info = ctx.locations_info[locations[i].location_id]
            item_name = ctx.item_names.lookup_in_slot(location_info.item, location_info.player)
            manager.inject(text_id, item_name)
    elif vendor.mode is Vendor.Mode.GADGETRON:
        locations: Sequence[LocationData] = Locations.GADGETRON_VENDOR_LOCATIONS
        weapons: Sequence[EquipmentData] = Items.GADGETRON_VENDOR_WEAPONS
        for i in range(len(locations)):
            text_id = ctx.game_interface.pcsx2_interface.read_int32(equipment_data + weapons[i].offset * 0xE0 + 0x08)
            location_info = ctx.locations_info[locations[i].location_id]
            item_name = ctx.item_names.lookup_in_slot(location_info.item, location_info.player)
            manager.inject(text_id, item_name)
    else:
        locations: list[LocationData] = list(Locations.MEGACORP_VENDOR_LOCATIONS) + list(Locations.GADGETRON_VENDOR_LOCATIONS)
        weapons: list[EquipmentData] = list(Items.MEGACORP_VENDOR_WEAPONS) + list(Items.GADGETRON_VENDOR_WEAPONS)
        weapons.remove(Items.CLANK_ZAPPER)
        for i in range(len(locations)):
            text_id = ctx.game_interface.pcsx2_interface.read_int32(equipment_data + weapons[i].offset * 0xE0 + 0x08)
            manager.inject(text_id, weapons[i].name)

    # else:
    #     slots: list[Vendor.VendorSlot] = []
    #     for i, location_info in enumerate([ctx.locations_info[location.location_id] for location in Locations.MEGACORP_VENDOR_LOCATIONS], 1):
    #         # Don't place items on the vendor that have already been purchased.
    #         if location_info.location in ctx.checked_locations:
    #             continue
    #
    #         item_name = ctx.item_names.lookup_in_slot(location_info.item, location_info.player)
    #         item = None
    #         try:
    #             item = Items.from_name(item_name)
    #         except ValueError:
    #             pass
    #
    #         equipment_table = addresses.planet[ctx.current_planet].equipment_data
    #         text_manager.inject(interface.pcsx2_interface.read_int32(equipment_table + i * 0xE0 + 0x08), item_name)
    #         if isinstance(item, EquipmentData):
    #             # TODO: Add correct model
    #             slots.append(Vendor.VendorSlot(i, False, 0xEC8))
    #             interface.pcsx2_interface.write_int16(equipment_table + i * 0xE0 + 0x3C, item.icon_id)
    #         else:
    #             slots.append(Vendor.VendorSlot(i, False, 0xEC8))
    #             interface.pcsx2_interface.write_int16(equipment_table + i * 0xE0 + 0x3C, 0xEA75)
    #
    #     if mode_changed:
    #         interface.vendor.populate_slots(slots)


    # if mode_changed:
    #     interface.set_vendor_cursor(0)
    # for vendor_slot in range(32):
    #
    #
    #     item_id: int = interface.read_int32(vendor_slot_table + vendor_slot * 24)
    #     # End of slots
    #     if item_id == 0:
    #         break
    #
    #     location_id = INVENTORY_OFFSET_TO_LOCATION_ID.get(item_id, 0)
    #     if location_id == 0:
    #         continue
    #
    #     if location_id in ctx.checked_locations:
    #         continue
    #
    #     planet_number: Optional[int] = None
    #     for planet in Planets.LOGIC_PLANETS:
    #         for location in planet.locations:
    #             if location.location_id == location_id:
    #                 planet_number = planet.number
    #                 break
    #     assert planet_number is not None, "Vendor slot location not on any planet."
    #     has_slot: bool = ctx.game_interface.get_current_inventory()[Items.coord_for_planet(planet_number).name] > 0
    #
    #     item: EquipmentData = Items.from_offset(item_id)
    #     holding_l2: bool = interface.read_int16(addresses.controller_input) & 0x01 != 0
    #     has_item: bool = ctx.game_interface.get_current_inventory()[item.name] > 0
    #     text_id = interface.read_int32(addresses.planet[ctx.current_planet].equipment_data + item_id * 0xE0 + 0x8)
    #     if holding_l2 and has_item:
    #         interface.write_int32(vendor_slot_table + vendor_slot * 24 + 4, 1)
    #         text_manager.inject(text_id, item.name)
    #         interface.write_int16(addresses.planet[ctx.current_planet].equipment_data + item_id * 0xE0 + 0x3C, item.icon_id)
    #     elif has_slot:
    #         interface.write_int32(vendor_slot_table + vendor_slot * 24 + 4, 0)
    #         text_manager.inject(text_id, text_manager.get_formatted_item_name(location_id))
    #         interface.write_int16(addresses.planet[ctx.current_planet].equipment_data + item_id * 0xE0 + 0x3C, 0xEA75)
