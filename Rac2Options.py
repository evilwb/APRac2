from Options import (
    DeathLink,
    StartInventoryPool,
    PerGameCommonOptions,
    Choice,
    DefaultOnToggle,
    Toggle,
    Range,
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


class FreeChallengeSelection(Toggle):
    """Makes all hoverbike and spaceship challenges selectable right away, which means you don't have to win a
    challenge to access the next one."""
    display_name = "Free Challenge Selection"


class NanotechExperienceMultiplier(Range):
    """A multiplier applied to experience gained for Nanotech levels, in percent."""
    display_name = "Nanotech XP Multiplier"
    range_start = 20
    range_end = 600
    default = 100


class WeaponExperienceMultiplier(Range):
    """A multiplier applied to experience gained for weapon levels, in percent."""
    display_name = "Weapon XP Multiplier"
    range_start = 20
    range_end = 600
    default = 100


class ExtendedWeaponProgression(Toggle):
    """If enabled, make all weapon tiers obtainable through weapon experience. This means LV2 (orange) weapons can
    upgrade into LV3 (yellow) weapons, which can then upgrade into LV4 (blue) weapons.
    This effectively makes all weapons that are usually restricted to NG+ available with enough grinding."""
    display_name = "Extended Weapon Progression"


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    shuffle_weapon_vendors: ShuffleWeaponVendors
    skip_wupash_nebula: SkipWupashNebula
    allow_first_person_mode: AllowFirstPersonMode
    enable_bolt_multiplier: EnableBoltMultiplier
    no_revisit_reward_change: NoRevisitRewardChange
    no_kill_reward_degradation: NoKillRewardDegradation
    free_challenge_selection: FreeChallengeSelection
    nanotech_xp_multiplier: NanotechExperienceMultiplier
    weapon_xp_multiplier: WeaponExperienceMultiplier
    extended_weapon_progression: ExtendedWeaponProgression
