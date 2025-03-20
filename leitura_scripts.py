import re

class LigacaoHidrogenio:
    def __init__(self, resnr, restype, reschain, resnr_lig, restype_lig, reschain_lig, sidechain, dist_h_a, dist_d_a, don_angle, protisdon, donoridx, donortype, acceptoridx, acceptortype, ligcoo, protcoo):
        self.resnr = resnr
        self.restype = restype
        self.reschain = reschain
        self.resnr_lig = resnr_lig
        self.restype_lig = restype_lig
        self.reschain_lig = reschain_lig
        self.sidechain = sidechain
        self.dist_h_a = dist_h_a
        self.dist_d_a = dist_d_a
        self.don_angle = don_angle
        self.protisdon = protisdon
        self.donoridx = donoridx
        self.donortype = donortype
        self.acceptoridx = acceptoridx
        self.acceptortype = acceptortype
        self.ligcoo = ligcoo
        self.protcoo = protcoo

    def __repr__(self):
        return f"{self.restype} {self.resnr} ({self.reschain}) - {self.restype_lig} {self.resnr_lig} ({self.reschain_lig})"

def parse_ligacoes_hidrogenio(linhas):
    ligacoes = []
    capturando = False  # Para saber quando estamos dentro da tabela

    for linha in linhas:
        linha = linha.strip()

        if "**Hydrogen Bonds**" in linha:
            capturando = True  # Começa a capturar dados a partir daqui
            continue
        
        if capturando:
            if linha.startswith("+"):  # Linha delimitadora da tabela
                continue
            
            partes = linha.split("|")
            if len(partes) < 17:  # Verifica se é uma linha válida de interação
                continue

            try:
                # Remove espaços extras e extrai os valores
                resnr = int(partes[1].strip())
                restype = partes[2].strip()
                reschain = partes[3].strip()
                resnr_lig = int(partes[4].strip())
                restype_lig = partes[5].strip()
                reschain_lig = partes[6].strip()
                sidechain = partes[7].strip() == "True"
                dist_h_a = float(partes[8].strip())
                dist_d_a = float(partes[9].strip())
                don_angle = float(partes[10].strip())
                protisdon = partes[11].strip() == "True"
                donoridx = int(partes[12].strip())
                donortype = partes[13].strip()
                acceptoridx = int(partes[14].strip())
                acceptortype = partes[15].strip()
                ligcoo = partes[16].strip()
                protcoo = partes[17].strip()

                ligacao = LigacaoHidrogenio(resnr, restype, reschain, resnr_lig, restype_lig, reschain_lig, sidechain, dist_h_a, dist_d_a, don_angle, protisdon, donoridx, donortype, acceptoridx, acceptortype, ligcoo, protcoo)
                ligacoes.append(ligacao)

            except ValueError:
                # Ignora linhas que não seguem o formato esperado
                continue
    
    return ligacoes

# Testando a função
with open("report.txt", "r") as file:
    linhas = file.readlines()

ligacoes_hidrogenio = parse_ligacoes_hidrogenio(linhas)

# Exibindo as ligações extraídas
for lig in ligacoes_hidrogenio:
    print(lig)
