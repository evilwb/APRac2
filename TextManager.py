from typing import TYPE_CHECKING

from NetUtils import NetworkItem

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context

COLOR_WHITE = '\x08'
COLOR_BLUE = '\x09'
COLOR_GREEN = '\x0A'
COLOR_VIOLET = '\x0B'
COLOR_ORANGE = '\x0C'


def colorize_item_name(item_name: str, item_flags: int) -> str:
    # Take a color depending on item's usefulness
    color = COLOR_GREEN  # Filler / Trap = Green
    if item_flags & 0b001:
        color = COLOR_ORANGE  # Progression = Orange
    elif item_flags & 0b010:
        color = COLOR_BLUE  # Useful = Blue
    return f"{color}{item_name}{COLOR_WHITE}"


def get_rich_item_name(ctx: 'Rac2Context', net_item: NetworkItem, player_name_after: bool = False) -> str:
    item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
    item_name = colorize_item_name(item_name, net_item.flags)

    if ctx.slot == net_item.player:
        # Item is ours, no need to specify player name
        return item_name
    else:
        # Item belongs to someone else, give their name
        player_name = ctx.player_names.get(net_item.player, "???")
        if player_name_after:
            return f"{item_name} to {player_name}"
        return f"{player_name}'s {item_name}"


def get_rich_item_name_from_location(ctx: 'Rac2Context', location_id: int) -> str:
    net_item = ctx.locations_info.get(location_id, None)
    if net_item is None:
        return "???"
    return get_rich_item_name(ctx, net_item)


def wrap_text(text: str, max_word_size: int, max_line_size: int) -> str:
    """
    Formats the given string with line breaks and ellipsis where relevant.

    :param text: the input text
    :param max_word_size: the max size of a word in bytes (if longer, it is truncated using "...")
    :param max_line_size: the max size of a line in bytes (line breaks are placed to respect this rule)
    """
    words = [word if len(word) < max_word_size else f"{word}\xAD" for word in text.split(' ')]
    lines = []
    while len(words) > 0:
        current_line = ""
        while len(words) > 0:
            if len(current_line) > 0:
                # If adding that word would make the line go over the size limit, "commit" the line by breaking
                # process next line
                if len(current_line) + 1 + len(words[0]) > max_line_size:
                    break
                current_line += " "
            current_line += words[0]
            words = words[1:]
        lines.append(current_line)
        # Propagate color to next line if it wasn't white and there will be another line
        if len(words) > 0:
            for char in current_line[::-1]:
                if ord(char) == 0x08:
                    # Last color was white, nothing to do
                    break
                if 0x09 <= ord(char) <= 0x0f:
                    # Last color was not white, propagate it to next line
                    words[0] = char + words[0]
                    break

    joining_str = '\x01'
    # Pad lines with a few spaces if strings begin with a controller button icon
    if 0x10 <= ord(lines[0][0]) <= 0x19:
        joining_str += "    "
    return joining_str.join(lines)


class TextManager:
    def __init__(self, ctx: 'Rac2Context'):
        self.ctx = ctx
        self.injectable_chunks = []

        clanks_day_at_insomniac_chunk = ctx.game_interface.get_text_address(0x3246)
        self.injectable_chunks.append([clanks_day_at_insomniac_chunk, clanks_day_at_insomniac_chunk + 0x893])
        insomniac_museum_chunk = ctx.game_interface.get_text_address(0x1BAD)
        self.injectable_chunks.append([insomniac_museum_chunk, insomniac_museum_chunk + 0x18DC])

    def inject(self, vanilla_text_id: int, text: str):
        """
        Replace a vanilla string by injecting the given text in some unused space, and re-routing the text ID on this
        new address. This is needed when replacement string have a chance of exceeding original string size, otherwise
        prefer using `replace`.
        """
        text_bytes = wrap_text(text, 32, 40).encode() + b'\x00'

        for chunk in self.injectable_chunks:
            remaining_bytes = chunk[1] - chunk[0]
            if len(text_bytes) <= remaining_bytes:
                # We found a chunk with enough room to inject the string, do it
                if self.ctx.game_interface.set_text_address(vanilla_text_id, chunk[0]):
                    self.ctx.game_interface.pcsx2_interface.write_bytes(chunk[0], text_bytes)
                    chunk[0] += len(text_bytes)
                return

        self.ctx.game_interface.logger.error("Not enough space to inject game text, please report this issue!")

    def replace(self, vanilla_text_id: int, text: str):
        """
        Replaces a vanilla string by simply overwriting the vanilla string contents. If not used carefully, this can
        overlap the following strings, so use this carefully or use `inject` instead if you have any doubt.
        """
        addr = self.ctx.game_interface.get_text_address(vanilla_text_id)
        if addr:
            text_bytes = text.encode() + b'\x00'
            self.ctx.game_interface.pcsx2_interface.write_bytes(addr, text_bytes)
