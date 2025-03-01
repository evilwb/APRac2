import hashlib
import shutil
import mmap
from typing import Any, Callable, TYPE_CHECKING, Optional

import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .Rac2Options import ShuffleWeaponVendors
from .data import Items, IsoAddresses, RamAddresses
from . import MIPS, TextManager
from .data.RamAddresses import PlanetAddresses

if TYPE_CHECKING:
    from . import Rac2World

SCUS_97268_HASH = "3cbbb5127ee8a0be93ef0876f7781ee8"
NOP = bytes([0x00, 0x00, 0x00, 0x00])


class Rac2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = SCUS_97268_HASH
    game = "Ratchet & Clank 2"
    patch_file_ending = ".aprac2"
    result_file_ending = ".iso"
    procedure = [
        ("apply_tokens", ["token_data.bin"])
    ]
    notifier: Callable[[str, float], None]

    @staticmethod
    def check_hash(iso_path: str):
        basemd5 = hashlib.md5()
        with open(iso_path, "rb") as iso:
            basemd5.update(mmap.mmap(iso.fileno(), 0, access=mmap.ACCESS_READ))
        md5_hash = basemd5.hexdigest()
        if md5_hash not in {SCUS_97268_HASH}:
            raise Exception("Supplied Base ISO does not match known MD5 for a supported release."
                            "\nPlease verify that you are using the correct version of the game."
                            "\nYou should delete `Archipelago/Ratchet & Clank 2.iso' if you want to try again with a different ISO")
        Rac2ProcedurePatch.hash = md5_hash

    @staticmethod
    def get_game_version_from_iso(iso_path: str) -> Optional[str]:
        with open(iso_path, "rb") as iso:
            iso.seek(0x828F5)
            if iso.read(11) == b"SCUS_972.68":
                return "SCUS-97268"
        return None

    @staticmethod
    def apply_tokens_mmap(caller: APProcedurePatch, rom: mmap, token_file: str) -> None:
        token_data = caller.get_file(token_file)
        token_count = int.from_bytes(token_data[0:4], "little")
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = int.from_bytes(token_data[bpr + 1:bpr + 5], "little")
            size = int.from_bytes(token_data[bpr + 5:bpr + 9], "little")
            data = token_data[bpr + 9:bpr + 9 + size]
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                arg = data[0]
                if token_type == APTokenTypes.AND_8:
                    rom[offset] = rom[offset] & arg
                elif token_type == APTokenTypes.OR_8:
                    rom[offset] = rom[offset] | arg
                else:
                    rom[offset] = rom[offset] ^ arg
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                length = int.from_bytes(data[:4], "little")
                value = int.from_bytes(data[4:], "little")
                if token_type == APTokenTypes.COPY:
                    rom[offset: offset + length] = rom[value: value + length]
                else:
                    rom[offset: offset + length] = bytes([value] * length)
            else:
                rom[offset:offset + len(data)] = data
            bpr += 9 + size
        return

    def patch_mmap(self, target: str, notifier: Callable[[str, float], None]) -> bool:
        self.read()
        notifier("First time setup. This may take some time.", 0)
        settings.FilePath.md5s = [SCUS_97268_HASH]
        try:
            iso_file = settings.get_settings().rac2_options.iso_file
        except ValueError:
            notifier(
                "[color=#FF0000][size=20]Error[/size]"
                "\n\nThe supplied ISO is not a supported version of the game."
                "\nOnly [b]US Version 1.01 (SCUS-97268)[/b] is supported right now.[/color]"
                "\n\n[i]You can close this window when you are done reading.[/i]",
                0
            )
            return False
        notifier("Verifying game version...", 0)
        if not self.get_game_version_from_iso(iso_file):
            notifier(
                "[color=#FF0000][size=20]Error[/size]"
                "\n\nThe [b]Ratchet & Clank 2.iso[/b] in the [b]Archipelago Folder[/b] is invalid."
                "\nPlease remove is and try again.[/color]"
                "\n\n[i]You can close this window when you are done reading.[/i]",
                0
            )
            return False
        notifier("Game version supported. \n\nCreating new copy of ISO...", 0)
        shutil.copy(iso_file, target)
        notifier("Patching ISO...", 0)
        with open(target, "r+b") as file:
            self.apply_tokens_mmap(self, mmap.mmap(file.fileno(), 0), "token_data.bin")
        notifier("Patching complete!", 100)
        return True

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)


