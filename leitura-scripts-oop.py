import re

class PLIPRowParser:
    """Base class for parsing table rows from PLIP reports"""
    
    @staticmethod
    def parse_table_row(row):
        """Remove vertical bars and split into columns, stripping whitespace"""
        return [p.strip() for p in row.strip().strip('|').split('|')]
    
    @staticmethod
    def is_data_row(parts):
        """Check if the row contains data (first column is numeric)"""
        return parts and parts[0].isdigit()
    
    def parse(self, parts):
        """To be implemented by subclasses"""
        raise NotImplementedError


class HydrogenBondParser(PLIPRowParser):
    """Parser for Hydrogen Bonds section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[4]} {parts[5]} {parts[3]} | "
                f"Distance H-A: {parts[7]}")


class HydrophobicInteractionParser(PLIPRowParser):
    """Parser for Hydrophobic Interactions section"""
    
    def parse(self, parts):
        if len(parts) < 7:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[4]} {parts[5]} {parts[3]} | "
                f"Distance: {parts[6]}")


class SaltBridgeParser(PLIPRowParser):
    """Parser for Salt Bridges section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class PiCationParser(PLIPRowParser):
    """Parser for pi-Cation Interactions section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class PiStackingParser(PLIPRowParser):
    """Parser for Pi-Stacking Interactions section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class DisulfideBridgeParser(PLIPRowParser):
    """Parser for Disulfide Bridge section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class MetalCoordinationParser(PLIPRowParser):
    """Parser for Metal Coordination section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class WaterBridgeParser(PLIPRowParser):
    """Parser for Water Bridge section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class HalogenBondParser(PLIPRowParser):
    """Parser for Halogen Bond section"""
    
    def parse(self, parts):
        if len(parts) < 8:
            return None
        return (f"Residue: {parts[1]} {parts[2]} {parts[0]} | "
                f"Ligand: {parts[5]} {parts[6]} {parts[4]} | "
                f"Distance: {parts[7]}")


class PLIPReportParser:
    """Main class for parsing PLIP report files"""
    
    # Class-level configuration of available section parsers
    SECTION_PARSERS = {
        "Hydrogen Bonds": ("Hydrogen Bond:", HydrogenBondParser()),
        "Hydrophobic Interactions": ("Hydrophobic Interaction:", HydrophobicInteractionParser()),
        "Salt Bridges": ("Salt Bridge:", SaltBridgeParser()),
        "pi-Cation Interactions": ("pi-Cation Interactions:", PiCationParser()),
        "Pi-Stacking": ("Pi-Stacking:", PiStackingParser()),
        "Disulfide Bridge": ("Disulfide Bridge:", DisulfideBridgeParser()),
        "Metal Coordination": ("Metal Coordination:", MetalCoordinationParser()),
        "Water Bridge": ("Water Bridge:", WaterBridgeParser()),
        "Halogen Bond": ("Halogen Bond:", HalogenBondParser()),
    }
    
    def __init__(self):
        self.structure = None
        self.results = {}
        self.current_section = None
        self.current_parser = None
    
    def process_file(self, filename):
        """Process the PLIP report file"""
        with open(filename, 'r') as file:
            for line in file:
                self._process_line(line.rstrip())
        return self.structure, self.results
    
    def _process_line(self, line):
        """Process a single line from the file"""
        # Capture structure info if not already set
        if not self.structure and line.startswith("Prediction of noncovalent interactions for PDB structure"):
            self.structure = line
            return
        
        # Check for section headers
        section_match = re.match(r"\*\*(.+?)\*\*", line)
        if section_match:
            self._handle_section_header(section_match.group(1).strip())
            return
        
        # Process data lines if in a known section
        if self.current_section and self.current_parser:
            self._process_data_line(line)
    
    def _handle_section_header(self, sec_title):
        """Handle a section header line"""
        if sec_title in self.SECTION_PARSERS:
            self.current_section = sec_title
            if self.current_section not in self.results:
                self.results[self.current_section] = []
            self.current_parser = self.SECTION_PARSERS[sec_title][1]
        else:
            self.current_section = None
            self.current_parser = None
    
    def _process_data_line(self, line):
        """Process a data line within a known section"""
        # Skip divider lines
        if (line.startswith('+') or not line.strip() or 
            set(line.strip()) <= set("-=")):
            return
        
        # Process table rows
        if line.startswith('|'):
            parts = PLIPRowParser.parse_table_row(line)
            if PLIPRowParser.is_data_row(parts):
                parsed = self.current_parser.parse(parts)
                if parsed:
                    self.results[self.current_section].append(parsed)


class PLIPReportPrinter:
    """Class for printing the parsed PLIP report results"""
    
    @staticmethod
    def print_results(structure, results, section_parsers):
        """Print the parsed results in a readable format"""
        if structure:
            print(f"PDB Structure: {structure}\n")
        
        # Define the order of sections to print
        section_order = [
            "Hydrogen Bonds",
            "Hydrophobic Interactions",
            "Salt Bridges",
            "pi-Cation Interactions",
            "Pi-Stacking",
            "Disulfide Bridge",
            "Metal Coordination",
            "Water Bridge",
            "Halogen Bond",
        ]
        
        for sec in section_order:
            if sec in results and results[sec]:
                title = section_parsers[sec][0]
                print(title)
                for row in results[sec]:
                    print(row)
                print()  # Blank line between sections


if __name__ == '__main__':
    # Example usage
    filename = "report.txt"
    
    # Parse the file
    parser = PLIPReportParser()
    structure, results = parser.process_file(filename)
    
    # Print the results
    PLIPReportPrinter.print_results(structure, results, PLIPReportParser.SECTION_PARSERS)