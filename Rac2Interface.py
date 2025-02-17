import array
import dataclasses
import struct
from dataclasses import dataclass, field
from logging import Logger
from enum import Enum, IntEnum
from typing import Optional, List, Dict

from .data import Items
from .data.RamAddresses import Addresses
from .data.Items import ItemData, EquipmentData, CoordData, CollectableData
from .pcsx2_interface.pine import Pine

_SUPPORTED_VERSIONS = ["SCUS-97268"]

HUD_MESSAGE_DURATION = 2.0
HUD_MAX_MESSAGE_WIDTH = 35

MOBY_SIZE = 0x100
MEMORY_SEGMENTS = 35
PLANET_LIST_SIZE = 25
INVENTORY_SIZE = 56
PLATINUM_BOLT_MAX = 40
NANOTECH_BOOST_MAX = 10


class ConnectionState(Enum):
    DISCONNECTED = 0
    IN_GAME = 1
    IN_MENU = 2


class Rac2Armor(Enum):
    Commando = 0
    Tetrafiber = 1
    Duraplate = 2
    Electrosteel = 3
    Carbonox = 4


class Rac2Planet(IntEnum):
    """Game planets with their corresponding IDs"""
    Title_Screen = -1
    Aranos_Tutorial = 0
    Oozla = 1
    Maktar_Nebula = 2
    Endako = 3
    Barlow = 4
    Feltzin_System = 5
    Notak = 6
    Siberius = 7
    Tabora = 8
    Dobbo = 9
    Hrugis_Cloud = 10
    Joba = 11
    Todano = 12
    Boldan = 13
    Aranos_Prison = 14
    Gorn = 15
    Snivelak = 16
    Smolg = 17
    Damosel = 18
    Grelbin = 19
    Yeedil = 20
    Dobbo_Orbit = 22
    Damosel_Orbit = 23
    Ship_Shack = 24
    Wupash_Nebula = 25
    Jamming_Array = 26
    Insomniac_Museum = 30


@dataclass
class MobyInstance:
    address: int
    x: float  # 0x10, 32 bits
    y: float  # 0x14, 32 bits
    z: float  # 0x18, 32 bits
    state: int  # 0x20, 8 bits
    group: int  # 0x21, 8 bits
    moby_class: int  # 0x22, 8 bits
    alpha: int  # 0x23, 8 bits
    class_address: int  # 0x24, 32 bits
    chain_address: int  # 0x28, 32 bits
    scale: float  # 0x2C, 32 bits
    is_drawn: bool  # 0x31, 8 bits
    draw_distance: int  # 0x32, 16 bits
    flags1: int  # 0x34, 16 bits
    flags2: int  # 0x36, 16 bits
    lighting: float  # 0x38, 32 bits
    red: int  # 0x3C, 8 bits
    green: int  # 0x3D, 8 bits
    blue: int  # 0x3E, 8 bits
    shine: int  # 0x3F, 8 bits
    update_function_address: int  # 0x64, 32 bits
    pvars_address: int  # 0x68, 32 bits
    colldata_address: int  # 0x98, 32 bits
    oclass: int  # 0xAA, 16 bits
    uid: int  # 0xB2, 16 bits

    def push(self):
        Rac2Interface.pcsx2_interface.write_float(self.address + 0x10, self.x)
        Rac2Interface.pcsx2_interface.write_float(self.address + 0x14, self.y)
        Rac2Interface.pcsx2_interface.write_float(self.address + 0x18, self.z)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x20, self.state)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x21, self.group)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x22, self.moby_class)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x23, self.alpha)
        Rac2Interface.pcsx2_interface.write_int32(self.address + 0x24, self.class_address)
        Rac2Interface.pcsx2_interface.write_int32(self.address + 0x28, self.chain_address)
        Rac2Interface.pcsx2_interface.write_float(self.address + 0x2C, self.scale)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x31, self.is_drawn)
        Rac2Interface.pcsx2_interface.write_int16(self.address + 0x32, self.draw_distance)
        Rac2Interface.pcsx2_interface.write_int16(self.address + 0x34, self.flags1)
        Rac2Interface.pcsx2_interface.write_int16(self.address + 0x36, self.flags2)
        Rac2Interface.pcsx2_interface.write_float(self.address + 0x38, self.lighting)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x3C, self.red)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x3D, self.green)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x3E, self.blue)
        Rac2Interface.pcsx2_interface.write_int8(self.address + 0x3F, self.shine)
        Rac2Interface.pcsx2_interface.write_int32(self.address + 0x64, self.update_function_address)
        Rac2Interface.pcsx2_interface.write_int32(self.address + 0x68, self.pvars_address)
        Rac2Interface.pcsx2_interface.write_int32(self.address + 0x98, self.colldata_address)
        Rac2Interface.pcsx2_interface.write_int16(self.address + 0xAA, self.oclass)
        Rac2Interface.pcsx2_interface.write_int16(self.address + 0xB2, self.uid)


