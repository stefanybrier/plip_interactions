import re

class Interaction:
    def __init__(self, parts):
        self.RESNR = parts[0]
        self.RESTYPE = parts[1]
        self.RESCHAIN = parts[2]
        self.RESNR_LIG = parts[3]
        self.RESTYPE_LIG = parts[4]
        self.RESCHAIN_LIG = parts[5]
        self.LIGCOO = parts[-2] if len(parts) > 8 else None
        self.PROTCOO = parts[-1] if len(parts) > 8 else None
    
    def __str__(self):
        return (f"Residue: {self.RESTYPE} {self.RESCHAIN} {self.RESNR} | "
                f"Ligand: {self.RESTYPE_LIG} {self.RESCHAIN_LIG} {self.RESNR_LIG}")

class HydrogenBond(Interaction):
    def __init__(self, parts):
        super().__init__(parts)
        self.SIDECHAIN = parts[6]
        self.DIST_H_A = parts[7]
        self.DIST_D_A = parts[8]
        self.DON_ANGLE = parts[9]
        self.PROTISDON = parts[10]
        self.DONORIDX = parts[11]
        self.DONORTYPE = parts[12]
        self.ACCEPTORIDX = parts[13]
        self.ACCEPTORTYPE = parts[14]
    
    def __str__(self):
        return (super().__str__() + f" | Distance H-A: {self.DIST_H_A} | Distance D-A: {self.DIST_D_A} | "
                f"Donor Angle: {self.DON_ANGLE}")

class HydrophobicInteraction(Interaction):
    def __init__(self, parts):
        super().__init__(parts)
        self.DIST = parts[6]
        self.LIGCARBONIDX = parts[7]
        self.PROTCARBONIDX = parts[8]
    
    def __str__(self):
        return super().__str__() + f" | Distance: {self.DIST}"

class SaltBridge(Interaction):
    def __init__(self, parts):
        super().__init__(parts)
        self.PROT_IDX_LIST = parts[6]
        self.DIST = parts[7]
        self.PROTISPOS = parts[8]
        self.LIG_GROUP = parts[9]
        self.LIG_IDX_LIST = parts[10]
    
    def __str__(self):
        return super().__str__() + f" | Distance: {self.DIST} | Ligand Group: {self.LIG_GROUP}"

class PiCationInteraction(Interaction):
    def __init__(self, parts):
        super().__init__(parts)
        self.PROT_IDX_LIST = parts[6]
        self.DIST = parts[7]
        self.OFFSET = parts[8]
        self.PROTCHARGED = parts[9]
        self.LIG_GROUP = parts[10]
        self.LIG_IDX_LIST = parts[11]
    
    def __str__(self):
        return super().__str__() + f" | Distance: {self.DIST} | Offset: {self.OFFSET}"

class HalogenBond(Interaction):
    def __init__(self, parts):
        super().__init__(parts)
        self.SIDECHAIN = parts[6]
        self.DIST = parts[7]
        self.DON_ANGLE = parts[8]
        self.ACC_ANGLE = parts[9]
        self.DON_IDX = parts[10]
        self.DONORTYPE = parts[11]
        self.ACC_IDX = parts[12]
        self.ACCEPTORTYPE = parts[13]
    
    def __str__(self):
        return (super().__str__() + f" | Distance: {self.DIST} | Donor Angle: {self.DON_ANGLE} | "
                f"Acceptor Angle: {self.ACC_ANGLE} | Donor Type: {self.DONORTYPE} | Acceptor Type: {self.ACCEPTORTYPE}")

# Mapeamento das seções para classes
section_parsers = {
    "Hydrogen Bonds": ("Hydrogen Bond:", HydrogenBond),
    "Hydrophobic Interactions": ("Hydrophobic Interaction:", HydrophobicInteraction),
    "Salt Bridges": ("Salt Bridge:", SaltBridge),
    "pi-Cation Interactions": ("pi-Cation Interaction:", PiCationInteraction),
    "Halogen Bonds": ("Halogen Bond:", HalogenBond)
}

def parse_table_row(row):
    return [p.strip() for p in row.strip().strip('|').split('|')]

def is_data_row(parts):
    return parts and parts[0].isdigit()

def process_plip_file(filename):
    structure = None
    results = {}
    current_section = None
    current_parser = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip()
            if not structure and line.startswith("Prediction of noncovalent interactions for PDB structure"):
                structure = line
            
            section_match = re.match(r"\*\*(.+?)\*\*", line)
            if section_match:
                sec_title = section_match.group(1).strip()
                if sec_title in section_parsers:
                    current_section = sec_title
                    results.setdefault(current_section, [])
                    current_parser = section_parsers[sec_title][1]
                else:
                    current_section = None
                    current_parser = None
                continue
            
            if current_section and current_parser:
                if line.startswith('+') or not line.strip() or set(line.strip()) <= set("-="):
                    continue
                if line.startswith('|'):
                    parts = parse_table_row(line)
                    if is_data_row(parts):
                        interaction = current_parser(parts)
                        results[current_section].append(interaction)
    return structure, results

def print_results(structure, results):
    if structure:
        print(f"{structure}\n")
    for sec, (title, _) in section_parsers.items():
        if sec in results and results[sec]:
            print(title)
            for row in results[sec]:
                print(row)
            print()

if __name__ == '__main__':
    filename = "report1.txt"
    structure, results = process_plip_file(filename)
    print_results(structure, results)
