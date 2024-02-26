import os
import pandas as pd
from collections import defaultdict

# Certifique-se de que o CSV e o modelo HTML estão em UTF-8
dados = pd.read_csv('colaboradores_tecnoportas.csv', encoding='utf-8', sep=';')

# Ler o modelo de assinatura com UTF-8
with open('modelo-tecnoportas.html', 'r', encoding='utf-8') as file:
    modelo = file.read()

# Pasta de destino para as assinaturas
pasta_destino = 'assinaturas/tecnoportas/'
os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta se não existir

# Para controlar os nomes duplicados
contador_nomes = defaultdict(int)

# Processar cada colaborador
for index, row in dados.iterrows():
    # Pular linha se o nome for NaN (não um número ou dado ausente)
    if pd.isna(row['nome']):
        continue

    # Garantir que todos os valores são tratados como strings
    assinatura_atualizada = modelo.replace('{{nome}}', str(row['nome']))
    assinatura_atualizada = assinatura_atualizada.replace('{{cargo}}', str(row['cargo']))
    assinatura_atualizada = assinatura_atualizada.replace('{{telefones}}', str(row['telefones']))
    assinatura_atualizada = assinatura_atualizada.replace('{{email}}', str(row['email']))

    # Incrementar o contador para o nome e gerar um nome de arquivo único se necessário
    contador_nomes[row['nome']] += 1
    nome_arquivo = f"{row['nome'].replace(' ', '_')}_assinatura"
    if contador_nomes[row['nome']] > 1:
        nome_arquivo += f"_{contador_nomes[row['nome']]}"
    nome_arquivo = ''.join(e for e in nome_arquivo if e.isalnum() or e == '_')

    # Caminho completo do arquivo
    caminho_completo = os.path.join(pasta_destino, f"{nome_arquivo}.html")

    # Certifique-se de salvar os arquivos com UTF-8
    with open(caminho_completo, 'w', encoding='utf-8') as file:
        file.write(assinatura_atualizada)