import fipper


class ButtonParser:
    async def button_parser(self: 'fipper.Client', raw_text: str):
        prev = 0
        note_data = ""
        buttons = []
        for match in self.button_regex.finditer(raw_text):
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and raw_text[to_check] == "\\":
                n_escapes += 1
                to_check -= 1
            if n_escapes % 2 == 0:
                buttons.append((match.group(2), match.group(3), bool(match.group(4))))
                note_data += raw_text[prev : match.start(1)]
                prev = match.end(1)
            elif n_escapes % 2 == 1:
                note_data += raw_text[prev:to_check]
                prev = match.start(1) - 1
            else:
                break
        else:
            note_data += raw_text[prev:]
        text = note_data.strip()
        return text, buttons
