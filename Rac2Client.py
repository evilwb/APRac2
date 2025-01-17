import asyncio
import multiprocessing
import os
import subprocess
import traceback
from typing import Optional
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus
import Utils
from settings import get_settings
from worlds.rac2 import every_location, LocationName
from worlds.rac2.ClientCheckLocations import handle_checked_location
from worlds.rac2.Container import get_version_from_iso, Rac2ProcedurePatch
from .Callbacks import update, init
from .ClientReceiveItems import handle_receive_items
from .NotificationManager import NotificationManager
from .Rac2Interface import HUD_MESSAGE_DURATION, ConnectionState, Rac2Interface, Rac2Planet


class Rac2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_test_hud(self, *args):
        """Send a message to the game interface."""
        self.ctx.notification_manager.queue_notification(' '.join(map(str, args)))

    def _cmd_status(self):
        """Display the current PCSX2 connection status."""
        logger.info(f"Connection status: {'Connected' if self.ctx.is_connected else 'Disconnected'}")

    def _cmd_segments(self):
        """Display the memory segment table."""
        logger.info(self.ctx.game_interface.get_segment_pointer_table())

    def _cmd_test_deathlink(self, deaths: str):
        """Queue up specified number of deaths."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(f"Queuing {deaths} deaths.")
            self.ctx.notification_manager.queue_notification("Received test deathlink")
            self.ctx.queued_deaths = int(deaths)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, Rac2Context):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            Utils.async_start(self.ctx.update_death_link(
                self.ctx.death_link_enabled), name="Update Deathlink")
            message = f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
            logger.info(message)
            self.ctx.notification_manager.queue_notification(message)


class Rac2Context(CommonContext):
    current_planet: Optional[Rac2Planet] = None
    previous_planet: Optional[Rac2Planet] = None
    is_pending_death_link_reset = False
    command_processor = Rac2CommandProcessor
    game_interface: Rac2Interface
    notification_manager: NotificationManager
    game = "Ratchet & Clank 2"
    items_handling = 0b111
    pcsx2_sync_task = None
    is_connected = ConnectionState.DISCONNECTED
    is_loading: bool = False
    slot_data: dict[str, Utils.Any] = None
    last_error_message: Optional[str] = None
    death_link_enabled = False
    queued_deaths: int = 0

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = Rac2Interface(logger)
        self.notification_manager = NotificationManager(HUD_MESSAGE_DURATION, self.game_interface.send_hud_message)
        self.locations_scouted = {
            every_location[LocationName.Oozla_Megacorp_Scientist].id,
            every_location[LocationName.Maktar_Arena_Challenge].id,
            every_location[LocationName.Barlow_Inventor].id,
            every_location[LocationName.Feltzin_Defeat_Thug_Ships].id,
            every_location[LocationName.Feltzin_Race_PB].id,
            every_location[LocationName.Notak_Worker_Bots].id,
            every_location[LocationName.Hrugis_Destroy_Defenses].id,
            every_location[LocationName.Hrugis_Race_PB].id,
            every_location[LocationName.Joba_Shady_Salesman].id,
            every_location[LocationName.Joba_Arena_Battle].id,
            every_location[LocationName.Joba_Arena_Cage_Match].id,
            every_location[LocationName.Todano_Stuart_Zurgo_Trade].id,
            every_location[LocationName.Aranos_Plumber].id,
            every_location[LocationName.Gorn_Defeat_Thug_Fleet].id,
            every_location[LocationName.Gorn_Race_PB].id,
            every_location[LocationName.Smolg_Mutant_Crab].id,
            every_location[LocationName.Damosel_Hypnotist].id,
            every_location[LocationName.Grelbin_Mystic_More_Moonstones].id,
        }

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        if self.death_link_enabled:
            self.queued_deaths += 1
            cause = data.get("cause", "")
            if cause:
                self.notification_manager.queue_notification(f"DeathLink: {cause}")
            else:
                self.notification_manager.queue_notification(f"DeathLink: Received from {data['source']}")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Rac2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))

    def run_gui(self):
        from kvui import GameManager

        class Rac2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Ratchet & Clank 2 Client"

        self.ui = Rac2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def update_connection_status(ctx: Rac2Context, status: bool):
    if ctx.is_connected == status:
        return

    if status:
        logger.info("Connected to Ratchet & Clank 2")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")
    ctx.is_connected = status


async def pcsx2_sync_task(ctx: Rac2Context):
    logger.info("Starting Ratchet & Clank 2 Connector, attempting to connect to emulator...")
    ctx.game_interface.connect_to_game()
    while not ctx.exit_event.is_set():
        try:
            is_connected = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, is_connected)
            if is_connected:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
        except ConnectionError:
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


async def handle_check_goal_complete(ctx: Rac2Context):
    if ctx.current_planet is Rac2Planet.Yeedil and ctx.game_interface.get_moby(197).state == 0x11:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    pass


async def handle_deathlink(ctx: Rac2Context):
    if ctx.game_interface.get_alive():
        if ctx.is_pending_death_link_reset:
            ctx.is_pending_death_link_reset = False
        if ctx.queued_deaths > 0 and ctx.game_interface.get_pause_state() == 0:
            ctx.is_pending_death_link_reset = True
            ctx.game_interface.kill_player()
            ctx.queued_deaths -= 1
    else:
        if not ctx.is_pending_death_link_reset:
            await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of Nanotech.")
            ctx.is_pending_death_link_reset = True


async def _handle_game_ready(ctx: Rac2Context):
    if ctx.is_loading:
        if not ctx.game_interface.is_loading():
            ctx.is_loading = False
            current_planet = ctx.game_interface.get_current_planet()
            if current_planet is not None:
                logger.info(f"Loaded planet {current_planet} ({current_planet.name})")
            await asyncio.sleep(1)
        await asyncio.sleep(0.5)
        return
    elif ctx.game_interface.is_loading():
        ctx.game_interface.logger.info("Waiting for planet to load...")
        ctx.is_loading = True
        return

    ctx.notification_manager.handle_notifications()

    if ctx.current_planet != ctx.game_interface.get_current_planet():
        ctx.previous_planet = ctx.current_planet
        ctx.current_planet = ctx.game_interface.get_current_planet()
        init(ctx, ctx.server is not None and ctx.slot is not None)
    update(ctx, ctx.server is not None and ctx.slot is not None)

    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        current_inventory = ctx.game_interface.get_current_inventory()
        if ctx.current_planet is not None and ctx.current_planet > 0:
            await handle_receive_items(ctx, current_inventory)
        await handle_checked_location(ctx)
        await handle_check_goal_complete(ctx)

        if ctx.death_link_enabled:
            await handle_deathlink(ctx)
        await asyncio.sleep(0.5)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: Rac2Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await asyncio.sleep(3)


async def run_game(romfile):
    auto_start = get_settings().rac2_options.get("iso_start", True)

    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(aprac2_file: str):
    aprac2_file = os.path.abspath(aprac2_file)
    input_iso_path = get_settings().rac2_options.iso_file
    game_version = get_version_from_iso(input_iso_path)
    base_name = os.path.splitext(aprac2_file)[0]
    output_path = base_name + '.iso'

    if not os.path.exists(output_path):
        from .PatcherUI import PatcherUI
        patcher = PatcherUI(aprac2_file, output_path, logger)
        patcher.run()
    Utils.async_start(run_game(output_path))


def launch():
    Utils.init_logging("RAC2 Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        parser.add_argument('aprac2_file', default="", type=str, nargs="?",
                            help='Path to an aprac2 file')
        args = parser.parse_args()

        if os.path.isfile(args.aprac2_file):
            logger.info("aprac2 file supplied, beginning patching process...")
            await patch_and_run_game(args.aprac2_file)

        ctx = Rac2Context(args.connect, args.password)

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.pcsx2_sync_task = asyncio.create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await asyncio.sleep(3)
            await ctx.pcsx2_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == '__main__':
    launch()
