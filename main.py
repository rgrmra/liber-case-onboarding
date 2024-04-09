import pandas as pd

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

df = read_file("clientes.csv")
df2 = read_file("clientes2.csv")
#print(df)
#print(df2)
df = pd.merge(df, df2, on="id") 

df.rename(columns={"segmento":"sgmento"}, inplace=True)
#print(df.head(10))

xl = pd.read_excel("resultado.xlsx")
xl = pd.concat([xl, df], axis=0)
print(xl)
xl = xl.drop_duplicates(subset=['email'], keep="first")
print(xl)

xl.to_excel("resultado.xlsx", index=False)
