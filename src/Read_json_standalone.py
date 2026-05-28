import json


def build_modbus_dict(json_path):

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}

    for block in data:

        slave_id = block.get("slave_id")
        slave_key = f"slave_ID_{slave_id}"

        # crear nodo si no existe
        if slave_key not in result:
            result[slave_key] = {}

        addresses = block.get("addresses", [])
        registers = block.get("registers", [])

        # asegurar que sean same length
        for addr, reg in zip(addresses, registers):

            result[slave_key][addr] = {
                "name": reg.get("name", ""),
                "is_bitmap": reg.get("is_bitmap", False),
                "bit_labels": reg.get("bit_labels", [])
            }

    return result