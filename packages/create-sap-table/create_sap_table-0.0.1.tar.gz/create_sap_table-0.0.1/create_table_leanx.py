import requests
from bs4 import BeautifulSoup

# data types description found at https://www.ibm.com/docs/en/iis/11.3?topic=types-sql-syntax-data-values
data_types = {
    'ACCP' : 'TIMESTAMP',
    'CHAR' : 'VARCHAR(254)',
    'CLNT' : 'VARCHAR(20)',
    'CUKY' : 'VARCHAR(20)',
    'CURR' : 'FLOAT',
    'DATS' : 'TIMESTAMP',
    'DEC' : 'FLOAT',
    'FLTP' : 'FLOAT',
    'INT1' : 'SMALLINT',
    'INT2' : 'MEDIUMINT',
    'INT4' : 'INT',
    'LANG' : 'VARCHAR(20)',
    'LCHR' : 'VARCHAR(20)',
    'LRAW' : 'VARCHAR(20)',
    'NUMC' : 'FLOAT',
    'QUAN' : 'FLOAT',
    'RAW' : 'VARBINARY(254)',
    'TIMS' : 'TIMESTAMP',
    'UNIT' : 'VARCHAR(20)',
}


def fetch_table(table_name: str):
    # validate
    table_name = table_name.strip()
    table_name = table_name.lower()

    url = f"https://www.leanx.eu/en/sap/table/{table_name}.html"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # get table by class name, change class name if neccessary
    # built for the class name and html structure on October 5, 2023
    table = soup.find('table', attrs={'class':'table table-condensed table-striped'})
    table_body = table.find('tbody')
    rows = table_body.findAll(lambda tag: tag.name=='tr')

    data = []
    for row in rows:
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.text)
        
        # to avoid tables under 'possible value' button
        if len(row_data) >= 6:
            data.append(row_data)

    fileds = []
    for d in data:
        fileds.append([d[0], d[4]])
    
    assert len(fileds) > 0, f'No fields returned for the given table name `{table_name}`. Please check if the table exists on https://www.leanx.eu/en/sap/table/search. If problem persists, please get in touch @n.basaye'
    return fileds

def write_query(table_name: str, fileds: list):
    # validate
    table_name = table_name.strip()
    table_name = table_name.upper()

    query_data_types = ''
    for f in fileds:
        query_data_types += f"{f[0]} {data_types[f[1]]}, \n\t"

    # query_data_types ends with ', \n' so '_CELONIS_CHANGE_DATE TIME' is being added to a new line
    query = f"DROP TABLE IF EXISTS {table_name};\n"
    query += f"CREATE TABLE {table_name} (\n"
    query += f"\t{query_data_types}_CELONIS_CHANGE_DATE TIME\n);"

    with open(f'create_{table_name}.sql', 'w') as f:
        try:
            f.write(query)
            print(f"Script generated successfully. File create_{table_name}.sql created.")
        except:
            print("Failed, please check if the table exists on https://www.leanx.eu/en/sap/table/search. If problem persists, please get in touch @n.basaye")

def get_query(table_name: str):
    fields = fetch_table(table_name=table_name)
    write_query(table_name=table_name, fileds=fields)