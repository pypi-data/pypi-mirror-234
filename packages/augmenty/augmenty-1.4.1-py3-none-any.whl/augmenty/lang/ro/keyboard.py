from ...util import registry


@registry.keyboards("ro_qwerty_v1")
def create_qwerty_ro():
    qwerty = {
        "default": [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "'", "+"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "º", "´"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ç", "~", "\\"],
            ["<", "z", "x", "c", "v", "b", "n", "m", ",", ".", "-"],
        ],
        "shift": [
            ["!", '"', "#", "$", "%", "&", "/", "(", ")", "=", "?", "*"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "ª", "`"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ç", "^", "|"],
            [">", "z", "x", "c", "v", "b", "n", "m", ",", ".", "_"],
        ],
    }
    return qwerty
