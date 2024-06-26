import pandas as pd
import locale
import re

def read_file(filename):
    df = []

    try:
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
    except Exception:
        print(f'Error: Failed to read file \"{filename}\".')
        return pd.DataFrame()

def define_datatypes(df = pd.DataFrame()):
    if not df.empty:
        df['id'] = df['id'].astype(int)
        df['nome'] = df['nome'].astype(str)
        df['telefone'] = df['telefone'].astype(str)
        df['email'] = df['email'].astype(str)
        df['cnpj'] = df['cnpj'].astype(str)
        df['sgmento'] = df['sgmento'].astype(str)
        df['receita_anual'] = df['receita_anual'].astype(str)

    return df

def _validate_id(df):
    df['id'] = df['id'].str.strip()
    df = df[df['id'].str.isdigit()]

    return df

def _validate_nome(df):
    df['nome'] = df['nome'].str.strip()
    df = df[df['nome'].str.match(r'^[\w\s]+$', na=False)]

    return df

def _validate_telefone(df):
    df['telefone'] = df['telefone'].str.strip()
    df = df[df['telefone'].str.match(r'^(\(\d{2}\)) (\d{4,5})-(\d{4})$', na=False)]

    return df

def _validate_email(df):
    df['email'] = df['email'].str.strip()
    df['email'] = df['email'].str.lower()
    df = df[df['email'].str.match(r'^[a-z\d_\-]{1,64}@{1}[a-z\d]{1,64}.{1}[a-z]{2,4}$', na=False)]

    return df

def _validate_cnpj(df):
    df['cnpj'] = df['cnpj'].str.strip()
    df = df[df['cnpj'].str.len() == 14]
    df = df[df['cnpj'].str.isdigit()]

    for i in range(len(df['cnpj'])):
        res = re.search(r'^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$', df.at[i, 'cnpj'])
        if res:
            df.at[i, 'cnpj'] = '{}.{}.{}/{}-{}'.format(res.group(1), res.group(2), res.group(3), res.group(4), res.group(5))

    return df

def _validate_segmento(df):
    df['sgmento'] = df['sgmento'].str.strip()
    df = df[df['sgmento'].str.match(r'^[\w\s]+$', na=False)]

    return df

def _validate_receita_anual(df):
    df['receita_anual'] = df['receita_anual'].str.strip()
    df['receita_anual'] = df['receita_anual'].str.replace(',','.')
    df = df[df['receita_anual'].str.match(r'^(\d+).(\d+)$', na=False)]

    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

    for i in range(len(df['receita_anual'])):
        df.at[i, 'receita_anual'] = locale.currency(float(df.at[i, 'receita_anual']), grouping=True)

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

def main():
    df = []

    cliente = read_file('clientes.csv').astype(str)
    cliente2 = read_file('clientes2.csv').astype(str)
    if cliente.empty or cliente2.empty:
        print('Aborting...')
        return

    try:
        df = pd.merge(cliente, cliente2, on='id')
    except Exception:
        print('Error: Failed to merge files.')
        print('Aborting...')
        return

    del cliente
    del cliente2

    df.rename(columns={'segmento':'sgmento'}, inplace=True)

    filename = 'resultado.xlsx'
    try:
        xl = pd.read_excel(filename, dtype=str)
    except Exception:
        print(f'Error: Failed to read file \"{filename}\".')
        print('Aborting...')
        return

    df = define_datatypes(validate(df))
    xl = define_datatypes(xl)

    xl = pd.concat([xl, df], axis=0)
    del df

    xl.drop_duplicates(subset=['id'], keep='last', inplace=True)
    xl.sort_values(by='id', inplace=True)

    print(xl)

    try:
        xl.to_excel(filename, index=False)
    except Exception:
        print(f'Error: Failed to write file \"{filename}\".')
        print('Aborting...')
        return

if __name__ == '__main__':
    main()
