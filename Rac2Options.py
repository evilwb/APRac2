from Options import (
    DeathLink,
    StartInventoryPool,
    PerGameCommonOptions,
    Choice,
    Toggle,
)
from dataclasses import dataclass


class ShuffleWeaponVendors(Choice):
    """Shuffle what items appear at the Megacorp and Gadgetron vendors. Also shuffles your two starting weapons.
    Off: The vendors will stay unmodified.
    Weapons: All weapons that are normally available at the vendors will be shuffled among the vendor slots.
    """

    option_off = 0
    option_weapons = 1
    default = 0


class SkipWupashNebula(Toggle):
    """Skips the Wupash Nebula ship section that appears when first traveling to Maktar Nebula."""

    display_name = "Skip Wupash Nebula"
    default = True


class EnableBoltMultiplier(Toggle):
    """Enables the bolt multiplier feature without being in New Game+."""
    display_name = "Enable Bolt Multiplier"


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    shuffle_weapon_vendors: ShuffleWeaponVendors
    skip_wupash_nebula: SkipWupashNebula
    enable_bolt_multiplier: EnableBoltMultiplier
