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


class NoRevisitRewardChange(Toggle):
    """In the vanilla game, rewards given when killing enemies change when you come back to a previously visited planet
    (bolts & experience). Enabling this option removes this behavior, making the experience and bolts obtained more
    stable throughout the seed.
    """
    display_name = "Remove Revisit Rewards Change"


class NoKillRewardDegradation(Toggle):
    """In the vanilla game, rewards given by a specific enemy decrease each time you kill it (bolts & experience).
    Enabling this option removes this behavior, making the experience and bolts obtained more stable throughout
    the seed.
    """
    display_name = "Remove Kill Rewards Degradation"


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    shuffle_weapon_vendors: ShuffleWeaponVendors
    skip_wupash_nebula: SkipWupashNebula
    no_revisit_reward_change: NoRevisitRewardChange
    no_kill_reward_degradation: NoKillRewardDegradation
