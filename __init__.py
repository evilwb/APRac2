# Setup local dependencies if running in an apworld
from .data.Planets import Planet, PlanetData, planets

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
import settings
from worlds.AutoWorld import World, WebWorld
from .Regions import create_regions
from .Locations import every_location, LocationName
from .Rac2Options import Rac2Options
from .Items import Rac2Item, ItemName, equipment_table, item_table
from .Container import Rac2ProcedurePatch, generate_patch
from BaseClasses import Item, Tutorial, ItemClassification
import typing
import os
from typing import Dict, Optional


def run_client(url: Optional[str] = None):
    from .Rac2Client import launch
    launch_subprocess(launch, name="Rac2Client")


components.append(
    Component("Ratchet & Clank 2 Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".aprac2"))
)


class Rac2Settings(settings.Group):
    class IsoFile(settings.UserFilePath):
        """File name of the Ratchet & Clank 2 ISO"""
        description = "Ratchet & Clank 2 PS2 ISO file"
        copy_to = "Ratchet & Clank 2.iso"

    class IsoStart(str):
        """
        Set this to false to never autostart an iso (such as after patching),
        Set it to true to have the operating system default program open the iso
        Alternatively, set it to a path to a program to open the .iso file with (like PCSX2)
        """

    iso_file: IsoFile = IsoFile(IsoFile.copy_to)
    iso_start: typing.Union[IsoStart, bool] = False


class Rac2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ratchet & Clank 2 for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["evilwb"]
    )]


class Rac2World(World):
    """
    Ratchet & Clank 2: Going Commando is a third-person shooter platform game originally for the PlayStation 2. Play as
    Ratchet and Clank as they attempt to unravel a conspiracy in a new galaxy involving a mysterious "pet project"
    orchestrated by the shadowy MegaCorp.
    """
    game = "Ratchet & Clank 2"
    web = Rac2Web()
    options_dataclass = Rac2Options
    options: Rac2Options
    topology_present = True
    item_name_to_id = {str(item_data.name): item_data.id for item_data in item_table.values()}
    location_name_to_id = {str(location_data.name): location_data.id for location_data in every_location.values()}
    settings: Rac2Settings
    starting_planet: Optional[PlanetData] = None
    prefilled_item_map: Dict[str, str] = {}  # Dict of location name to item name

    def get_filler_item_name(self) -> str:
        return ItemName.Platinum_Bolt

    def create_regions(self) -> None:
        create_regions(self)

    def create_item(self, name: str, override: Optional[ItemClassification] = None) -> "Item":
        created_thing = item_table[name]
        if override:
            return Rac2Item(name, override, created_thing.id, self.player)
        return Rac2Item(name, created_thing.classification, created_thing.id, self.player)

    def create_event(self, name: str) -> "Item":
        return Rac2Item(name, ItemClassification.progression, None, self.player)

    def pre_fill(self) -> None:
        for location_name, item_name in self.prefilled_item_map.items():
            location = self.get_location(location_name)
            item = self.create_item(item_name, ItemClassification.progression)
            location.place_locked_item(item)

    def create_items(self) -> None:
        excluded = {}
        items_added = 0
        start_inventory = []

        # Select starting planets
        possible_start_coords = [planet.coord_item for planet in planets if planet.can_start]
        self.random.shuffle(possible_start_coords)
        start_inventory += possible_start_coords[:3]

        for start_item in start_inventory:
            ap_item = self.create_item(start_item)
            if ap_item not in self.multiworld.precollected_items[self.player]:
                self.multiworld.push_precollected(ap_item)

        # add items to pool
        items_with_multiple = [ItemName.Platinum_Bolt, ItemName.Nanotech_Boost, ItemName.Hypnomatic_Part]
        for item_name in item_table.keys():
            if item_name in start_inventory and item_name not in items_with_multiple:
                continue
            if item_name in excluded.keys():
                continue
            elif item_table[item_name].max_capacity > 1:
                for new_item in range(item_table[item_name].max_capacity):
                    self.multiworld.itempool += [
                        self.create_item(item_name, item_table[item_name].classification)]
                    items_added += 1
            # elif item_name == ItemName.Aranos_Prison_Coords:
            #     self.multiworld.get_location(LocationName.Boldan_Find_Fizzwidget,
            #                                  self.player).place_locked_item(self.create_item(item_name))
            else:
                self.multiworld.itempool += [self.create_item(item_name)]
                items_added += 1

        # add platinum bolts in whatever slots we have left
        remain = (len(every_location) - 1) - items_added
        print(f"Not enough items to fill all locations. Adding {remain} Platinum Bolt(s) to the item pool")
        for _ in range(remain):
            self.multiworld.itempool += [self.create_item(ItemName.Platinum_Bolt)]

    def set_rules(self) -> None:
        self.multiworld.get_location(LocationName.Yeedil_Defeat_Mutated_Protopet, self.player).place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        aprac2 = Rac2ProcedurePatch(player=self.player, player_name=self.multiworld.get_player_name(self.player))
        generate_patch(self.multiworld, self.player, aprac2)
        rom_path = os.path.join(output_directory,
                                f"{self.multiworld.get_out_file_name_base(self.player)}{aprac2.patch_file_ending}")
        aprac2.write(rom_path)
