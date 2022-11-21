
def csv2list(val: str) -> list[str]:
    val = val.replace(' ', '')
    items = val.split(',')
    return items
