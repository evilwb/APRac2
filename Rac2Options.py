from Options import (
    DeathLink,
    StartInventoryPool,
    PerGameCommonOptions,
    Choice,
    DefaultOnToggle,
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


class AllowFirstPersonMode(DefaultOnToggle):
    """Gives access to first person mode in 'Special' menu without being in New Game+."""
    display_name = "Allow First Person Mode"


class EnableBoltMultiplier(Toggle):
    """Enables the bolt multiplier feature without being in New Game+."""
    display_name = "Enable Bolt Multiplier"


class FreeChallengeSelection(Toggle):
    """Makes all hoverbike and spaceship challenges selectable right away, which means you don't have to win a
    challenge to access the next one."""
    display_name = "Free Challenge Selection"


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    shuffle_weapon_vendors: ShuffleWeaponVendors
    skip_wupash_nebula: SkipWupashNebula
    allow_first_person_mode: AllowFirstPersonMode
    enable_bolt_multiplier: EnableBoltMultiplier
    free_challenge_selection: FreeChallengeSelection