def generate_patch(world: "Rac2World", patch: Rac2ProcedurePatch, instruction=None) -> None:
    # TODO: use for other game versions
    # if world.options.game_version is ...
    #     addresses = IsoAddresses.Addresses*
    #     patch.hash = ...
    if True:
        addresses = IsoAddresses.AddressesSCUS97268
        ram = RamAddresses.Addresses("SCUS-97268")

    """---------------
    Core
    ---------------"""
    # Set 'Planet Loaded' byte to 1 when a new planet is done loading and about to start running.
    patch.write_token(APTokenTypes.WRITE, addresses.MAIN_LOOP_FUNC + 0x1C, bytes([0x01, 0x00, 0x11, 0x24]))
    patch.write_token(APTokenTypes.WRITE, addresses.MAIN_LOOP_FUNC + 0x24, bytes([0xF5, 0x8B, 0x91, 0xA3]))

    # Define a custom "game name" for memcard folders & files, so save files are not compatible between different seeds
    generated_game_name = f"AP{hex((world.multiworld.seed + world.player) & 0xFFFFF)[2:].upper()}"
    for address in addresses.MEMCARD_GAME_NAMES:
        patch.write_token(APTokenTypes.WRITE, address, generated_game_name.encode())

    """---------------
    Multiple planets
    ---------------"""
    # Change new game starting planet to Slim's Ship Shack
    for address in addresses.GO_STARTING_PLANET_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x38, bytes([0x18, 0x00, 0x04, 0x64]))

    # Set 'Planet Loaded' byte to 0 when a new planet starts loading.
    for address in addresses.PLANET_MAIN_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0xD2C, bytes([0xF5, 0x8B, 0x80, 0xA3]))
    patch.write_token(APTokenTypes.WRITE, addresses.TITLE_SCREEN_MAIN_FUNC + 0x8F0, bytes([0xF5, 0x8B, 0x80, 0xA3]))
    patch.write_token(APTokenTypes.WRITE, addresses.QUIT_TITLE_MAIN_FUNC + 0x830, bytes([0xF5, 0x8B, 0x80, 0xA3]))

    # Disable game failsafe that unlocks any planet we land on if we don't have it unlocked already.
    for address in addresses.SETUP_PLANET_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x144, bytes([0x07, 0x00, 0x00, 0x10]))

    # Make it so the vendor only unlocks weapons that are new to a planet but not all weapons from prior planets.
    for address in addresses.IS_BUYABLE_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x68, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x6C, bytes([0x03, 0x00, 0x50, 0x14]))

    # Disable game failsafe that disable Clank if you don't have heli-pack unlocked when loading into a planet.
    for address in addresses.SETUP_RATCHET_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x3BC, NOP)

    # prevent planets from getting added to the ship menu when a new planet is unlocked
    for address in addresses.UNLOCK_PLANET_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x4C, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x58, bytes([0x10, 0x00, 0x00, 0x10]))

    # prevent all planet unlock message popups
    for address in addresses.PLANET_UNLOCK_MESSAGE_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x10, bytes([0x42, 0x00, 0x00, 0x10]))

    # prevent normal platinum bolt received message
    for address in addresses.PLAT_BOLT_UPDATE_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x27C, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x43C, NOP)

    # disable nanotech boost help message
    for address in addresses.NANOTECH_BOOST_UPDATE_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x3A8, NOP)

    # Change variable checked by starmap to display a planet
    for address in addresses.STARMAP_MENU_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x144, bytes([0x20, 0x00, 0x43, 0x90]))

    # Handle options altering rewards
    if world.options.no_revisit_reward_change:
        # When loading both base XP and revisit XP to write them in the moby instance, put base XP in both instead
        for address in addresses.RESET_MOBY_FUNCS:
            # Use base bolts as revisit bolts
            patch.write_token(APTokenTypes.WRITE, address + 0x1384, bytes([0x00, 0x00, 0x45, 0x8E]))  # lw a3,(s2)
            patch.write_token(APTokenTypes.WRITE, address + 0x1388, bytes([0x04, 0x00, 0x52, 0x26]))  # addiu s2,s2,0x4
            # Use base XP as revisit XP
            patch.write_token(APTokenTypes.WRITE, address + 0x139C, bytes([0x00, 0x00, 0x47, 0x8E]))  # lw a3,(s2)
            patch.write_token(APTokenTypes.WRITE, address + 0x13A0, bytes([0x04, 0x00, 0x52, 0x26]))  # addiu s2,s2,0x4

    # Replace factors in the reward degradation by values which depend on
    for address in addresses.KILL_COUNT_MULT_TABLES:
        if world.options.no_kill_reward_degradation:
            # Put 100% XP & Bolts in every case
            patch.write_token(APTokenTypes.WRITE, address, bytes([100] * 32))
        elif world.options.no_revisit_reward_change:
            # Put the base scaling from vanilla game for XP & Bolts even for revisits
            patch.write_token(APTokenTypes.WRITE, address, bytes([100, 50, 40, 30, 25, 20, 15, 10] * 4))

    """ Normally, the game will iterate through the entire collected platinum bolt table whenever it needs to get your 
    current platinum bolt count. This changes it to read a single byte that we control to get that count instead. This 
    is done to decouple the platinum bolt count from platinum bolt locations checked. This same concept is also applied 
    to nanotech boosts below. """
    for address in addresses.PLAT_BOLT_COUNT_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x4, bytes([0x13, 0x00, 0x00, 0x10]))
        patch.write_token(APTokenTypes.WRITE, address + 0x8, bytes([0xE4, 0xB2, 0x46, 0x90]))

    # Same for nanotech boosts
    for address, spaceish_wars_address in zip(addresses.NANOTECH_COUNT_FUNCS, addresses.SPACEISH_WARS_FUNCS):
        # Inject a custom procedure run on each tick of the main loop of each planet.
        # It will be called through the NANOTECH_COUNT_FUNC since we are removing a few instructions there,
        # leaving space for a call.
        planet = ram.planet[IsoAddresses.get_planet_id_from_iso_address(address)]
        patch.write_token(APTokenTypes.WRITE, spaceish_wars_address, custom_main_loop(ram, planet))

        patch.write_token(APTokenTypes.WRITE, address + 0x70, bytes([0xE5, 0xB2, 0xA5, 0x90]))  # lbu a1,-0x4D1B(a1)
        patch.write_token(APTokenTypes.WRITE, address + 0x74, bytes([0x00, 0x00, 0xA4, 0x8F]))  # lw a0,0x0(sp)
        patch.write_token(APTokenTypes.WRITE, address + 0x78, bytes([0x21, 0x10, 0x85, 0x00]))  # addu v0,a0,a1
        patch.write_token(APTokenTypes.WRITE, address + 0x7C, MIPS.jal(planet.spaceish_wars_func))
        patch.write_token(APTokenTypes.WRITE, address + 0x80, bytes([0x00, 0x00, 0xA2, 0xAF]))  # sw v0,0x0(sp)
        patch.write_token(APTokenTypes.WRITE, address + 0x84, bytes([0x07, 0x00, 0x00, 0x10]))  # beq zero,zero,0x7
        patch.write_token(APTokenTypes.WRITE, address + 0x88, MIPS.nop())

    # Prevent Platinum Bolt received message popup at the end of ship races.
    for address in addresses.RACE_CONTROLLER_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x1FC, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x36C, NOP)

    # Reuse "Short Cuts" button on special manu to travel to Ship Shack.
    for address in addresses.SPECIAL_MENU_FUNCS:
        # Enable button outside of Challenge Mode.
        patch.write_token(APTokenTypes.WRITE, address + 0x1B8, NOP * 2)
    for address in addresses.SHORTCUT_MENU_FUNCS:
        # Branch directly to switch planet function call.
        patch.write_token(APTokenTypes.WRITE, address + 0x20, bytes([0x63, 0x00, 0x00, 0x10]))
        # Set arg0 to 0x18 for ship shack
        patch.write_token(APTokenTypes.WRITE, address + 0x24, bytes([0x18, 0x00, 0x04, 0x24]))

    # Allow first-person mode outside of NG+ if requested in options
    if world.options.allow_first_person_mode:
        for address in addresses.SPECIAL_MENU_FUNCS:
            patch.write_token(APTokenTypes.WRITE, address + 0x1B0, NOP * 2)
            
    # Enable bolt multiplier outside of NG+ if requested in options
    if world.options.enable_bolt_multiplier:
        for address in addresses.TRACK_KILL_FUNCS:
            patch.write_token(APTokenTypes.WRITE, address + 0x9C, NOP)  # beq b0,zero,0x1e

    if world.options.free_challenge_selection:
        patch_free_challenge_selection(patch, addresses)

    if world.options.nanotech_xp_multiplier != 100:
        alter_nanotech_xp_tables(patch, addresses, world.options.nanotech_xp_multiplier.value)

    if world.options.weapon_xp_multiplier != 100:
        alter_weapon_xp_tables(patch, addresses, world.options.weapon_xp_multiplier.value)

    """----------------------
    Shuffle Weapons Vendors
    ----------------------"""
    # Handle "weapons" mode.
    if world.options.shuffle_weapon_vendors == ShuffleWeaponVendors.option_weapons:
        weapons = list(Items.WEAPONS)
        weapons.remove(Items.CLANK_ZAPPER)
        weapons.remove(Items.SHEEPINATOR)
        weapons.remove(Items.SPIDERBOT_GLOVE)
        unlock_planets = [1, 1, 3, 3, 4, 6, 8, 8, 9, 11, 12, 14, 14]
        world.random.shuffle(weapons)

        first_weapon = weapons[0]
        second_weapon = weapons[1]
        megacorp_weapons = weapons[2:len(unlock_planets) + 2]
        gadgetron_weapons = weapons[len(unlock_planets) + 2:]

        # Patch starting weapons.
        for address in addresses.AVAILABLE_ITEM_FUNCS:
            # First weapon.
            weapon_id = first_weapon.offset
            low = (0x7AF8 + weapon_id).to_bytes(2, "little")
            patch.write_token(APTokenTypes.WRITE, address + 0x8, low)
            patch.write_token(APTokenTypes.WRITE, address + 0x18, weapon_id.to_bytes(1, "little"))
            patch.write_token(APTokenTypes.WRITE, address + 0x20, weapon_id.to_bytes(1, "little"))
            patch.write_token(APTokenTypes.WRITE, address + 0x24, bytes([0x40, 0x00, 0x83, 0x34]))
            patch.write_token(APTokenTypes.WRITE, address + 0x28, weapon_id.to_bytes(1, "little"))

            # Second weapon.
            weapon_id = second_weapon.offset
            low = (0x7AF8 + weapon_id).to_bytes(2, "little")
            patch.write_token(APTokenTypes.WRITE, address + 0x40, low)
            patch.write_token(APTokenTypes.WRITE, address + 0x50, weapon_id.to_bytes(1, "little"))
            patch.write_token(APTokenTypes.WRITE, address + 0x58, weapon_id.to_bytes(1, "little"))
            patch.write_token(APTokenTypes.WRITE, address + 0x5C, bytes([0x40, 0x00, 0x83, 0x34]))

        # Patch Megacorp vendor.
        for address in addresses.VENDOR_REQUIREMENT_TABLES:
            for i, planet in enumerate(unlock_planets):
                patch.write_token(APTokenTypes.WRITE, address + i * 8, megacorp_weapons[i].offset.to_bytes(4, "little"))
                patch.write_token(APTokenTypes.WRITE, address + i * 8 + 4, planet.to_bytes(4, "little"))

        # Patch Gadgetron vendor.
        for address in addresses.POPULATE_VENDOR_SLOT_FUNCS:
            for i, offset in enumerate(range(0x8C0, 0x8D8, 4)):
                patch.write_token(APTokenTypes.WRITE, address + offset, gadgetron_weapons[i].offset.to_bytes(1, "little"))

    """--------- 
    Oozla 
    ---------"""
    # Megacorp Scientist
    address = addresses.MEGACORP_SCIENTIST_FUNC
    # check secondary inventory table instead of primary when determining if the purchase has already occurred.
    patch.write_token(APTokenTypes.WRITE, address + 0x70, bytes([0x5E, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x49C, bytes([0x5E, 0x7B, 0x42, 0x90]))
    # Replace code that calls give_item, equip_item, and display_pickup_message with code that just
    # sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x4e0, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x4e4, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x4e8, bytes([0x5E, 0x7B, 0x44, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x4f4, NOP)
    # Prevent post buy cutscene from playing
    patch.write_token(APTokenTypes.WRITE, address + 0x518, NOP)

    # Dynamo Pickup
    address = addresses.DYNAMO_PICKUP_FUNC
    # check secondary inventory table instead of primary when determining if pickup has already occurred.
    patch.write_token(APTokenTypes.WRITE, address + 0x58, bytes([0x54, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x49C, bytes([0x54, 0x7B, 0x42, 0x90]))
    # Replace code that calls give_item and equip_item with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x19C, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A0, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A4, bytes([0x54, 0x7B, 0x44, 0xA0]))
    # prevent pickup message popup
    patch.write_token(APTokenTypes.WRITE, address + 0x1B0, NOP)
    # Disable post pickup cutscene
    patch.write_token(APTokenTypes.WRITE, address + 0x194, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x1EC, NOP)

    # Box Breaker Pickup
    address = addresses.BOX_BREAKER_PICKUP_FUNC
    # check secondary inventory table instead of primary when determining if pickup has already occurred.
    patch.write_token(APTokenTypes.WRITE, address + 0x7C, bytes([0x62, 0x7B, 0x42, 0x90]))
    # Replace code that calls give_item and display_pickup_message with code that just sets secondary
    # inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x590, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x594, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x598, bytes([0x62, 0x7B, 0x44, 0xA0]))

    # Swamp Monster Gate
    address = addresses.SWAMP_MONSTER_GATE_FUNC
    # check secondary inventory table instead of primary when determining if boss kill has already occurred.
    patch.write_token(APTokenTypes.WRITE, address + 0x110, bytes([0x62, 0x7B, 0x42, 0x90]))

    # Prevent spawning at Scientist when Tractor Beam is collected.
    patch.write_token(APTokenTypes.WRITE, addresses.OOZLA_CONTROLLER_FUNC + 0x108, NOP)

    """--------- 
    Maktar
    ---------"""
    # Prevent spawning at Arena exit when Electrolyzer is collected but Electrolyzer puzzles are not completed
    patch.write_token(APTokenTypes.WRITE, addresses.MAKTAR_CONTROLLER_FUNC + 0x6B0, NOP)
    # Arena Controller
    address = addresses.ARENA_CONTROLLER_FUNC
    # Replace code that calls give_item and equip_item with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x30F4, bytes([0x1A, 0x00, 0x05, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x30F8, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x30FC, bytes([0x56, 0x7B, 0xA4, 0xA0]))
    # Change the code that determines where you exit the arena to check for Electrolyzer instead of challenge 1 victory
    patch.write_token(APTokenTypes.WRITE, address + 0x2EEC, bytes([0x1A, 0x00, 0x10, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x2EF4, bytes([0x26, 0x00, 0x02, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x2EF8, bytes([0xF8, 0x7A, 0x10, 0x26]))

    """--------- 
    Endako   
    ---------"""
    # Endako Controller
    address = addresses.ENDAKO_CONTROLLER_FUNC
    # Use Secondary Inventory to determine if location has been checked
    patch.write_token(APTokenTypes.WRITE, address + 0x54, bytes([0x3D, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0xA8, bytes([0x3D, 0x7B, 0x42, 0x90]))
    # Disable hard checkpoint at Swingshot tutorial when reloading the planet
    patch.write_token(APTokenTypes.WRITE, address + 0x64, bytes([0x0F, 0x00, 0x00, 0x10]))
    # Controller sub-function
    address = addresses.APARTMENT_PICKUP_FUNC
    # Replace code that calls give_item and equip_item with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x34, bytes([0x3D, 0x7B, 0x22, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x38, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x40, NOP)

    # Post Clank Button
    address = addresses.POST_CLANK_BUTTON_FUNC
    # Disable hard checkpoint at Heli-Pack tutorial when reloading the planet
    patch.write_token(APTokenTypes.WRITE, address + 0x210, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x26C, NOP)
    # Disable failsafe that can give or remove Clank items when landing on planet
    patch.write_token(APTokenTypes.WRITE, address + 0x278, bytes([0x00 for _ in range(14 * 4)]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1EC, NOP)
    # Sub-function
    address = addresses.FREE_RATCHET_FUNC
    # Prevent Clank from being enabled
    patch.write_token(APTokenTypes.WRITE, address + 0x2C, NOP)
    # Prevent Heli-Pack and Thruster-Pack from being added to Primary Inventory
    patch.write_token(APTokenTypes.WRITE, address + 0x4C, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x64, NOP)

    """--------- 
    Barlow   
    ---------"""
    # Inventor
    address = addresses.INVENTOR_FUNC
    # Use Secondary Inventory slot instead Primary when checking to see if purchase has occurred
    patch.write_token(APTokenTypes.WRITE, address + 0x74, bytes([0x57, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x638, bytes([0x57, 0x7B, 0x42, 0x90]))
    # Replace code that calls give_item and equip_item with code that sets secondary inventory flag and only raises the
    # elevator if you have the Thermanator
    patch.write_token(APTokenTypes.WRITE, address + 0x67C, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x680, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x684, bytes([0x57, 0x7B, 0x44, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x688, bytes([0x1F, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x68C, bytes([0xDC, 0x09, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x690, bytes([0x2B, 0x00, 0x40, 0x10]))
    patch.write_token(APTokenTypes.WRITE, address + 0x694, bytes([0x33, 0x00, 0x05, 0x24]))

    # # Biker One
    # address = addresses.BIKER_ONE_FUNC
    # # Replace code that calls give_item and planet_unlock_message with code that just sets secondary inventory flag.
    # patch.write_token(APTokenTypes.WRITE, address + 0x240, bytes([0x1A, 0x00, 0x02, 0x3C]))
    # patch.write_token(APTokenTypes.WRITE, address + 0x244, bytes([0x01, 0x00, 0x04, 0x24]))
    # patch.write_token(APTokenTypes.WRITE, address + 0x248, bytes([0x60, 0x7B, 0x44, 0xA0]))

    # Prevent spawning at Gadgetron Inventor when Thermanator is collected.
    patch.write_token(APTokenTypes.WRITE, addresses.BARLOW_SPAWN_CONTROLLER_FUNC + 0x7C, NOP)
    # Don't skip ship landing cutscene.
    for address in addresses.PLANET_MAIN_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x284, NOP)

    """--------- 
    Notak 
    ---------"""
    # The planet unlock message for Ship Shack gets called in a unique way that we disable here.
    patch.write_token(APTokenTypes.WRITE, addresses.SECRET_MESSAGE_FUNC + 0x24, NOP)
    patch.write_token(APTokenTypes.WRITE, addresses.SECRET_MESSAGE_FUNC + 0x4C, NOP)

    """--------- 
    Siberius
    ---------"""
    # Change the forced ship travel after defeating the boss to go back to the Ship Shack instead of Tabora
    patch.write_token(APTokenTypes.WRITE, addresses.THIEF_FUNC + 0x880, bytes([0x18, 0x00, 0x04, 0x24]))

    """--------- 
    Tabora
    ---------"""
    # Prevent Planet Controller from spawning player at Glider.
    patch.write_token(APTokenTypes.WRITE, addresses.TABORA_CONTROLLER_FUNC + 0x380, bytes([0x59, 0x00, 0x00, 0x10]))

    # Wrench Pickup
    # Have Wrench pickup check a custom flag to determine if it has been checked.
    address = addresses.TABORA_CONTROLLER_FUNC
    upper_half, lower_half = MIPS.get_address_halves(ram.tabora_wrench_cutscene_flag)
    patch.write_token(APTokenTypes.WRITE, address + 0x1D4, bytes([
        *upper_half, 0x03, 0x3C,  # lui v1,...
        *lower_half, 0x62, 0x90,  # lbu v0,...(v1)
    ]))

    # Replace the code that upgrades wrench and displays a message by code that just sets a custom flag.
    # Also removes the wrench skin change + HUD message on pickup.
    patch.write_token(APTokenTypes.WRITE, address + 0x6C4, bytes([0x01, 0x00, 0x04, 0x24]))  # addiu a0,zero,0x1
    patch.write_token(APTokenTypes.WRITE, address + 0x6C8, upper_half + bytes([0x02, 0x3C]))  # lui v0,...
    patch.write_token(APTokenTypes.WRITE, address + 0x6CC, lower_half + bytes([0x44, 0xA0]))  # sb a0,...(v0)
    patch.write_token(APTokenTypes.WRITE, address + 0x6D0, NOP * 10)

    # Glider Pickup
    address = addresses.GLIDER_PICKUP_FUNC
    # Have Glider pickup check Secondary Inventory to determine if the Glider location has been checked.
    patch.write_token(APTokenTypes.WRITE, address + 0x58, bytes([0x45, 0x7B, 0x42, 0x90]))
    # Replace code that gives item and displays message with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x198, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x19C, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A0, bytes([0x45, 0x7B, 0x44, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A4, NOP)

    """--------- 
    Joba
    ---------"""
    # Biker Two
    address = addresses.BIKER_TWO_FUNC
    # Check Secondary Inventory to determine if the Charge Boots location has been checked.
    patch.write_token(APTokenTypes.WRITE, address + 0x60, bytes([0x66, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x228, bytes([0x66, 0x7B, 0x63, 0x90]))
    # Replace code that gives item, equips_item and displays message with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x234, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x238, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x23C, bytes([0x66, 0x7B, 0x44, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x248, NOP)

    # Shady Merchant
    address = addresses.SHADY_MERCHANT_FUNC
    # Check Secondary Inventory to determine if the Levitator has been purchased.
    patch.write_token(APTokenTypes.WRITE, address + 0x60, bytes([0x38, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x394, bytes([0x38, 0x7B, 0x42, 0x90]))
    # Replace code that gives item with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x3D8, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x3DC, bytes([0x48, 0x8B, 0x84, 0xA3]))
    # Prevent item unlocked popup message after cutscene
    patch.write_token(APTokenTypes.WRITE, address + 0x410, NOP)

    # Arena
    address = addresses.ARENA2_REWARD_FUNC
    # Replace code that gives / equips Gravity Boots with code that just sets Secondary Inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x64, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x68, bytes([0x53, 0x8B, 0x84, 0xA3]))
    patch.write_token(APTokenTypes.WRITE, address + 0x6C, NOP)
    # Replace code that gives Infiltrator with code that just sets Secondary Inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0xB4, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0xB8, bytes([0x73, 0x8B, 0x84, 0xA3]))
    # Only exit arena on back side if you have the Infiltrator
    patch.write_token(APTokenTypes.WRITE, addresses.ARENA2_EXIT_FUNC + 0x84, bytes([0x3B, 0x8B, 0x83, 0x93]))

    # Prevent spawning at the Infiltrator puzzle when entering the planet with the Infiltrator
    patch.write_token(APTokenTypes.WRITE, addresses.JOBA_CONTROLLER_FUNC + 0x108, NOP)

    """--------- 
    Todano
    ---------"""
    # Stuart Zurgo
    address = addresses.STUART_ZURGO_FUNC
    # Check Secondary Inventory to determine if the trade has been done.
    patch.write_token(APTokenTypes.WRITE, address + 0x60, bytes([0x37, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x39C, bytes([0x37, 0x7B, 0x42, 0x90]))
    # Don't remove Qwark Statuette from both main & secondary inventory when doing the trade.
    patch.write_token(APTokenTypes.WRITE, address + 0x3A8, NOP * 2)
    patch.write_token(APTokenTypes.WRITE, address + 0x3B4, NOP)
    # Replace code that gives Armor Magnetizer and displays message with code that just sets Secondary Inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x3B8, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x3BC, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x3C0, bytes([0x37, 0x7B, 0x44, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x3C4, NOP)

    # Sheepinator Pickup
    address = addresses.SHEEPINATOR_PICKUP_FUNC
    # Replace code that gives item, displays message and equips item with code that just sets secondary inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x138, bytes([0x1A, 0x00, 0x02, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x13C, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x140, bytes([0x40, 0x7B, 0x44, 0xA0]))
    patch.write_token(APTokenTypes.WRITE, address + 0x164, NOP)

    """--------- 
    Boldan
    ---------"""
    # Prevent getting automatically sent to Aranos Prison after the cutscene
    patch.write_token(APTokenTypes.WRITE, addresses.BOLDAN_CUTSCENE_TRIGGER_FUNC + 0x570, NOP)

    """--------- 
    Aranos Prison
    ---------"""
    # Planet Controller
    address = addresses.PRISON_CONTROLLER_FUNC
    # Stop planet from messing with Secondary Inventory when adding/removing Clank
    patch.write_token(APTokenTypes.WRITE, address + 0x18C, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x19C, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x100, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x110, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x610, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x62C, NOP)
    # Plumber
    address = addresses.PLUMBER_FUNC
    # Completely ignore check for presence of Armor Magnetizer
    patch.write_token(APTokenTypes.WRITE, address + 0x74, NOP)
    # Check Secondary Inventory to determine if the purchase has been done.
    patch.write_token(APTokenTypes.WRITE, address + 0x80, bytes([0x61, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x4BC, bytes([0x61, 0x7B, 0x42, 0x90]))
    # Just set Secondary Inventory flag when you make the purchase.
    patch.write_token(APTokenTypes.WRITE, address + 0x4D4, NOP)

    # Wrench Pickup
    # Have Wrench pickup check a custom flag to determine if it has been checked.
    address = addresses.PRISON_WRENCH_INIT_FUNC
    upper_half, lower_half = MIPS.get_address_halves(ram.aranos_wrench_cutscene_flag)
    wrench_pickup_condition = upper_half + bytes([0x03, 0x3C])  # lui v1,0x1A
    wrench_pickup_condition += lower_half + bytes([0x62, 0x90])  # lbu v0,0x-4D18(v1)
    wrench_pickup_condition += NOP * 8
    # The same patch is applied at two different spots, for two different wrench mobies that apply on different
    # circumstances (depending on the current level of your wrench)
    patch.write_token(APTokenTypes.WRITE, address + 0x84, wrench_pickup_condition)
    patch.write_token(APTokenTypes.WRITE, address + 0x12C, wrench_pickup_condition)

    # Replace the code that upgrades wrench and displays a message by code that just sets a custom flag.
    # Also removes the wrench skin change + HUD message on pickup.
    patch.write_token(APTokenTypes.WRITE, address + 0x1F8, bytes([0x01, 0x00, 0x04, 0x24]))  # addiu a0,zero,0x1
    patch.write_token(APTokenTypes.WRITE, address + 0x1FC, upper_half + bytes([0x02, 0x3C]))  # lui v0,...
    patch.write_token(APTokenTypes.WRITE, address + 0x200, lower_half + bytes([0x44, 0xA0]))  # sb a0,...(v0)
    patch.write_token(APTokenTypes.WRITE, address + 0x204, NOP * 9)

    """--------- 
    Damosel
    ---------"""
    # Planet Controller
    address = addresses.DAMOSEL_CONTROLLER_FUNC
    # Prevent forced spawn at Hypnotist
    patch.write_token(APTokenTypes.WRITE, address + 0x228, bytes([0x15, 0x00, 0x00, 0x10]))
    # Check Secondary Inventory to determine if the Mapper location has been checked.
    patch.write_token(APTokenTypes.WRITE, address + 0x38C, bytes([0x35, 0x7B, 0x42, 0x90]))
    # Replace code that gives Mapper with code that just sets Secondary Inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x3A8, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x3AC, bytes([0x45, 0x8B, 0x84, 0xA3]))
    # Prevent Mapper auto equip and unlocked popup message after cutscene
    patch.write_token(APTokenTypes.WRITE, address + 0x3B0, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x3BC, NOP)

    # Allow Hypnomatic part to spawn even if the Hypnomatic has already been collected.
    patch.write_token(APTokenTypes.WRITE, addresses.HYPNOMATIC_PART2_FUNC + 0x70, NOP)

    # Hypnotist
    address = addresses.HYPNOTIST_FUNC
    # Check Secondary Inventory to determine if the purchase has occurred.
    patch.write_token(APTokenTypes.WRITE, address + 0x60, bytes([0x67, 0x7B, 0x42, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x440, bytes([0x67, 0x7B, 0x63, 0x90]))
    # Make Hypnotist check AP controlled Hypnomatic Part Count
    # instead of normal address to determine total parts collected.
    patch.write_token(APTokenTypes.WRITE, address + 0x19C, bytes([0x1A, 0x00, 0x03, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A0, bytes([0xE6, 0xB2, 0x62, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A4, bytes([0x03, 0x00, 0x42, 0x28]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1A8, bytes([0x14, 0x00, 0x40, 0x14]))
    patch.write_token(APTokenTypes.WRITE, address + 0x1AC, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x1B0, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x1B4, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x1B8, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x1BC, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x218, bytes([0x1A, 0x00, 0x03, 0x3C]))
    patch.write_token(APTokenTypes.WRITE, address + 0x21C, bytes([0xE6, 0xB2, 0x62, 0x90]))
    patch.write_token(APTokenTypes.WRITE, address + 0x220, bytes([0xD9, 0x27, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x224, bytes([0xFF, 0xFF, 0x06, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x228, bytes([0x03, 0x00, 0x03, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x22C, bytes([0x22, 0x28, 0x62, 0x00]))
    patch.write_token(APTokenTypes.WRITE, address + 0x230, bytes([0x24, 0x00, 0x00, 0x10]))
    # Replace code that gives Hypnomatic with code that just sets Secondary Inventory flag.
    patch.write_token(APTokenTypes.WRITE, address + 0x4A0, bytes([0x01, 0x00, 0x04, 0x24]))
    patch.write_token(APTokenTypes.WRITE, address + 0x4A4, bytes([0x77, 0x8B, 0x84, 0xA3]))
    # Prevent Hypnomatic auto equip and unlocked popup message after cutscene
    patch.write_token(APTokenTypes.WRITE, address + 0x4A8, NOP)
    patch.write_token(APTokenTypes.WRITE, address + 0x4F0, NOP)

    patch.write_file("token_data.bin", patch.get_token_binary())


def custom_main_loop(ram: RamAddresses.Addresses, planet: PlanetAddresses) -> bytes:
    func = bytes()

    upper_half, lower_half = MIPS.get_address_halves(ram.custom_text_notification_trigger)
    text_id_to_display = TextManager.RESERVED_HUD_NOTIFICATION_TEXT_ID.to_bytes(2, 'little')

    # Store return address on the stack
    func += bytes([0xF8, 0xFF, 0xBD, 0x27])   # addiu sp,sp,-0x8
    func += bytes([0x00, 0x00, 0xBF, 0xFF])   # sd ra,(sp)

    # Read some custom variable managed by the client, and display a message if it is non-zero
    func += upper_half + bytes([0x04, 0x3C])  # lui a0,0x001a
    func += lower_half + bytes([0x84, 0x90])  # _lbu a0,-0x4D17(a0)
    func += bytes([0x06, 0x00, 0x80, 0x10])   # beq a0,zero,0x6
    func += MIPS.nop()

    func += text_id_to_display + bytes([0x04, 0x24])   # li a0,<TEXT_ID>
    func += MIPS.jal(planet.display_skill_point_message_func)
    func += bytes([0xff, 0xff, 0x05, 0x24])   # li a1,-0x1
    func += upper_half + bytes([0x04, 0x3C])  # lui a0,0x001a
    func += lower_half + bytes([0x80, 0xA0])  # _sb zero,-0x4D17(a0)

    # Load back return address from stack, then return
    func += bytes([0x00, 0x00, 0xBF, 0xDF])   # ld ra,(sp)
    func += MIPS.jr_ra()
    func += bytes([0x08, 0x00, 0xBD, 0x27])   # _addiu sp,sp,0x08

    # The chunk looks like it's way more than 0x800 bytes of contiguous code, but the precise count and the consistency
    # of that contiguity between planets would need to be proven, so let's use that "small" space until we need more.
    assert len(func) < 0x800, "Injected code might exceed Space-ish Wars code cave size"

    return func


def patch_free_challenge_selection(patch: Rac2ProcedurePatch, addresses: IsoAddresses):
    # Make Maktar arena challenges selectable
    address = addresses.MAKTAR_ARENA_MENU_FUNC
    patch.write_token(APTokenTypes.WRITE, address + 0xDC, NOP)  # Enable pressing right
    patch.write_token(APTokenTypes.WRITE, address + 0x204, NOP)  # Enable pressing left
    patch.write_token(APTokenTypes.WRITE, address + 0x348, NOP * 2)  # Enable starting a challenge without requirements
    patch.write_token(APTokenTypes.WRITE, addresses.MAKTAR_ARENA_DISPLAY_PREV_FUNC + 0x290, NOP)  # Display "previous"
    patch.write_token(APTokenTypes.WRITE, addresses.MAKTAR_ARENA_DISPLAY_NEXT_FUNC + 0x324, NOP)  # Display "next"

    # Make Joba arena challenges selectable
    address = addresses.JOBA_ARENA_MENU_FUNC
    patch.write_token(APTokenTypes.WRITE, address + 0xDC, NOP)  # Enable pressing right
    patch.write_token(APTokenTypes.WRITE, address + 0x1CC, NOP)  # Enable pressing left
    patch.write_token(APTokenTypes.WRITE, address + 0x2F0, NOP * 2)  # Enable starting a challenge without requirements
    patch.write_token(APTokenTypes.WRITE, addresses.JOBA_ARENA_DISPLAY_PREV_FUNC + 0x288, NOP)  # Display "previous"
    patch.write_token(APTokenTypes.WRITE, addresses.JOBA_ARENA_DISPLAY_NEXT_FUNC + 0x364, NOP)  # Display "next"

    # Show spaceship challenge as unlocked without winning the previous one
    for address in addresses.SPACESHIP_MENU_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x58C, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x790, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x7A0, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x914, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x924, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x934, NOP)
    # Enable starting spaceship challenge without winning the previous one
    for address in addresses.START_SPACESHIP_CHALLENGE_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x134, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x144, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x150, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x160, NOP)
        patch.write_token(APTokenTypes.WRITE, address + 0x170, NOP)

    # Show hoverbike race as unlocked without winning previous one
    for address in addresses.HOVERBIKE_MENU_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x5D0, NOP)
    # Allow starting hoverbike race without winning previous one
    for address in addresses.START_HOVERBIKE_CHALLENGE_FUNCS:
        patch.write_token(APTokenTypes.WRITE, address + 0x214, NOP)


def alter_nanotech_xp_tables(patch: Rac2ProcedurePatch, addresses: IsoAddresses, mult_percent: int):
    DEFAULT_NANO_XP_TABLE: list[int] = [
        0x00B4, 0x00D2, 0x00F0, 0x010E, 0x012C, 0x014A, 0x0168, 0x0186,
        0x01A4, 0x01C2, 0x01E0, 0x01F4, 0x0208, 0x0208, 0x0208, 0x0208,
        0x0208, 0x0208, 0x0208, 0x0208, 0x0208, 0x0212, 0x0212, 0x0230,
        0x0244, 0x0258, 0x026C, 0x0280, 0x0294, 0x02A8, 0x02BC, 0x02D0,
        0x02E4, 0x02F8, 0x030C, 0x0320, 0x0348, 0x032A, 0x03B1, 0x0438,
        0x04BF, 0x0546, 0x05CD, 0x0654, 0x06DB, 0x0762, 0x07E9, 0x0870,
        0x08CA, 0x0924, 0x0924, 0x0924, 0x0924, 0x0924, 0x0924, 0x0924,
        0x0924, 0x0924, 0x0951, 0x09AB, 0x09D8, 0x0A32, 0x0A8C, 0x0AE6,
        0x0B40, 0x0BB8
    ]
    # Multiplier given as input is meant to represent gained XP, while this table represents required XP to level up.
    # Therefore, we need to use the multiplicative inverse of that mult to get the factor we need to apply to this
    # table to mimic the effect of gained XP increase / decrease.
    factor = 1.0 / (mult_percent * 0.01)
    nanotech_xp_table = [int(x * factor) for x in DEFAULT_NANO_XP_TABLE]
    for address in addresses.NANOTECH_XP_TABLES:
        for xp_amount in nanotech_xp_table:
            patch.write_token(APTokenTypes.WRITE, address + 0x4, xp_amount.to_bytes(2, 'little'))
            address += 0x4


def alter_weapon_xp_tables(patch: Rac2ProcedurePatch, addresses: IsoAddresses, mult_percent: int):
    # None values are either 0x0000 or 0xFFFF and must be left as-is
    DEFAULT_WEAPON_XP_TABLE: list[int] = [
        None,   None,   None,   None,   None,   None,   None,   None,
        None,   0x09C4, None,   None,   None,   None,   None,   None,
        0x0384, None,   None,   None,   None,   None,   0x0190, 0x0096,
        0x041A, 0x0DAC, 0x02EE, 0x0FA0, 0x0834, 0x0578, 0x0118, 0x04B0,
        0x03E8, None,   0x2710, None,   None,   0x06A4, None,   None,
        0x2710, 0x02EE, 0x00C8, None,   None,   0x01C2, None,   None,
        None,   None,   None,   None,   None,   None,   None,   None,
        None,   None,   None,   None,   None,   None,   None,   None,
        None,   None,   None,   None,   None,   None,   None,   None,
        None,   None,   None,   None,   None,   None,   None,   0x1F40,
        None,   0x2EE0, None,   0x1388, None,   0x2968, None,   0x1130,
        None,   0x1770, None,   0x1B58, None,   0x0FA0, None,   0x0FA0,
        None,   0x1388, None,   0x1F40, None,   0x1F40, None,   0x2710,
        None,   0x1F40, None,   0x1770, None,   0x1388
    ]
    # Multiplier given as input is meant to represent gained XP, while this table represents required XP to level up.
    # Therefore, we need to use the multiplicative inverse of that mult to get the factor we need to apply to this
    # table to mimic the effect of gained XP increase / decrease.
    factor = 1.0 / (mult_percent * 0.01)
    weapon_xp_table = [int(x * factor) if x is not None else None for x in DEFAULT_WEAPON_XP_TABLE]
    for address in addresses.WEAPON_DATA_TABLES:
        for xp_amount in weapon_xp_table:
            if xp_amount is not None:
                patch.write_token(APTokenTypes.WRITE, address + 0x6C, xp_amount.to_bytes(2, 'little'))
            address += 0xE0


def get_version_from_iso(iso_path: str) -> str:
    with open(iso_path, "rb") as file:
        file.seek(0x828F5)
        return file.read(11).decode()
