# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

def split_name(name: str) -> list[str, str]:
    if "." not in name:
        raise ValueError(f'Invalid format, expected: "SECTION.OPTION", got: "{name}"')
    return name.rsplit(".", 1)
