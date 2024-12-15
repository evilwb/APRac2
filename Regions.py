import typing

from BaseClasses import CollectionState, Region
from .Locations import LocationData
from .Logic import can_pack, can_swingshot
from .data.Planets import Planet, PlanetData, planets
from .Items import ItemName

if typing.TYPE_CHECKING:
    from . import Rac2World


def create_regions(world: 'Rac2World'):
    # create all regions and populate with locations
    from worlds.rac2.Locations import Rac2Location
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for planet_data in planets:
        if planet_data.coord_item:
            def generate_planet_access_rule(planet: PlanetData) -> typing.Callable[[CollectionState], bool]:
                def planet_access_rule(state: CollectionState):
                    # Connect with special case access rules
                    if planet == Planet.Tabora:
                        return (
                            state.has(planet.coord_item, world.player)
                            and can_pack(state, world.player)
                            and can_swingshot(state, world.player)
                        )
                    if planet == Planet.Aranos_Prison:
                        return (
                            state.has(planet.coord_item, world.player)
                            and state.has_all([ItemName.Gravity_Boots, ItemName.Levitator], world.player)
                        )
                    # Connect with general case access rule
                    else:
                        return state.has(planet.coord_item, world.player)
                return planet_access_rule

            region = Region(planet_data.name, world.player, world.multiworld)
            world.multiworld.regions.append(region)
            menu.connect(region, None, generate_planet_access_rule(planet_data))

            for location_data in planet_data.locations:
                def generate_access_rule(location_data: LocationData) -> typing.Callable[[CollectionState], bool]:
                    def access_rule(state: CollectionState):
                        return location_data.access_rule(state, world.player)
                    return access_rule

                region.add_locations({location_data.name: location_data.id}, Rac2Location)
                location = world.multiworld.get_location(location_data.name, world.player)
                location.access_rule = generate_access_rule(location_data)

    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
