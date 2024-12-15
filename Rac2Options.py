
from Options import DeathLink, StartInventoryPool, PerGameCommonOptions
from dataclasses import dataclass


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
