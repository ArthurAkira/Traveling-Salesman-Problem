import math

class Cidadao:
    def __init__(self, id_, x, y):
        self.id_ = id_
        self.x = x
        self.y = y

    def __str__(self):
        return f"Cidadão {self.id_}: ({self.x}, {self.y})"

def ler_tsp(caminho):
    with open(caminho) as f:
        lines = f.readlines()
    
    dimension = None
    edge_weight_type = None
    edge_weight_format = None
    coord_section = False
    weight_section = False
    cidades = []
    matriz = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())
        elif line.startswith("EDGE_WEIGHT_TYPE"):
            edge_weight_type = line.split(":")[1].strip()
        elif line.startswith("EDGE_WEIGHT_FORMAT"):
            edge_weight_format = line.split(":")[1].strip()
        elif line == "NODE_COORD_SECTION":
            coord_section = True
            i += 1
            break
        elif line == "EDGE_WEIGHT_SECTION":
            weight_section = True
            i += 1
            break
        i += 1
    
    if coord_section:
        while i < len(lines):
            line = lines[i].strip()
            if line == "EOF":
                break
            partes = line.split()
            if len(partes) >= 3:
                cidades.append(Cidadao(int(partes[0]), float(partes[1]), float(partes[2])))
            i += 1
    elif weight_section and edge_weight_format == "UPPER_ROW":
        weights = []
        while i < len(lines):
            line = lines[i].strip()
            if line == "EOF":
                break
            weights.extend([float(x) for x in line.split()])
            i += 1
        # Build upper triangle matrix
        matriz = [[0] * dimension for _ in range(dimension)]
        idx = 0
        for row in range(dimension - 1):
            for col in range(row + 1, dimension):
                matriz[row][col] = weights[idx]
                matriz[col][row] = weights[idx]
                idx += 1
        # Create dummy cities with ids
        for j in range(1, dimension + 1):
            cidades.append(Cidadao(j, 0, 0))  # dummy coords
    
    return cidades, matriz if matriz else None