@dataclass(frozen=True)
class MemorySegmentTable:
    kernel: int = field()
    code: int
    base: int
    tfrag_geometry: int
    occlusion: int
    sky: int
    collision: int
    shared_vram: int
    particle_vram: int
    effects_vram: int
    moby_classes: int
    ties: int
    shrubs: int
    ratchet_seqs: int
    help_messages: int
    tie_instances: int
    shrub_instances: int
    moby_instances: int
    moby_pvars: int
    misc_instances: int
    misc_instances_end: int
    hud: int
    gui: int

    @classmethod
    def from_list(cls, raw_table: List[int]):
        return cls(
            kernel=raw_table[0],
            code=raw_table[1],
            base=raw_table[2],
            tfrag_geometry=raw_table[7],
            occlusion=raw_table[8],
            sky=raw_table[9],
            collision=raw_table[10],
            shared_vram=raw_table[11],
            particle_vram=raw_table[12],
            effects_vram=raw_table[13],
            moby_classes=raw_table[14],
            ties=raw_table[15],
            shrubs=raw_table[16],
            ratchet_seqs=raw_table[17],
            help_messages=raw_table[19],
            tie_instances=raw_table[20],
            shrub_instances=raw_table[21],
            moby_instances=raw_table[22],
            moby_pvars=raw_table[23],
            misc_instances=raw_table[24],
            misc_instances_end=raw_table[25],
            hud=raw_table[31],
            gui=raw_table[32],
        )

    def __repr__(self):
        string: str = ""
        for f in dataclasses.fields(self):
            string += f"{f.name:<18}: 0x{getattr(self, f.name):0>8X}\n"
        return string


def planet_by_id(planet_id) -> Optional[Rac2Planet]:
    for world in Rac2Planet:
        if world.value == planet_id:
            return world
    return None


# class InventoryItemData(NamedTuple):
#     """Class used to track the player's current items and their quantities"""
#     item: ItemData
#     current_amount: int
#     current_capacity: int


