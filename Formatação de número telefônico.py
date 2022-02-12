########################## - CONFIGURACAO - #############################




## Output do arquivo em CSV
output = r'C:\Users\telefones.csv'

## Lista de numeros telefonicos a serem tratados
telefones = ['11 99999999','+55(51)9999-9999','(21)9.9543-2100','554198765432']




############################ - CODIGO - ###############################
import pandas as pd
import regex as re



df = pd.DataFrame(
    {'Telefone':telefones})



## Salvando telefone original
df['Telefone_original'] = df.Telefone

## Removendo caracteres nao numericos
df.Telefone = df.Telefone.apply(lambda x: re.sub('[^0-9]','',x))

## Guardando telefone "raw" apos excluir caracteres nao numericos
df['Telefone_raw'] = df.Telefone

## Adicao de um digito 9 antes dos ultimos 8 digitos
df.Telefone = df.Telefone.apply(lambda x: '9'+x[-8:])

## Formatando telefone para melhor apresentacao visual
df['Telefone_formatted'] = df.Telefone.apply(lambda x: x[0]+'.'+x[1:5]+'-'+x[-4:])

## Guardando os prefixos do telefone (todos digitos antes dos ultimos 8 digitos que formam a base do numero telefonico)
df['Telefone_prefix'] = df.Telefone_raw.apply(lambda x: x[:-8])




df = df.loc[:,['Telefone_original','Telefone_raw','Telefone','Telefone_formatted','Telefone_prefix']].copy()
df['Telefone_prefix2'] = df['Telefone_prefix'].apply(lambda x: re.sub('\A55|\A0','',x) if len(x)>2 else x)
df['Telefone_prefix3'] = df['Telefone_prefix2'].apply(lambda x: x[:-1] if x[-1:] == '9' else x)
df['Telefone_formatted'] = '(' + df['Telefone_prefix3'].apply(lambda x: x if len(x)==2 else 'XX') + ') ' + df['Telefone_formatted']
df['Obs'] = df['Telefone_prefix3'].apply(lambda x: 'Entrada possivelmente incorreta' if len(x) != 2 else None)



## Reorganizando dataframe

df['Telefone_formatado'] = df['Telefone_formatted']
df['DDD_Telefone'] = df['Telefone_formatado'].apply(lambda x: re.sub('[^0-9XX]','',x))
df['DDD'] = df['Telefone_prefix3'].apply(lambda x: x if len(x)==2 else None)
df['Telefone'] = df['Telefone']
del df['Telefone_raw']
del df['Telefone']
del df['Telefone_formatted']
del df['Telefone_prefix']
del df['Telefone_prefix2']
del df['Telefone_prefix3']


df.to_csv(output)





