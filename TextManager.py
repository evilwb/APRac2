from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


class TextManager:
    """
    This dynamic text injector replaces the "Clank's Day at Insomniac" contiguous strings by others of our own,
    and automatically re-route existing vanilla text by changing offsets to point on those new strings.
    """
    DYNAMIC_TEXT_BLOCK_SIZE = 0x893

    def __init__(self, ctx: 'Rac2Context'):
        self.ctx = ctx
        self.base_addr = ctx.game_interface.get_text_address(0x3246)  # First "Clank's Day at Insomniac" string
        self.addr = self.base_addr

    def current_size(self):
        return self.addr - self.base_addr

    def get_formatted_item_name(self, location_id: int):
        net_item = self.ctx.locations_info.get(location_id, None)
        if net_item is None:
            return "???"
        item_name = self.ctx.item_names.lookup_in_slot(net_item.item, net_item.player)

        # Take a color depending on item's usefulness
        color = '\x0A'  # Filler / Trap = Green
        if net_item.flags & 0b001:
            color = '\x0C'  # Progression = Orange
        elif net_item.flags & 0b010:
            color = '\x09'  # Useful = Blue

        # Item is ours, no need to specify player name
        if self.ctx.slot == net_item.player:
            return f"{color}{item_name}\x08"
        # Item belongs to someone else, give their name
        player_name = self.ctx.player_names.get(net_item.player, "???")
        return f"{color}{player_name}'s {item_name}\x08"

    @staticmethod
    def format_text(text: str, max_word_size: int, max_line_size: int) -> str:
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
                    if 0x09 <= ord(char) <= 0x0f:
                        words[0] = char + words[0]
                        break

        joining_str = '\x01'
        # Pad lines with a few spaces if strings begin with a controller button icon
        if 0x10 <= ord(lines[0][0]) <= 0x19:
            joining_str += "    "
        return joining_str.join(lines)

    def inject(self, vanilla_text_id: int, text: str):
        text_bytes = self.format_text(text, 32, 40).encode() + b'\x00'
        if self.current_size() + len(text_bytes) > TextManager.DYNAMIC_TEXT_BLOCK_SIZE:
            # Failsafe, but it should never happen if proper limits are set in `get_descriptive_item_name`
            size_left = TextManager.DYNAMIC_TEXT_BLOCK_SIZE - self.current_size() - 1
            text_bytes = text_bytes[:size_left] + b'\x00'
        self.ctx.game_interface.pcsx2_interface.write_bytes(self.addr, text_bytes)
        self.ctx.game_interface.set_text_address(vanilla_text_id, self.addr)
        self.addr += len(text_bytes)

    def replace(self, vanilla_text_id: int, text: str):
        addr = self.ctx.game_interface.get_text_address(vanilla_text_id)
        if addr:
            text_bytes = text.encode() + b'\x00'
            self.ctx.game_interface.pcsx2_interface.write_bytes(addr, text_bytes)
