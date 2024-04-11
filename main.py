import pandas as pd
import re

def read_file(filename):
    df = []
    with open(filename, 'r') as file:
        lines = file.readlines()

        header = lines[0].strip().split(',')

        for line in lines[1:]:
            values = line.strip().split(',')

            if len(values) > len(header):
                values[len(header) - 1] = ','.join(values[len(header) - 1:])
                values = values[:len(header)]
            df.append(values)
    return pd.DataFrame(df, columns=header)

def define_datatypes(df = pd.DataFrame()):
    if not df.empty:
        df['id'] = df['id'].astype(int)
        df['nome'] = df['nome'].astype(str)
        df['telefone'] = df['telefone'].astype(str)
        df['email'] = df['email'].astype(str)
        df['cnpj'] = df['cnpj'].astype(str)
        df['sgmento'] = df['sgmento'].astype(str)
        df['receita_anual'] = df['receita_anual'].astype(float)
    return df

def _validate_id(df):
    df['id'] = df['id'].astype(str).str.strip()
    df = df[df['id'].astype(str).str.isdigit()]
    return df

def _validate_nome(df):
    df['nome'] = df['nome'].astype(str).str.strip()
    df = df[df['nome'].astype(str).str.match(r'^[a-zA-Zãáàéóõôç\s]+$', na=False)]
    return df

def _validate_telefone(df):
    df['telefone'] = df['telefone'].astype(str).str.strip()
    df = df[df['telefone'].astype(str).str.match(r'^(\([0-9]{2}\)) {1}([0-9]{4,5})-{1}([0-9]{4})$', na=False)]
    return df

def _validate_email(df):
    df['email'] = df['email'].astype(str).str.strip()
    df = df[df['email'].astype(str).str.match(r'^[a-z0-9_\-]{1,64}@{1}[a-z0-9]{1,64}.{1}[a-z]{2,4}$', na=False)]
    return df

def _validate_cnpj(df):
    df['cnpj'] = df['cnpj'].astype(str).str.strip()
    df = df[df['cnpj'].astype(str).str.len() == 14]
    df = df[df['cnpj'].astype(str).str.isdigit()]
    return df

def _validate_segmento(df):
    df['sgmento'] = df['sgmento'].astype(str).str.strip()
    df = df[df['sgmento'].astype(str).str.match(r'^[a-zA-Zãáàéóõôç\s]+$', na=False)]
    return (df)

def _validate_receita_anual(df):
    df['receita_anual'] = df['receita_anual'].astype(str).str.strip()
    df = df[df['receita_anual'].astype(str).str.match(r'^[0-9]+$', na=False)]
    return df

def validate(df = pd.DataFrame()):
    if not df.empty:
        df.dropna()
        df = _validate_id(df)
        df = _validate_nome(df)
        df = _validate_telefone(df)
        df = _validate_email(df)
        df = _validate_cnpj(df)
        df = _validate_segmento(df)
        df = _validate_receita_anual(df)
    return df

df = read_file('clientes.csv')
df2 = read_file('clientes2.csv')

df = pd.merge(df, df2, on='id')

df.rename(columns={'segmento':'sgmento'}, inplace=True)

xl = pd.read_excel('resultado.xlsx', dtype=str)

df = define_datatypes(validate(df))
xl = define_datatypes(xl)

xl = pd.concat([xl, df], axis=0)

xl.drop_duplicates(subset='id', keep='last', inplace=True)
print(xl)

xl.to_excel('resultado.xlsx', index=False)
