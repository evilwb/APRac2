import array
import dataclasses
import struct
import textwrap
from dataclasses import dataclass, field
from time import sleep
from logging import Logger
from enum import Enum, IntEnum
from typing import Optional, List

from .Items import ItemData, item_table, ItemName, equipment_table, planet_coord_table, CLANK_PACKS, QUICK_SELECTABLE
from .Addresses import Addresses
import pcsx2_interface

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
        pcsx2_interface.write_bytes(self.address + 0x10, struct.pack("<f", self.x))
        pcsx2_interface.write_bytes(self.address + 0x14, struct.pack("<f", self.y))
        pcsx2_interface.write_bytes(self.address + 0x18, struct.pack("<f", self.z))
        pcsx2_interface.write_int8(self.address + 0x20, self.state)
        pcsx2_interface.write_int8(self.address + 0x21, self.group)
        pcsx2_interface.write_int8(self.address + 0x22, self.moby_class)
        pcsx2_interface.write_int8(self.address + 0x23, self.alpha)
        pcsx2_interface.write_int32(self.address + 0x24, self.class_address)
        pcsx2_interface.write_int32(self.address + 0x28, self.chain_address)
        pcsx2_interface.write_bytes(self.address + 0x2C, struct.pack("<f", self.scale))
        pcsx2_interface.write_int8(self.address + 0x31, self.is_drawn)
        pcsx2_interface.write_int16(self.address + 0x32, self.draw_distance)
        pcsx2_interface.write_int16(self.address + 0x34, self.flags1)
        pcsx2_interface.write_int16(self.address + 0x36, self.flags2)
        pcsx2_interface.write_bytes(self.address + 0x38, struct.pack("<f", self.lighting))
        pcsx2_interface.write_int8(self.address + 0x3C, self.red)
        pcsx2_interface.write_int8(self.address + 0x3D, self.green)
        pcsx2_interface.write_int8(self.address + 0x3E, self.blue)
        pcsx2_interface.write_int8(self.address + 0x3F, self.shine)
        pcsx2_interface.write_int32(self.address + 0x64, self.update_function_address)
        pcsx2_interface.write_int32(self.address + 0x68, self.pvars_address)
        pcsx2_interface.write_int32(self.address + 0x98, self.colldata_address)
        pcsx2_interface.write_int16(self.address + 0xAA, self.oclass)
        pcsx2_interface.write_int16(self.address + 0xB2, self.uid)

    def get_pvar(self, offset: int, size: int) -> bytes:
        return pcsx2_interface.read_bytes(self.pvars_address + offset, size)

    def set_pvar(self, offset: int, value: bytes):
        pcsx2_interface.write_bytes(self.pvars_address + offset, value)


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


class InventoryItemData(ItemData):
    """Class used to track the player's current items and their quantities"""
    current_amount: int
    current_capacity: int

    def __init__(self, item_data: ItemData, current_amount: int, current_capacity: int) -> None:
        super().__init__(item_data.name, item_data.id, item_data.offset,
                         item_data.classification, item_data.max_capacity)
        self.current_amount = current_amount
        self.current_capacity = current_capacity


