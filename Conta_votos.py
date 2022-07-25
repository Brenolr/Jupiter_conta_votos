import pandas as pd

def main():
    data = pd.read_csv('Arquivo_de_exemplo.csv')
    # print(data)
    votos = conta_votos(data)

    print("")
    for area in votos.keys():
        print("<<"+area+">>")
        votos[area] = dict(sorted(votos[area].items(), key=lambda item: item[1], reverse=True))
        total = 0
        for candidato in votos[area].keys():
            if(candidato!="Nulo" and candidato!="nan"):
                total += votos[area][candidato]
        for candidato in votos[area].keys():
            porcentagem = votos[area][candidato]/total*100
            print(candidato, end=": ")
            if(candidato!="Nulo" and candidato!="nan"):
                print(votos[area][candidato], end=", ")
                print("{:.2f}".format(porcentagem), end="%\n")
            else:
                print(votos[area][candidato], end="-\n")
        print("")


def conta_votos(data):
    votos_totais = {"Capitania": {},"Aero": {},"Rec": {},"Prop": {},"Eletro": {},"Paylaod": {},"Finan": {},"MKT": {},"RH": {},"Seguranca": {},}

    #percorre a lista para pegar cada membro (OBS: em Pandas vc o index e os dados da linha)
    for index, linha in data.iterrows():
        votos_totais = conta_por_membro(votos_totais, linha)
    return votos_totais

def conta_por_membro(votos, linha):
    
    #converte o nome das linhas o forms os nomes que estamos usando no programa
    areas = ["Aero","Rec","Prop","Eletro","Paylaod","Finan","MKT","Seguranca","RH"]
    nomes_forms_codigo = {"Capitania 🦸‍♀️":"Capitania","Aerodinâmica e Estruturas 🌌":"Aero","Recuperação 🪂": "Rec","Propulsão 🔥":"Prop", "Sistemas Eletrônicos 📡": "Prop","Cargas Experimentais 🛸":"Paylaod", "Financeiro 💰":"Finan", "Marketing 📸":"MKT"}
    
    #pega as areas do membro
    areas_do_membro = []
    for area in linha[2].split(";"):
        areas_do_membro.append(nomes_forms_codigo[area])
    
    if "Capitania" in areas_do_membro:
        capitania =  True
    else:
        capitania =  False

    #pega as comissoes 
    comissao_raw = linha[4]
    if comissao_raw == "Sim, sou da Segurança 🦺":
        areas_do_membro.append("Seguranca")
    elif comissao_raw == "Sim, sou dos Recursos Humanos 🗣":
        areas_do_membro.append("RH")
    elif comissao_raw == "Sim, sou dos Recursos Humanos 🗣 e da Segurança 🦺":
        areas_do_membro.append("Seguranca")
        areas_do_membro.append("RH")
    else:
        pass

        
    #pega a posição
    posicao_raw = linha[3]
    areas_do_gerente = []
    if posicao_raw == "Gerência/Capitania":
        gerencia = True
        verterano = True
        novato = False        
        if(len(areas_do_membro) >= 2):
            print("email digite a area dessa gerencia")
            sair = False
            while(sair == False):
                print("Capitania-0 Aero-1 Rec-2 Prop-3 Eletro-4 Paylaod-5 Finan-6 MKT-7 Seguranca-8 RH-9")
                print(areas_do_membro)
                print("Email do Gerente: " + linha[1])
                area_digitada = int(input("Digite a area do gerente: "))
                if(area_digitada!=0):
                    areas_do_gerente.append(areas[area_digitada-1])
                print("Esse gerente é gerente de mais uma area ?")
                print("1-Sim/2-Não, ")
                mais_de_uma_area = int(input("Sim ou Não:"))
                if(mais_de_uma_area!=1):
                    sair = True
        else:
            areas_do_gerente = areas_do_membro
    elif posicao_raw == "Membro Novo":
        gerencia = False
        verterano = False
        novato = True
    elif posicao_raw == "Membro Veterano":
        gerencia = False
        verterano = True
        novato = False
    
    if(areas_do_gerente != []):
        print(areas_do_gerente)
    
    #pega todos os votos
    votos_membro={"Capitania": linha[12],"Aero": linha[10],"Rec": linha[22],"Prop": linha[20],"Eletro": linha[24],"Paylaod": linha[14],"Finan": linha[16],"MKT": linha[18],"RH": linha[5],"Seguranca": linha[8],}

    if(capitania):
        votos["Capitania"] = voto_para_candidato(votos["Capitania"], votos_membro["Capitania"], 3)
    elif(gerencia):
        votos["Capitania"] = voto_para_candidato(votos["Capitania"], votos_membro["Capitania"], 2)
    else:
        votos["Capitania"] = voto_para_candidato(votos["Capitania"], votos_membro["Capitania"], 1)

    #voto outras areas
    # areas = ["Aero","Rec","Prop","Eletro","Paylaod","Finan","MKT","Seguranca","RH"]
    for area in areas:
        if(capitania):
            votos[area] = voto_para_candidato(votos[area], votos_membro[area], 3)
        elif(area in areas_do_membro):
            if(area in areas_do_gerente):
                votos[area] = voto_para_candidato(votos[area], votos_membro[area], 3)
            else:
                votos[area] = voto_para_candidato(votos[area], votos_membro[area], 2)
        else:
            votos[area] = voto_para_candidato(votos[area], votos_membro[area], 1)

    return(votos)

def voto_para_candidato(dict_area, canditato, n_votos):
    
    #por algumo motivo no começo nulo era literalmente semvalor
    if(pd.isnull(canditato)):
        canditato="Nulo"
    
    #Vê se existe se não adiciona
    if(canditato in dict_area):
        dict_area[canditato] += n_votos
    else:
        dict_area[canditato] = n_votos
    return(dict_area)

main()