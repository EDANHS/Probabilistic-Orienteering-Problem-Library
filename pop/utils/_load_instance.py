from pop.utils import POP_Instance


def _parse_instance(instance_text: str) -> dict:
    lines = instance_text.strip().split("\n")
    data = {}

    section = None  # Para rastrear en qué sección estamos
    node_coords = {}
    node_prizes = {}

    for line in lines:
        line = line.strip()

        # Ignorar líneas vacías
        if not line:
            continue

        # Cambiar de sección
        if line == "NODE_COORD_SECTION":
            section = "NODE_COORD_SECTION"
            continue
        elif line == "NODE_PRIZE_PROBABILITY_SECTION":
            section = "NODE_PRIZE_PROBABILITY_SECTION"
            continue

        # Si estamos en una sección específica, procesar los datos
        if section == "NODE_COORD_SECTION":
            parts = line.split()
            node_coords[int(parts[0])] = (int(parts[1]), int(parts[2]))
        elif section == "NODE_PRIZE_PROBABILITY_SECTION":
            parts = line.split()
            node_prizes[int(parts[0])] = (int(parts[1]), float(parts[2]))
        else:
            # Procesar claves generales
            key, value = map(str.strip, line.split(":", 1))
            if key in ["DIMENSION", "TMAX", "TPRIZE", "ORIGIN", "DESTINATION"]:
                data[key] = int(value)
            else:
                data[key] = value

    # Agregar las secciones al diccionario principal
    data["NODE_COORD_SECTION"] = node_coords
    data["NODE_PRIZE_PROBABILITY_SECTION"] = node_prizes

    return data

def load_pop_instance(filename: str) -> POP_Instance:

    with open(filename, "r", encoding="utf-8") as file:
        instance_text = file.read()

    instance = _parse_instance(instance_text=instance_text)

    x = []
    y = []
    pis = []
    prizes = []

    # Extraer coordenadas
    for idx in sorted(instance["NODE_COORD_SECTION"]):  # Ordenar para asegurar consistencia
        coord = instance["NODE_COORD_SECTION"][idx]
        x.append(coord[0])
        y.append(coord[1])

    # Extraer premios y probabilidades
    for idx in sorted(instance["NODE_PRIZE_PROBABILITY_SECTION"]):  # Ordenar para mantener coherencia
        prize_info = instance["NODE_PRIZE_PROBABILITY_SECTION"][idx]
        prizes.append(prize_info[0])
        pis.append(prize_info[1])

    return POP_Instance(x=x, y=y, prizes=prizes, pis=pis, 
                        d_max=instance["TMAX"], 
                        origin=instance["ORIGIN"],
                        destination=instance["DESTINATION"])
