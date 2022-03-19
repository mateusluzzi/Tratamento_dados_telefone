import pandas as pd
import regex as re
import mysql.connector as connection

#################################################################
################ SETUP ##########################################
#################################################################

saida = r'' # caminho pra salvar CSV
col_telefone = 'telefone' # Nome da coluna que contem o número telefônico a ser tratado


## Opção 1 para uso de arquivo local, Opção 2 para uso de consulta (MySQL)
## 1. Uso de arquivo local
local_file = True # True para usar arquivo local, False para usar conexão do BD
file_path = r'' # caminho do arquivo local

## 2. Uso de consulta (MySQL)
query = ''' '''
host= ''
database= ''
user= ''
passwd= ''

######################### CÓDIGO ##############################
###############################################################

def tratar_telefone(df):
    colunas = []
    for x in df.columns:
        colunas.append(x)
    df['Telefone_original'] = df.Telefone
    df.Telefone = df.Telefone.apply(lambda x: '0' if x is None else re.sub('[^0-9]','',x)) ## Removendo caracteres não númericos
    df['Telefone_raw'] = df.Telefone
    df.Telefone = df.Telefone.apply(lambda x: '0' if x is None else '9'+x[-8:]) ## Adição de um dígito 9 antes dos últimos 8 dígitos
    df['Telefone_formatted'] = df.Telefone.apply(lambda x: '0' if x is None else x[0]+'.'+x[1:5]+'-'+x[-4:])
    df['Telefone_prefix'] = df.Telefone_raw.apply(lambda x: x[:-8]) 


    colunas_telefone = ['Telefone_original','Telefone_raw','Telefone','Telefone_formatted','Telefone_prefix']
    for x in colunas_telefone:
        colunas.append(x)


    df = df.loc[:,colunas].copy()

    df['Telefone_prefix2'] = df['Telefone_prefix'].apply(lambda x: re.sub('\A55|\A0','',x) if len(x)>2 else x)
    df['Telefone_prefix3'] = df['Telefone_prefix2'].apply(lambda x: x[:-1] if x[-1:] == '9' else x)
    df['Telefone_formatted'] = '(' + df['Telefone_prefix3'].apply(lambda x: x if len(x)==2 else 'XX') + ') ' + df['Telefone_formatted']
    df['Telefone_completo'] = df['Telefone_formatted'].apply(lambda x: re.sub('[^0-9]','',x))

    df['DDD'] = df['Telefone_prefix3'].apply(lambda x: x if len(x)==2 else None)
    del df['Telefone']
    df['Telefone'] = df['Telefone_completo'].apply(lambda x: x[-9:])
    df['Obs'] = df['Telefone_prefix3'].apply(lambda x: 'Entrada possivelmente incorreta' if len(x) != 2 else None)

    del df['Telefone_raw']
    del df['Telefone_formatted']
    del df['Telefone_prefix']
    del df['Telefone_prefix2']
    del df['Telefone_prefix3']

    ## Limpa as colunas de telefones nulos
    df.loc[df['Telefone_original'].isna(),['Telefone_completo','Telefone']] = [None,None]
    
    return df

if local_file:
    df = pd.read_csv(file_path)
else:
    conn = connection.connect(
    host,
    database,
    user, 
    passwd,
    use_pure=True
)
    df = pd.read_sql(query,conn)

df['Telefone'] = df[col_telefone]
del df[col_telefone]

df = tratar_telefone(df)

if len(saida) > 0:
    df.to_csv(saida)
else:
    print('Seu arquivo foi tratado. Acesse o objeto "df".')
