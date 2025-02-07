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


class ExperienceGain(Choice):
    """Defines the way experience is calculated in the game:
    - Vanilla: enemies killed several times are worth less XP, and revisiting a planet also applies a global malus
    - No Revisit Malus: enemies killed several times are worth less, but revisiting a planet does not reduce obtained XP
    - No Malus: an enemy always gives the same amount of XP when killed
    """

    display_name = "Experience Gain"
    option_vanilla = 0
    option_no_revisit_malus = 1
    option_no_malus = 2
    default = 0


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    shuffle_weapon_vendors: ShuffleWeaponVendors
    skip_wupash_nebula: SkipWupashNebula
    experience_gain: ExperienceGain
