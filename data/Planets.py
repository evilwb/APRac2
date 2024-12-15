from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, List, NamedTuple

from ..Items import ItemName
from ..Locations import *


@dataclass(frozen=True)
class PlanetData:
    name: str
    number: int
    coord_item: ItemName
    locations: List[LocationData]
    can_start: bool

    def __init__(self, name, number, coord_item=None, locations=None, can_start=False):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'number', number)
        object.__setattr__(self, 'coord_item', coord_item)
        object.__setattr__(self, 'locations', locations)
        object.__setattr__(self, 'can_start', can_start)


@dataclass(frozen=True)
class Planet:
    Aranos_Tutorial = PlanetData("Aranos Tutorial", 0)
    Oozla = PlanetData("Oozla", 1, ItemName.Oozla_Coords, oozla_location_table.values(), True)
    Maktar_Nebula = PlanetData("Maktar Nebula", 2, ItemName.Maktar_Nebula_Coords, maktar_location_table.values(), True)
    Endako = PlanetData("Endako", 3, ItemName.Endako_Coords, endako_location_table.values(), True)
    Barlow = PlanetData("Barlow", 4, ItemName.Barlow_Coords, barlow_location_table.values())
    Feltzin_System = PlanetData("Feltzin System", 5, ItemName.Feltzin_System_Coords, feltzin_location_table.values(), True)
    Notak = PlanetData("Notak", 6, ItemName.Notak_Coords, notak_location_table.values(), True)
    Siberius = PlanetData("Siberius", 7, ItemName.Siberius_Coords, siberius_location_table.values())
    Tabora = PlanetData("Tabora", 8, ItemName.Tabora_Coords, tabora_location_table.values())
    Dobbo = PlanetData("Dobbo", 9, ItemName.Dobbo_Coords, dobbo_location_table.values())
    Hrugis_Cloud = PlanetData("Hrugis Cloud", 10, ItemName.Hrugis_Cloud_Coords, hrugis_location_table.values(), True)
    Joba = PlanetData("Joba", 11, ItemName.Joba_Coords, joba_location_table.values())
    Todano = PlanetData("Todano", 12, ItemName.Todano_Coords, todano_location_table.values(), True)
    Boldan = PlanetData("Boldan", 13, ItemName.Boldan_Coords, boldan_location_table.values())
    Aranos_Prison = PlanetData("Aranos Prison", 14, ItemName.Aranos_Prison_Coords, aranos_location_table.values())
    Gorn = PlanetData("Gorn", 15, ItemName.Gorn_Coords, gorn_location_table.values(), True)
    Snivelak = PlanetData("Snivelak", 16, ItemName.Snivelak_Coords, snivelak_location_table.values())
    Smolg = PlanetData("Smolg", 17, ItemName.Smolg_Coords, smolg_location_table.values())
    Damosel = PlanetData("Damosel", 18, ItemName.Damosel_Coords, damosel_location_table.values(), True)
    Grelbin = PlanetData("Grelbin", 19, ItemName.Grelbin_Coords, grelbin_location_table.values())
    Yeedil = PlanetData("Yeedil", 20, ItemName.Yeedil_Coords, yeedil_location_table.values())
    Dobbo_Orbit = PlanetData("Dobbo Orbit", 22)
    Damosel_Orbit = PlanetData("Damosel Orbit", 23)
    Ship_Shack = PlanetData("Ship Shack", 24)
    Wupash_Nebula = PlanetData("Wupash Nebula", 25)
    Jamming_Array = PlanetData("Jamming Array", 26)
    Insomniac_Museum = PlanetData("Insomniac Museum", 30)


planets = [planet for planet in Planet.__dict__.values() if isinstance(planet, PlanetData)]