class Rac2Interface:
    """Interface sitting in front of the pcsx2_interface to provide higher level functions for interacting with RAC2"""
    pcsx2_interface: pcsx2_interface = pcsx2_interface
    addresses: Addresses = None
    connection_status: str
    logger: Logger
    _previous_message_size: int = 0
    game_id_error: str = None
    game_rev_error: int = None
    current_game: Optional[str] = None

    def __init__(self, logger) -> None:
        self.logger = logger

    def give_item_to_player(self, item: ItemData, new_amount: int = 1, new_capacity: int = 1):
        """Gives the player an item with the specified amount and capacity"""
        assert 0 <= new_amount <= item.max_capacity
        assert item.name in item_table.keys()

        if item.name in equipment_table.keys():
            self.pcsx2_interface.write_int8(self.addresses.inventory + item.offset, new_amount)
            if item.name in CLANK_PACKS:
                owned_items = [key for key, value in self.get_current_inventory().items() if value.current_amount == 1]
                has_clank = any(item in owned_items for item in CLANK_PACKS)
                self.pcsx2_interface.write_int8(self.addresses.clank_disabled, not has_clank)
            if item.name in QUICK_SELECTABLE:
                self.add_to_quickselect(item.id) if new_amount == 1 else self.remove_from_quickselect(item.id)

        if item.name in planet_coord_table.keys():
            planet_list = []
            for list_idx in range(PLANET_LIST_SIZE):
                planet_id = self.pcsx2_interface.read_int32(self.addresses.selectable_planets + 4 * list_idx)
                if planet_id:
                    planet_list.append(planet_id)
            if Rac2Planet.Ship_Shack not in planet_list:
                planet_list.insert(0, Rac2Planet.Ship_Shack)
            if new_amount > 0:
                planet_list.append(item.offset)
            else:
                planet_list = [i for i in planet_list if i != item.offset]
            for list_idx in range(PLANET_LIST_SIZE):
                try:
                    id_to_write = planet_list[list_idx]
                except IndexError:
                    id_to_write = 0
                self.pcsx2_interface.write_int32(self.addresses.selectable_planets + 4 * list_idx, id_to_write)

        if item.name == ItemName.Platinum_Bolt:
            pcsx2_interface.write_int8(self.addresses.platinum_bolt_count, new_amount)

        if item.name == ItemName.Nanotech_Boost:
            pcsx2_interface.write_int8(self.addresses.nanotech_boost_count, new_amount)

        if item.name == ItemName.Hypnomatic_Part:
            pcsx2_interface.write_int8(self.addresses.hypnomatic_part_count, new_amount)

        # TODO: Deal with armor and weapons

    def get_inventory_item(self, item: ItemData) -> Optional[InventoryItemData]:
        assert item.name in item_table.keys()

        if item.name in equipment_table.keys():
            result = self.pcsx2_interface.read_int8(self.addresses.inventory + item.offset)
            return InventoryItemData(item, result, 1)
        if item.name in planet_coord_table.keys():
            planet_list = []
            for list_idx in range(PLANET_LIST_SIZE):
                planet_id = self.pcsx2_interface.read_int32(self.addresses.selectable_planets + 4 * list_idx)
                if planet_id:
                    planet_list.append(planet_id)
            return InventoryItemData(item, item.offset in planet_list, 1)
        if item.name == ItemName.Platinum_Bolt:
            total_bolts = pcsx2_interface.read_int8(self.addresses.platinum_bolt_count)
            return InventoryItemData(item, total_bolts, item.max_capacity)
        if item.name == ItemName.Nanotech_Boost:
            total_boosts = pcsx2_interface.read_int8(self.addresses.nanotech_boost_count)
            return InventoryItemData(item, total_boosts, item.max_capacity)
        if item.name == ItemName.Hypnomatic_Part:
            part_count = self.pcsx2_interface.read_int8(self.addresses.hypnomatic_part_count)
            return InventoryItemData(item, part_count, item.max_capacity)

    def get_current_inventory(self) -> dict[str, InventoryItemData]:
        inventory: dict[str, InventoryItemData] = {}
        for item in item_table.values():
            inventory[item.name] = self.get_inventory_item(item)
        return inventory

    def get_alive(self) -> bool:
        nanotech = self.pcsx2_interface.read_int8(self.addresses.current_nanotech)
        return nanotech != 0

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
        memory = self.pcsx2_interface.read_bytes(self.addresses.current_planet, 4)
        planet_id = int.from_bytes(memory, "little", signed=True)
        return planet_by_id(planet_id)

    def get_pause_state(self) -> int:
        address = self.addresses.pause_state
        if self.get_current_planet() is Rac2Planet.Oozla:
            address = self.addresses.oozla_pause_state
        return pcsx2_interface.read_int8(address)

    def get_ratchet_state(self) -> int:
        return pcsx2_interface.read_int8(self.addresses.ratchet_state)

    def get_current_nanotech(self) -> int:
        return self.pcsx2_interface.read_int8(self.addresses.current_nanotech)

    def set_current_nanotech(self, new_nanotech_amount: int):
        self.pcsx2_interface.write_int8(self.addresses.current_nanotech, new_nanotech_amount)
        return self.get_current_nanotech()

    def add_to_quickselect(self, item_id: int) -> bool:
        for i in range(8):
            if self.pcsx2_interface.read_int32(self.addresses.quickselect + i * 4) == 0:
                self.pcsx2_interface.write_int32(self.addresses.quickselect + i * 4, item_id)
                return True
        return False

    def remove_from_quickselect(self, item_id: int) -> bool:
        for i in range(8):
            if self.pcsx2_interface.read_int32(self.addresses.quickselect + i * 4) == item_id:
                self.pcsx2_interface.write_int32(self.addresses.quickselect + i * 4, 0)
                return True
        return False

    def connect_to_game(self):
        """Initializes the connection to PCSX2 and verifies it is connected to RAC2"""
        try:
            self.pcsx2_interface.connect()
            if not self.pcsx2_interface.is_connected():
                return
            self.logger.info("Connected to PCSX2 Emulator")
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
        except RuntimeError as e:
            pass

    def disconnect_from_game(self):
        self.pcsx2_interface.disconnect()
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

    def send_hud_message(self, message: str) -> bool:
        if (
            self.get_current_planet() == Rac2Planet.Title_Screen
            or self.get_pause_state() != 0
            or self.get_ratchet_state() == 97
        ):
            return False

        # for i in range(1, math.ceil(len(message) / HUD_MAX_MESSAGE_WIDTH)):
        #     message = message[:HUD_MAX_MESSAGE_WIDTH * i] + '\1' + message[HUD_MAX_MESSAGE_WIDTH * i:]
        message = "\1".join(textwrap.wrap(message, width=35, replace_whitespace=False, break_long_words=False))

        try:
            payload_message = message.encode() + b"\00"
            segments = self.get_segment_pointer_table()
            message_address = self.pcsx2_interface.find_first(b"You got a skill point!",
                                                              segments.help_messages, segments.tie_instances)

            # Overwrite from start of "You got a skill point!" text with payload message.
            overwritten_text = self.pcsx2_interface.read_bytes(message_address, len(payload_message))
            self.pcsx2_interface.write_bytes(message_address, payload_message)

            # Save original values for variables we use to trigger the text box.
            has_nice_ride = self.pcsx2_interface.read_int8(0x1A7A7D)
            ship_upgrades = self.pcsx2_interface.read_int16(0x1A7AF0)

            # Set variables to trigger skill point get text box.
            self.pcsx2_interface.write_int8(0x1A7A7D, 0)
            self.pcsx2_interface.write_int16(0x1A7AF0, 0xFF50)

            # After short delay, reset variables to original values.
            sleep(0.05)
            self.pcsx2_interface.write_int8(0x1A7A7D, has_nice_ride)
            self.pcsx2_interface.write_int16(0x1A7AF0, ship_upgrades)
            self.pcsx2_interface.write_bytes(message_address, overwritten_text)
        except RuntimeError:
            return False

        return True

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
        self.pcsx2_interface.write_bytes(self.addresses.ratchet_position, struct.pack("<f", x))
        self.pcsx2_interface.write_bytes(self.addresses.ratchet_position + 0x4, struct.pack("<f", y))
        self.pcsx2_interface.write_bytes(self.addresses.ratchet_position + 0x8, struct.pack("<f", z))

    def dump_memory(self, output_file: str):
        with open(output_file, "wb") as file:
            for i in range(512):
                file.write(self.pcsx2_interface.batch_read(i * 65536, (i + 1) * 65536))

    def read_instruction(self, address: int) -> int:
        return self.pcsx2_interface.read_int32(address)

    def write_instruction(self, address: int, instruction: int):
        self.pcsx2_interface.write_int32(address, instruction)

    def nop_instruction(self, address: int):
        self.write_instruction(address, 0x0)

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
