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


class StartingWeapons(Choice):
    """Randomize what two weapons you start the game with.
    Vanilla: Start with the Lancer and Gravity Bomb.
    Balanced: Start with two random weapons that are relatively balanced.
    Non-Broken: Start with two random weapons besides RYNO II and Zodiac.
    Random All: Start with any two weapons.
    """
    display_name = "Starting Weapons"
    option_vanilla = 0
    option_balanced = 1
    option_non_broken = 2
    option_all = 3
    default = 0


class RandomizeGadgetronVendor(Toggle):
    """Randomize what items appear at the Gadgetron vendor on Barlow."""
    display_name = "Randomize Gadgetron Vendor"


class RandomizeMegacorpVendor(Toggle):
    """Randomize what items appear at the Megacorp vendor. New items will get added as you visit more planets."""
    display_name = "Randomize Megacorp Vendor"


class SkipWupashNebula(DefaultOnToggle):
    """Skips the Wupash Nebula ship section that appears when first traveling to Maktar Nebula."""
    display_name = "Skip Wupash Nebula"


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
    range_start = 10
    range_end = 400
    default = 100


class WeaponExperienceMultiplier(Range):
    """A multiplier applied to experience gained for weapon levels, in percent."""
    display_name = "Weapon XP Multiplier"
    range_start = 10
    range_end = 400
    default = 100


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    starting_weapons: StartingWeapons
    randomize_megacorp_vendor: RandomizeMegacorpVendor
    randomize_gadgetron_vendor: RandomizeGadgetronVendor
    skip_wupash_nebula: SkipWupashNebula
    allow_first_person_mode: AllowFirstPersonMode
    enable_bolt_multiplier: EnableBoltMultiplier
    no_revisit_reward_change: NoRevisitRewardChange
    no_kill_reward_degradation: NoKillRewardDegradation
    free_challenge_selection: FreeChallengeSelection
    nanotech_xp_multiplier: NanotechExperienceMultiplier
    weapon_xp_multiplier: WeaponExperienceMultiplier
