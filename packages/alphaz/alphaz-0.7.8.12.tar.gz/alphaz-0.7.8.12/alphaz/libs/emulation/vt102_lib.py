import vt102, re

CLEAR = chr(27) + "[2J"


class Screen:
    cursor = (0, 0)
    screen = []
    r_data = None
    merged: bool = False

    def read_screen(self, r_data: str):
        self.r_data = r_data
        stream = vt102.stream()
        screen = vt102.screen((24, 80))
        screen.attach(stream)

        stream.process(r_data)
        is_empty = all([x.strip() == "" for x in screen.display])

        # lines_nb = r_data.count("\x1b")

        if not is_empty:
            cursor = screen.cursor()
            self.screen = screen
            self.cursor = cursor
        return self

    def get_display(self, log: bool = False, print_mode: bool = False) -> str:
        if type(self.screen) == list:
            return ""

        display = "\n".join(self.screen.display)
        if print_mode:
            left_padding = 30
            header = " MERGED SCREEN " if self.merged else " NEW SCREEN "
            full_header = (
                ("_" * left_padding)
                + header
                + ("_" * (84 - left_padding - len(header)))
            )

            display = "\n" + full_header + "\n\n" + display + "\n" + ("_" * 84) + "\n"

        if log:
            print(display)
        return display

    def merge_screen(self, r_data):
        r_data = f"{chr(27)}[{self.cursor[1]+1};{self.cursor[0]+1}H{chr(27)}[0;0;0;0m{r_data}"
        screen = Screen().read_screen(self.r_data + r_data)
        screen.merged = True
        return screen


def clear_errors(r_data: str) -> str:
    match_error = re.findall(r"(\[[0-9]{2};[0-9]{2})(\[[0-9]{2};[0-9]{2}H)", r_data)
    if len(match_error) != 0:
        match_error = match_error[0]
        r_data = r_data.replace("".join(match_error), match_error[1])
    return r_data
