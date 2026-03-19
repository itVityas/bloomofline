from apps.shtrih.models import Models
from apps.warehouse.models import (
    WarehouseTTN,
    WarehouseDo
)


def len_word(str_in: str, col: int, replace='0') -> str:
    """change word to need count chars

    Args:
        str_in (str): string
        col (int): count chars in result world
        replace (str, optional): to what_replace, need 1 char str. Defaults to '0'.

    Returns:
        str: result word with add or remove chars
    """
    if len(str_in) < col:
        add = col - len(str_in)
        str_in = replace*add + str_in
    elif len(str_in) > col:
        rem = len(str_in) - col
        str_in = str_in[rem:]
    return str_in


def generate_barcode(ttn_number: str) -> str:
    warehouse_ttn = WarehouseTTN.objects.filter(ttn_number=ttn_number).first()
    if not warehouse_ttn:
        return f"Error: ttn_number {ttn_number} not found"

    warehouse_do = WarehouseDo.objects.filter(warehouse_ttn=warehouse_ttn)
    if not warehouse_do:
        return "Error: warehouse_do not found"

    col = warehouse_do.count()
    col = len_word(str(col), 3)  # we need col with 3 character

    ttn_date = warehouse_ttn.date
    month = ttn_date.month
    month = len_word(str(month), 2)  # we need month with 2 character
    year = ttn_date.year
    year = len_word(str(year), 2)  # we need year with 2 character

    model = Models.objects.filter(id=warehouse_do.first().warehouse_product.product.model.pk).first()
    model = len_word(str(model.code), 5)  # we need model with 5 character

    ttn_number = len_word(str(ttn_number), 8)  # we need ttn_number with 8 character

    barcode = model + month + year + col + ttn_number
    if len(barcode) < 18:
        return "Error: barcode not valid"
    return barcode
