import re

def parse_table_row(row):
    """
    Remove as barras verticais e divide a linha em colunas, removendo espaços.
    """
    # Remove a borda e divide pela barra vertical
    parts = [p.strip() for p in row.strip().strip('|').split('|')]
    return parts

def is_data_row(parts):
    """
    Considera a linha como de dados se a primeira coluna for numérica.
    """
    return parts and parts[0].isdigit()

def parse_hydrogen_bond_row(parts):
    # Colunas: 0: RESNR, 1: RESTYPE, 2: RESCHAIN, 3: RESNR_LIG, 4: RESTYPE_LIG, 5: RESCHAIN_LIG, 7: DIST_H-A
    if len(parts) < 8:
        return None
    return f"Residue: {parts[1]} {parts[2]} {parts[0]} | Ligand: {parts[4]} {parts[5]} {parts[3]} | Distance H-A: {parts[7]}"

def parse_hydrophobic_row(parts):
    # Colunas: 0: RESNR, 1: RESTYPE, 2: RESCHAIN, 3: RESNR_LIG, 4: RESTYPE_LIG, 5: RESCHAIN_LIG, 6: DIST
    if len(parts) < 7:
        return None
    return f"Residue: {parts[1]} {parts[2]} {parts[0]} | Ligand: {parts[4]} {parts[5]} {parts[3]} | Distance: {parts[6]}"

def parse_salt_bridge_row(parts):
    # Colunas: 0: RESNR, 1: RESTYPE, 2: RESCHAIN, 4: RESNR_LIG, 5: RESTYPE_LIG, 6: RESCHAIN_LIG, 7: DIST
    if len(parts) < 8:
        return None
    return f"Residue: {parts[1]} {parts[2]} {parts[0]} | Ligand: {parts[5]} {parts[6]} {parts[4]} | Distance: {parts[7]}"

def parse_pi_cation_row(parts):
    # Colunas: 0: RESNR, 1: RESTYPE, 2: RESCHAIN, 4: RESNR_LIG, 5: RESTYPE_LIG, 6: RESCHAIN_LIG, 7: DIST
    if len(parts) < 8:
        return None
    return f"Residue: {parts[1]} {parts[2]} {parts[0]} | Ligand: {parts[5]} {parts[6]} {parts[4]} | Distance: {parts[7]}"

# Mapeia o nome da seção (como aparece entre ** **) para (título de saída, função parser)
section_parsers = {
    "Hydrogen Bonds": ("Hydrogen Bond:", parse_hydrogen_bond_row),
    "Hydrophobic Interactions": ("Hydrophobic Interaction:", parse_hydrophobic_row),
    "Salt Bridges": ("Salt Bridge:", parse_salt_bridge_row),
    "pi-Cation Interactions": ("pi-Cation Interactions:", parse_pi_cation_row),
    # Você pode adicionar outros mapeamentos, por exemplo:
    # "Pi-Stacking": ("Pi-Stacking:", parse_pi_stacking_row),
    # "Disulfide Bridge": ("Disulfide Bridge:", parse_disulfide_bridge_row),
    # "Metal Coordination": ("Metal Coordination:", parse_metal_coordination_row),
    # "Water Bridge": ("Water Bridge:", parse_water_bridge_row),
    # "Halogen Bond": ("Halogen Bond:", parse_halogen_bond_row),
}

def process_plip_file(filename):
    structure = None
    results = {}  # chave: seção, valor: lista de linhas extraídas
    current_section = None
    current_parser = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip()
            
            # Captura a linha que indica a estrutura PDB, se ainda não foi definida
            if not structure:
                if line.startswith("Prediction of noncovalent interactions for PDB structure"):
                    structure = line

            # Detecta início de uma seção de interação (linha iniciada e terminada por **)
            section_match = re.match(r"\*\*(.+?)\*\*", line)
            if section_match:
                sec_title = section_match.group(1).strip()
                if sec_title in section_parsers:
                    current_section = sec_title
                    # Se já houver dados para essa seção, não reinitialize; senão, cria uma lista
                    if current_section not in results:
                        results[current_section] = []
                    current_parser = section_parsers[sec_title][1]
                else:
                    current_section = None
                    current_parser = None
                continue

            # Se estamos dentro de uma seção conhecida
            if current_section and current_parser:
                # Ignora linhas que são divisórias (iniciadas com '+' ou vazias ou formadas somente por '-' ou '=')
                if line.startswith('+') or not line.strip() or set(line.strip()) <= set("-="):
                    continue

                # Se a linha começa com '|' (possível linha da tabela)
                if line.startswith('|'):
                    parts = parse_table_row(line)
                    if is_data_row(parts):
                        parsed = current_parser(parts)
                        if parsed:
                            results[current_section].append(parsed)
    return structure, results

def print_results(structure, results):
    # Imprime a estrutura PDB lida
    if structure:
        print(f"{structure}\n")
    # Para cada seção definida em section_parsers, imprime os dados acumulados, se houver
    for sec, (title, _) in section_parsers.items():
        if sec in results and results[sec]:
            print(title)
            for row in results[sec]:
                print(row)
            print()  # Linha em branco entre seções

if __name__ == '__main__':
    # Substitua 'report.txt' pelo caminho do seu arquivo PLIP
    filename = "report.txt"
    structure, results = process_plip_file(filename)
    print_results(structure, results)