class Rac2Interface:
    """Interface sitting in front of the pcsx2_interface to provide higher level functions for interacting with RAC2"""
    pcsx2_interface: Pine = Pine()
    addresses: Addresses = None
    connection_status: str
    logger: Logger
    _previous_message_size: int = 0
    game_id_error: str = None
    game_rev_error: int = None
    current_game: Optional[str] = None
    text_ids_cache: Dict[int, int] = {}

    def __init__(self, logger) -> None:
        self.logger = logger

    def give_equipment_to_player(self, equipment: EquipmentData):
        self.pcsx2_interface.write_int8(self.addresses.inventory + equipment.offset, 1)
        # TODO: Auto equip Thruster-Pack if you don't have Heli-Pack.
        if equipment in Items.QUICK_SELECTABLE:
            self.add_to_quickselect(equipment)

    def unlock_planet(self, planet_number: int):
        planet_list = []
        for list_idx in range(PLANET_LIST_SIZE):
            planet_id = self.pcsx2_interface.read_int32(self.addresses.selectable_planets + 4 * list_idx)
            if planet_id:
                planet_list.append(planet_id)
        if Rac2Planet.Ship_Shack not in planet_list:
            planet_list.insert(0, Rac2Planet.Ship_Shack)

        planet_list.append(planet_number)

        for list_idx in range(PLANET_LIST_SIZE):
            try:
                id_to_write = planet_list[list_idx]
            except IndexError:
                id_to_write = 0
            self.pcsx2_interface.write_int32(self.addresses.selectable_planets + 4 * list_idx, id_to_write)

    def give_collectable_to_player(self, item: CollectableData, new_amount: int):
        if item is Items.PLATINUM_BOLT:
            self.pcsx2_interface.write_int8(self.addresses.platinum_bolt_count, new_amount)

        if item is Items.NANOTECH_BOOST:
            self.pcsx2_interface.write_int8(self.addresses.nanotech_boost_count, new_amount)

        if item is Items.HYPNOMATIC_PART:
            self.pcsx2_interface.write_int8(self.addresses.hypnomatic_part_count, new_amount)

    # TODO: Deal with armor and weapons

    def count_inventory_item(self, item: ItemData) -> int:
        if isinstance(item, EquipmentData):
            return self.pcsx2_interface.read_int8(self.addresses.inventory + item.offset)
        if isinstance(item, CoordData):
            planet_list = []
            for list_idx in range(PLANET_LIST_SIZE):
                planet_id = self.pcsx2_interface.read_int32(self.addresses.selectable_planets + 4 * list_idx)
                if planet_id:
                    planet_list.append(planet_id)
            return int(item.planet_number in planet_list)
        if item is Items.PLATINUM_BOLT:
            return self.pcsx2_interface.read_int8(self.addresses.platinum_bolt_count)
        if item is Items.NANOTECH_BOOST:
            return self.pcsx2_interface.read_int8(self.addresses.nanotech_boost_count)
        if item is Items.HYPNOMATIC_PART:
            return self.pcsx2_interface.read_int8(self.addresses.hypnomatic_part_count)

    def get_current_inventory(self) -> dict[str, int]:
        inventory: dict[str, int] = {}
        for item in Items.ALL:
            inventory[item.name] = self.count_inventory_item(item)
        return inventory

    def get_wrench_level(self) -> int:
        wrench_id = self.pcsx2_interface.read_int8(self.addresses.wrench_weapon_id)
        if wrench_id == 0x4A:
            return 1
        elif wrench_id == 0x4B:
            return 2
        return 0

    def set_wrench_level(self, level: int):
        try:
            wrench_id = 0x0A
            if level == 1:
                wrench_id = 0x4A
            elif level == 2:
                wrench_id = 0x4B
            self.pcsx2_interface.write_int8(self.addresses.wrench_weapon_id, wrench_id)
            return True
        except RuntimeError:
            return False

    def get_armor_level(self) -> int:
        return self.pcsx2_interface.read_int8(self.addresses.current_armor_level)

    def set_armor_level(self, level: int):
        try:
            self.pcsx2_interface.write_int8(self.addresses.current_armor_level, level)
            return True
        except RuntimeError:
            return False

    def get_alive(self) -> bool:
        planet = self.get_current_planet()
        if planet in [Rac2Planet.Wupash_Nebula, Rac2Planet.Feltzin_System, Rac2Planet.Hrugis_Cloud, Rac2Planet.Gorn]:
            return self.pcsx2_interface.read_int8(self.addresses.planet[planet].camara_state) != 6
        elif planet in [Rac2Planet.Dobbo_Orbit, Rac2Planet.Damosel_Orbit]:
            return self.pcsx2_interface.read_int8(self.addresses.ratchet_state) != 95
        else:
            if (self.pcsx2_interface.read_int8(self.addresses.current_nanotech) == 0
                    or self.pcsx2_interface.read_int8(self.addresses.ratchet_state) == 116
                    or self.pcsx2_interface.read_int8(self.addresses.ratchet_state) == 145):
                return False
            else:
                return True

    def kill_player(self) -> None:
        planet = self.get_current_planet()
        # Kill Ship
        if planet in [Rac2Planet.Wupash_Nebula, Rac2Planet.Feltzin_System, Rac2Planet.Hrugis_Cloud, Rac2Planet.Gorn]:
            self.pcsx2_interface.write_int8(self.addresses.planet[planet].camara_state, 6)
        # Kill Giant Clank
        elif planet in [Rac2Planet.Dobbo_Orbit, Rac2Planet.Damosel_Orbit]:
            self.pcsx2_interface.write_int8(self.addresses.ratchet_state, 95)
        # Kill Receiver Bot
        elif self.get_ratchet_state() > 140:
            current_moby = self.pcsx2_interface.read_int32(self.addresses.current_moby_instance_pointer)
            pvars = self.pcsx2_interface.read_int32(current_moby + 0x68)
            self.pcsx2_interface.write_int16(pvars + 0x3BC, 0)
        # Kill Ratchet
        else:
            self.set_nanotech(0)

    def set_nanotech(self, new_value) -> None:
        if not (0 <= new_value <= 0xFF):
            return
        self.pcsx2_interface.write_int8(self.addresses.current_nanotech, new_value)

    def switch_planet(self, new_planet: Rac2Planet) -> bool:
        current_planet = self.get_current_planet()
        trigger_address = self.addresses.planet[current_planet].planet_switch_trigger
        next_planet_address = self.addresses.planet[current_planet].next_planet
        if not (trigger_address and next_planet_address):
            return False

        try:
            self.pcsx2_interface.write_int32(trigger_address, 1)
            self.pcsx2_interface.write_int32(next_planet_address, new_planet)
        except RuntimeError:
            return False

        return True

    def get_current_planet(self) -> Rac2Planet:
        """Returns the planet that the player is currently on"""
        planet_id = self.pcsx2_interface.read_int32(self.addresses.current_planet)
        return planet_by_id(planet_id)

    def get_pause_state(self) -> int:
        address = self.addresses.pause_state
        if self.get_current_planet() is Rac2Planet.Oozla:
            address = self.addresses.oozla_pause_state
        return self.pcsx2_interface.read_int8(address)

    def get_ratchet_state(self) -> int:
        return self.pcsx2_interface.read_int8(self.addresses.ratchet_state)

    def get_current_nanotech(self) -> int:
        return self.pcsx2_interface.read_int8(self.addresses.current_nanotech)

    def set_current_nanotech(self, new_nanotech_amount: int):
        self.pcsx2_interface.write_int8(self.addresses.current_nanotech, new_nanotech_amount)
        return self.get_current_nanotech()

    def add_to_quickselect(self, equipment: EquipmentData) -> bool:
        for i in range(8):
            if self.pcsx2_interface.read_int32(self.addresses.quickselect + i * 4) == 0:
                self.pcsx2_interface.write_int32(self.addresses.quickselect + i * 4, equipment.offset)
                return True
        return False

    def remove_from_quickselect(self, equipment: EquipmentData) -> bool:
        for i in range(8):
            if self.pcsx2_interface.read_int32(self.addresses.quickselect + i * 4) == equipment.offset:
                self.pcsx2_interface.write_int32(self.addresses.quickselect + i * 4, 0)
                return True
        return False

    def connect_to_game(self):
        """Initializes the connection to PCSX2 and verifies it is connected to RAC2"""
        if not self.pcsx2_interface.is_connected():
            self.pcsx2_interface.connect()
            if not self.pcsx2_interface.is_connected():
                return
            self.logger.info("Connected to PCSX2 Emulator")
        try:
            game_id = self.pcsx2_interface.get_game_id()
            # The first read of the address will be null if the client is faster than the emulator
            self.current_game = None
            if game_id in _SUPPORTED_VERSIONS:
                self.current_game = game_id
                self.addresses = Addresses(game_id)
            if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
                self.logger.warning(
                    f"Connected to the wrong game ({game_id}, "
                    f"please connect to Ratchet & Clank 2 (Game ID starts with a SCUS-)")
                self.game_id_error = game_id
        except RuntimeError:
            pass
        except ConnectionError:
            pass

    def disconnect_from_game(self):
        self.pcsx2_interface.disconnect()
        self.current_game = None
        self.logger.info("Disconnected from PCSX2 Emulator")

    def get_connection_state(self) -> bool:
        try:
            connected = self.pcsx2_interface.is_connected()
            if not connected or self.current_game is None:
                return False
            else:
                return True
        except RuntimeError:
            return False

    def is_loading(self) -> bool:
        return not self.pcsx2_interface.read_int8(self.addresses.loaded_flag)

    def get_moby(self, uid: int) -> Optional[MobyInstance]:
        address = self.get_segment_pointer_table().moby_instances
        uid_offset = 0xB2
        for _ in range(self.get_segment_pointer_table().moby_instances, self.get_segment_pointer_table().moby_pvars):
            if self.pcsx2_interface.read_int16(address + uid_offset) == uid:
                moby_data = struct.unpack("<16xfff4xBBBBIIfx?HHHIBBBB36xII44xI14xH6xH76x",
                                          self.pcsx2_interface.read_bytes(address, MOBY_SIZE))
                return MobyInstance(*((address,) + moby_data))
            address += MOBY_SIZE

        return None

    def get_update_function(self, oclass: int) -> Optional[int]:
        oclass_offset = 0xAA
        update_function_offset = 0x64
        segments = self.get_segment_pointer_table()
        if not segments:
            return None
        for address in range(segments.moby_instances, segments.moby_pvars, MOBY_SIZE):
            if self.pcsx2_interface.read_int16(address + oclass_offset) == oclass:
                return self.pcsx2_interface.read_int32(address + update_function_offset)
        return None

    def move_ratchet(self, x: float, y: float, z: float):
        self.pcsx2_interface.write_float(self.addresses.ratchet_position, x)
        self.pcsx2_interface.write_float(self.addresses.ratchet_position + 0x4, y)
        self.pcsx2_interface.write_float(self.addresses.ratchet_position + 0x8, z)

    def read_instruction(self, address: int) -> int:
        return self.pcsx2_interface.read_int32(address)

    def write_instruction(self, address: int, instruction: int):
        self.pcsx2_interface.write_int32(address, instruction)

    def nop_instruction(self, address: int):
        self.write_instruction(address, 0x0)

    def get_text_offset_addr(self, text_id: int) -> Optional[int]:
        text_address_table = self.get_segment_pointer_table().help_messages

        # If text segment starts with "WAD", it means the game is currently performing a light reload
        # (e.g. after a death) and writing over this data would most likely crash the game.
        header = self.pcsx2_interface.read_int32(text_address_table)
        if header & 0x00FFFFFF == 0x444157:  # "WAD"
            return None

        # Since the order of text IDs is always the same in the table for a given version of the game, we store the
        # position of each text ID we encounter to avoid looping over that table ever again.
        if text_id in self.text_ids_cache:
            offset_addr = text_address_table + self.text_ids_cache[text_id] * 0x10
            found_text_id = self.pcsx2_interface.read_int32(offset_addr + 0x4)
            if found_text_id == text_id:
                return offset_addr
            # When changing planets, offsets can slightly shift for some reason: invalidate the cache
            self.text_ids_cache.clear()

        # Perform a lookup on the text offsets table to know the address of the string referenced by the given text ID
        # Cache all offsets in this table inside the dictionary to not have to perform that lookup next time.
        i = 0
        while True:
            current_text_id = self.pcsx2_interface.read_int32(text_address_table + i * 0x10 + 0x4)
            self.text_ids_cache[current_text_id] = i
            if current_text_id > 0x2000000:
                return None
            if current_text_id == text_id:
                return text_address_table + i * 0x10
            i += 1

    def get_text_address(self, text_id: int) -> Optional[int]:
        offset_addr = self.get_text_offset_addr(text_id)
        if offset_addr:
            return self.pcsx2_interface.read_int32(offset_addr)
        return None

    def set_text_address(self, text_id: int, addr: int) -> bool:
        offset_addr = self.get_text_offset_addr(text_id)
        if offset_addr:
            self.pcsx2_interface.write_int32(offset_addr, addr)
            return True
        return False

    def can_trigger_hud_notification(self):
        return (self.get_current_planet() != Rac2Planet.Title_Screen
                and self.get_pause_state() == 0
                and self.get_ratchet_state() != 97)

    def trigger_hud_notification_display(self):
        try:
            # Overwrite from start of "You got a skill point!" text with payload message.
            self.pcsx2_interface.write_int8(self.addresses.custom_text_notification_trigger, 0x01)
            return True
        except RuntimeError:
            return False

    def get_segment_pointer_table(self) -> Optional[MemorySegmentTable]:
        if self.addresses is None:
            return None

        table_base_address = self.addresses.planet[self.get_current_planet().value].segment_pointers
        if table_base_address is None:
            return None

        try:
            table_bytes = self.pcsx2_interface.read_bytes(table_base_address, MEMORY_SEGMENTS * 4)
        except ValueError:
            return None

        return MemorySegmentTable.from_list(array.array('I', table_bytes).tolist())
