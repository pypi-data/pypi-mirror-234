import generate


class Buttons:
    def generate_button(self: 'generate.Generate', markdown_note):
        """
        This function for delete memory

        Arguments
            objec (`str`):
                The objec, get data for delete from memory.

            markdown_note (`str`):
                Give string for generate button.

        Example
            text_button '''
            Hello my firend
            
            [NameButton](https://t.me/AyiinXd)
            [NameButton2](https://t.me/AyiinChats:same) #for button in right
            '''
            text, button = gen.generate_button(markdown_note=text_button)
            your code here...
        """
        prev = 0
        note_data = ""
        buttons = []
        for match in self.btn_url_regex.finditer(markdown_note):
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and markdown_note[to_check] == "\\":
                n_escapes += 1
                to_check -= 1
            if n_escapes % 2 == 0:
                buttons.append((match.group(2), match.group(3), bool(match.group(4))))
                note_data += markdown_note[prev : match.start(1)]
                prev = match.end(1)
            elif n_escapes % 2 == 1:
                note_data += markdown_note[prev:to_check]
                prev = match.start(1) - 1
            else:
                break
        else:
            note_data += markdown_note[prev:]
        text = note_data.strip()
        return text, buttons