import os, requests, json, time, re
from datetime import date, datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from urllib.request import urlretrieve
import urllib.parse
import site

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from ahk import AHK
# ahk = AHK(executable_path='C:\\Program Files\\AutoHotkey\\AutoHotkey.exe')
ahk = AHK()


user_site_packages = site.getusersitepackages()
user_site_packages = user_site_packages.replace('Roaming', 'Local\\Programs').replace('site-packages','Lib\\site-packages')

db_fluid ='fluid'
ip_planning = str(os.getenv('ip_planning'))
user_planning = str(os.getenv('user_planning'))
pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning')))
sql = f"SELECT * FROM rpa_cofre_senhas"
con = create_engine(f'mysql+mysqlconnector://{user_planning}:{pw_bd_planning}@{ip_planning}/{db_fluid}', pool_recycle=3600)
df_cred = pd.read_sql_query(sql, con)
try:
    con.dispose()
except:
    pass
    
    


def gerador_pwd(palavra_chave:str, select_atributo:str ='usuario', print_atributo=False, retornar_chaves=False, base:pd.DataFrame =df_cred):
    '''
    usuario = gerador_pwd('fluid', 'usuario')\n
    print(usuario)\n
    '''
    import os
    import socket
    from cryptography.fernet import Fernet 
    import site
    user_site_packages = site.getusersitepackages()
    user_site_packages = user_site_packages.replace('Roaming', 'Local\\Programs').replace('site-packages','Lib\\site-packages')
    palavrachave = str(palavra_chave)

    p0 = os.getenv('userdomain')
    p1 = p0
    p2 = socket.gethostname()
    p3 = socket.gethostbyname(p2)

    p3 = p3[::-1]
    p3 = p3.replace('.','')[-6:]
    p1 = p1[0]
    if os.path.exists('c:\\temp\\'): p2 = p0[1:]
    p4 = str(socket.getfqdn()[-14:]).replace('.','')
    p5 = os.name
    p6 = ''
    if '2192' in p3: p3 = p3.replace('2192', '2213')
    for x in p4: p6 = p6 + str(ord(x))
    key = '2'+ ((p1 + p2)[::-1] * (2^3)) + (p3) + p4 + p6[:7] + p5 + ((p2[::-1])[:3]) + '__' + ((p2[::-1])[:3]).capitalize() + '='
    
    file = open(f'{user_site_packages}\\rpa_coop\\img\\hash', 'r')
    hash = file.read()
    file.close
    fernet = Fernet(key) 
    msg_encripted = hash
    msg = bytes(msg_encripted, "utf-8") 
    hash_validador = fernet.decrypt(msg).decode("utf-8")
    
    
    if retornar_chaves:
        base = base[['usuario', 'palavra_chave', 'sistema', 'tipo']]
        return base[['palavra_chave', 'sistema']]
    else:  
        base["palavra_chave"] = base["palavra_chave"].astype('str')
        df = base[base["palavra_chave"].str.contains(palavrachave)]
        # res = df[select_atributo].values[0]
        # print(df)
        credencial_atributos = {}
        df = df.drop(columns='id')
        valor = df.iloc[0,:].apply(str).values
        valor = str(valor[1])
        fernet = Fernet(hash_validador) 
        msg_encripted = valor
        msg = bytes(msg_encripted, "utf-8") 
        try:
            valor = fernet.decrypt(msg).decode("utf-8")
            df['senha'] = valor
        except:
            pass
        credencial_atributos = df.to_dict(orient='records')
        credenciais = credencial_atributos[0]
        valor = credenciais.get(select_atributo)
        result = f'{select_atributo} : {valor}'
        if print_atributo: print(result)
    return valor


class Adobe:
    # https://secure.na1.adobesign.com/public/docs/restapi/v6#://
    def __init__(self):
        self.token_api_adobe = str(gerador_pwd('api_adobe', 'senha'))
        self.url_api_adobe = str(gerador_pwd('api_adobe', 'ip_host'))
        
        
    def alterar_status_usuario(self, email_usuario: str, status_usuario: str = 'INACTIVE'):
        '''status_usuario: ACTIVE, INACTIVE'''
        token_get_user = self.token_api_adobe
        url = f'{self.url_api_adobe}users'
        headers = { "Authorization": f"{token_get_user}"}
        response = requests.get(url, headers=headers)
        df = pd.DataFrame(response.json()['userInfoList'])
        for x in df.itertuples():
            if str(x.email) == str(email_usuario):
                id_usuario = str(x.id)
                break
            else:
                id_usuario = 'Não encontrado'

        if id_usuario == 'Não encontrado': raise Exception('Usuário não encontrado')
        url = f'{self.url_api_adobe}users/{id_usuario}/state'
        headers = { "Authorization": f"{token_get_user}"}
        body = {"state": f"{status_usuario}", "comment": "desativado por rpa"}
        response = requests.put(url, headers=headers, json=body)
        return response
    
    
    def criar_usuario_adobe(self, email: str, nome_completo: str, cod_agencia: str, user_admin = False, status = 'ACTIVE', company = 'SICREDI', accountType = 'ENTERPRISE'):  
        '''criar_usuario_adobe(email, nome_completo, cod_agencia)'''
        groupName = '0718_' + cod_agencia  
        id_adobe = str(email.split('@')[0])
        primeiro_nome = str(nome_completo.split(' ')[0]) 
        try:    ultimo_nome = str(nome_completo.split(' ')[1]) + ' ' + str(nome_completo.split(' ')[2])
        except: ultimo_nome = str(nome_completo.split(' ')[1])
        
        hoje = datetime.now().strftime('%d-%m-%Y')
        h = { "Authorization": f"{self.token_api_adobe}"}
        
        url = f'{self.url_api_adobe}groups'
        res1 = requests.get(url, headers=h) # get grupos
        r1 = res1.status_code
        
        if r1 == 200:
            df = pd.DataFrame(res1.json()['groupInfoList'])
            df = df[df['groupName'] == groupName]
            id_grupo = str(df['groupId'].values[0])
            
            url = f'{self.url_api_adobe}users'    
            body = { 
                    "accountType": accountType,
                    "email": email,
                    "id": id_adobe,
                    "isAccountAdmin": user_admin,
                    "status": status,
                    "company": company,
                    "createdDate": hoje,
                    "firstName": primeiro_nome,
                    "lastName": ultimo_nome,
                    "locale": "BR",
                    "primaryGroupId": id_grupo,
                    }

            res2 = requests.post(url, headers=h, json=body)
            r2 = res2.status_code
            if r2 == 201:  
                print('USUARIO ADOBE CRIADO COM SUCESSO')
                print(res2.text)
            elif r2 == 409:
                print('OPS. O USUARIO ADOBE COM O EMAIL ESPECIFICADO JA EXISTE')
            else:
                print('ERRO AO TENTAR CRIAR USUARIO ADOBE VIA API')
                print(res2.text)
                raise Exception('Erro ao tentar criar usuario via api da adobe')
            return res2.status_code
        else:
            raise Exception('Erro ao consultar a api da adobe, para pegar grupos de usuarios')
        
                
class Dados:
    
    def __init__(self):
        self.ip_planning = str(os.getenv('ip_planning'))
        self.user_planning = str(os.getenv('user_planning'))
        self.pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning'))) 
        
        self.user_planning_controles = str(gerador_pwd('user_planning_controles', 'senha'))
        self.pw_planning_controles = str(gerador_pwd('pw_planning_controles', 'senha'))
        
        self.ip_grafana = str(gerador_pwd('grafana', 'ip_host'))
        self.user_grafana = str(gerador_pwd('grafana', 'usuario'))
        self.pw_bd_grafana = str(urllib.parse.quote_plus(gerador_pwd('grafana', 'senha')))
        
        self.ip_sistema_senhas = str(gerador_pwd('sistema_senhas', 'ip_host'))
        self.user_sistema_senhas = str(gerador_pwd('sistema_senhas', 'usuario'))
        self.database_sistema_senhas = str(gerador_pwd('sistema_senhas', 'db_name'))
        self.pw_bd_sistema_senhas = str(urllib.parse.quote_plus(gerador_pwd('sistema_senhas', 'senha')))
        
        self.ip_db_sapiens = str(gerador_pwd('pw_bd_sapiens', 'ip_host'))
        self.db_sapiens = str(gerador_pwd('pw_bd_sapiens', 'db_name'))
        self.pw_db_sapiens = str(gerador_pwd('pw_bd_sapiens', 'senha'))
        self.user_db_sapiens = str(gerador_pwd('pw_bd_sapiens', 'usuario'))
        
        self.ip_denodo = str(gerador_pwd('denodo_web', 'ip_host'))
        self.user_denodo = str(gerador_pwd('denodo_web', 'usuario'))
        self.pw_denodo = str(urllib.parse.quote_plus(gerador_pwd('denodo_web', 'senha')))
        
        self.token_api_denodo = str(gerador_pwd('token_api_denodo', 'senha'))
        self.url_api_denodo = str(gerador_pwd('token_api_denodo', 'ip_host'))
        
        # self.user_plat_atend = str(gerador_pwd('contacorrente', 'usuario'))
        # self.senha_plat_atend = str(urllib.parse.quote_plus(gerador_pwd('contacorrente', 'senha')))
        # self.name_plat_atend = str(gerador_pwd('contacorrente', 'db_name'))
        # self.ip_plat_atend = str(gerador_pwd('contacorrente', 'ip_host'))
        # self.porta_plat_atend = str(gerador_pwd('contacorrente', 'porta'))

        
    def criar_engine(self, db:str, user_db='user_opcional', password_db='senha_opcional', ip_ou_host_db='ip_host_opcional', porta='3306', library_sql='mysqlconnector'):
        '''
        retorna conexao com db, db='parametro_obrigatorio' \n
        schema planinng: db = ('planning', 'fluid', 'cronos', 'controles_internos') \n
        schema sistema_senhas: db = 'sistema_senhas' \n
        schema grafana: db = 'grafana' \n
        schema denodo: db = ('ldw', 'seguros', 'cooperativa', 'auditoria_7000') \n
        '''
        if (db == 'planning') or (db == 'fluid') or (db == 'cronos') or (db == 'controles_internos') or (db == 'bok_credito') or (db == 'pufv') or (db == 'boas_vindas'):
            if db == 'controles_internos':
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning_controles}:{self.pw_planning_controles}@{self.ip_planning}/{db}', poolclass=NullPool, pool_recycle=3600)
            else:
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', poolclass=NullPool, pool_recycle=3600)
        elif (db == 'ldw') or (db == 'seguros') or (db == 'cooperativa') or (db == 'auditoria_7000') or (db == 'deploy_auditoria_7000_ci'):
            conexao = create_engine(f'denodo://{self.user_denodo}:{self.pw_denodo}@{self.ip_denodo}:9996/{db}')
        elif (db == 'grafana'):
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_grafana}:{self.pw_bd_grafana}@{self.ip_grafana}/{db}', poolclass=NullPool)
        elif (db == 'sistema_senhas'):
            banco = self.database_sistema_senhas
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_sistema_senhas}:{self.pw_bd_sistema_senhas}@{self.ip_sistema_senhas}:3307/{banco}', poolclass=NullPool)
        elif (db == 'sapiens') or (db == 'sap') or (db == 'fiori'):
            conexao = create_engine(f"mssql+pymssql://{self.user_db_sapiens}:{self.pw_db_sapiens}@{self.ip_db_sapiens}")
        elif (db == 'contacorrente'):
            # plataforma de atendimento
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_plat_atend}:{self.senha_plat_atend}@{self.ip_plat_atend}/{self.name_plat_atend}', poolclass=NullPool, pool_recycle=3600)
        else:
            conexao = create_engine(f'mysql+{library_sql}://{user_db}:{password_db}@{ip_ou_host_db}:{porta}/{db}', poolclass=NullPool)
        return conexao
            
                         
    def criar_conexao(self, db:str, user_db='user_opcional', password_db='senha_opcional', ip_ou_host_db='ip_host_opcional', porta='3306', library_sql='mysqlconnector'):
        '''
        retorna conexao com db, db='parametro_obrigatorio' \n
        schema planinng: db = ('planning', 'fluid', 'cronos', 'controles_internos') \n
        schema sistema_senhas: db = 'sistema_senhas' \n
        schema grafana: db = 'grafana' \n
        schema denodo: db = ('ldw', 'seguros', 'cooperativa', 'auditoria_7000') \n
        '''
        if (db == 'planning') or (db == 'fluid') or (db == 'cronos') or (db == 'controles_internos') or (db == 'bok_credito') or (db == 'pufv') or (db == 'boas_vindas'):
            if db == 'controles_internos':
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning_controles}:{self.pw_planning_controles}@{self.ip_planning}/{db}', pool_recycle=3600)
            else:
                conexao = create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', pool_recycle=3600)
        elif (db == 'ldw') or (db == 'seguros') or (db == 'cooperativa') or (db == 'auditoria_7000'):
            conexao = create_engine(f'denodo://{self.user_denodo}:{self.pw_denodo}@{self.ip_denodo}:9996/{db}')
        elif (db == 'grafana'):
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_grafana}:{self.pw_bd_grafana}@{self.ip_grafana}/{db}')
        elif (db == 'sistema_senhas'):
            banco = self.database_sistema_senhas
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_sistema_senhas}:{self.pw_bd_sistema_senhas}@{self.ip_sistema_senhas}:3307/{banco}')
        elif (db == 'sapiens') or (db == 'sap') or (db == 'fiori'):
            conexao = create_engine(f"mssql+pymssql://{self.user_db_sapiens}:{self.pw_db_sapiens}@{self.ip_db_sapiens}")
        elif (db == 'contacorrente'):
            # plataforma de atendimento
            conexao = create_engine(f'mysql+mysqlconnector://{self.user_plat_atend}:{self.senha_plat_atend}@{self.ip_plat_atend}/{self.name_plat_atend}', pool_recycle=3600)
        else:
            conexao = create_engine(f'mysql+{library_sql}://{user_db}:{password_db}@{ip_ou_host_db}:{porta}/{db}')
        return conexao
            
        
    def api_consulta_denodo(self, database:str, tabela:str, colunas:str, filtro_where="opcional"):
        '''
        filtro = "coluna2 eq 'SIM' and coluna3 eq 'Ativo'" \n
        df = dados.api_consulta_denodo('ldw', 'nome_da_tabela', 'coluna1, coluna5', filtro) \n\n
        
        # operadores para filtro where: \n
        eq = igual \n
        lt = menor que \n
        le = menor ou igual \n
        ne = diferente \n
        ge = maior ou igual \n
        gt = maior que \n       
        
        '''
        df = pd.DataFrame()
        requests.packages.urllib3.disable_warnings()
        if filtro_where == "opcional":
            url = f"{self.url_api_denodo}/{database}/views/{tabela}?$select={colunas}"
        else:
            url = f"{self.url_api_denodo}/{database}/views/{tabela}?$select={colunas}&$filter={filtro_where}"
        payload={}
        headers = {'Accept': 'application/xhtml+xml;q=0.9,application/json', 'Authorization': self.token_api_denodo}
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        # print(response.text.encode('utf8'))
        rows = json.loads(response.content)
        try:
            df = pd.DataFrame(rows['elements'])
        except:
            print('erro ao converter para DataFrame, json retornou: \n', response.text.encode('utf8'))
        return df   
        
     
    def consultar_banco_dados(self, conexao_engine, query_sql:str, retorna_DataFrame=True):
        '''
        retorna um DataFrame pandas \n
        exemplo de query: \n
        SELECT * FROM rpa_historico WHERE cod_rpa = "3000" \n
        '''
        if retorna_DataFrame:
            df_rows = pd.read_sql_query(query_sql, conexao_engine)
        else:
            df_rows = conexao_engine.execute(query_sql)
        return df_rows
    
    
    def select_banco_dados(self, conexao_engine, query_sql:str, retorna_DataFrame=True):
        '''
        retorna um DataFrame pandas \n
        exemplo de query: \n
        SELECT * FROM rpa_historico WHERE cod_rpa = "3000" \n
        '''
        if retorna_DataFrame:
            df_rows = pd.read_sql_query(query_sql, conexao_engine)
        else:
            df_rows = conexao_engine.execute(query_sql)
        return df_rows

           
    def update_banco_dados(self, conexao_engine, query_sql):
        '''
        realizar update na tabela do banco de dados \n
        exemplo de query: \n
        "UPDATE rpa_fila SET nome_rpa = 'teste_01' WHERE id_fila = 9161" \n
        '''
        conexao_engine.execute(query_sql)
        
        
    def insert_banco_dados(self, conexao_engine, query_sql):
        '''
        realiza insert na tabela do banco de dados \n
        exemplo de query: \n
        "INSERT INTO rpa_fila(cod_rpa, nome_rpa, status) VALUES (6001, NULL, 'novo')" \n
        OBS. passar todas as colunas, exceto a primmeira caso seja auto-incremento
        '''
        conexao_engine.execute(query_sql)
                
        
    def insert_DataFrame_to_db(self, df, engine, nome_da_tabela:str, if_existir='append', mostrar_index=False):
        df.to_sql(nome_da_tabela, engine, if_exists=if_existir, index = mostrar_index)
        print('Inserção realizada com sucesso')


    def delete_linhas_banco_dados(self, conexao_engine, query_sql):
        '''
        realiza delete na tabela do banco de dados \n
        exemplo de query: \n
        "DELETE FROM rpa_fila WHERE id_fila = 9161" \n
        '''
        aux_query = str(query_sql).upper()
        if 'WHERE' in aux_query:
            conexao_engine.execute(query_sql)
            print('Exclusão realizada com sucesso')
        else:
            print('Não foi possível realizar a exclusão, é necessário informar o WHERE na query')
            

class Fluid:
    
    def __init__(self):
        
        self.id_usuario = str(gerador_pwd('fluid_cod_user', 'senha'))
        self.token_fluid = str(gerador_pwd('token_api_fluid', 'senha'))
        self.organizacao = str(gerador_pwd('fluid_organizacao', 'senha'))
        self.headers = {'organization': self.organizacao,'authorization': self.token_fluid}
        self.url_api = str(gerador_pwd('fluid_url_api', 'senha'))
        self.url_fluid = str(gerador_pwd('fluid_url_request', 'senha'))
        self.user_fluid = str(gerador_pwd('fluid_user_web', 'senha'))
        self.senha_fluid = str(gerador_pwd('usuario_fluid', 'senha'))
        
        self.token_fluid_v2 = str(gerador_pwd('token_api_fluid_v2', 'senha'))
        self.organizacao_v2 = str(gerador_pwd('token_api_fluid_v2', 'usuario'))
        self.url_api_v2 = str(gerador_pwd('token_api_fluid_v2', 'ip_host'))
        
        self.ip_planning = str(os.getenv('ip_planning'))
        self.user_planning = str(os.getenv('user_planning'))
        self.pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning'))) 
        
        
    def cancelar_processos_fluid(self, cod_processo:str|int, motivo:str):
        processo = int(str(cod_processo).replace('.0', '').replace('.', ''))
        motivo = str('Demanda aberta no caminho incorreto')

        headers = {'organization': self.organizacao_v2,'authorization': self.token_fluid_v2}
        payload = {'processos': [processo], 'parecer_cancelamento': motivo}

        url = f'{self.url_api_v2}/process/cancel'
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200:
            print('Processo(s) cancelado(s) com sucesso')
        else:
            print('Erro ao cancelar o processo')
            print(response.text)
            raise Exception(f'Erro ao cancelar o processo {cod_processo} via api fluid')
        return response
               
               
    def anexar_arquivo_fluid(self, cod_processo:str, path_file:str, tipo_arquivo:str):
        '''
            num_processo = '497305'\n
            path_file = 'C:\\Temp\\teste.xlsx'\n
            id_doc_fluid = '417'\n
            api_upload_anexo_fluid( num_processo, path_file, id_doc_fluid )
        '''
        nome_arquivo = os.path.basename(path_file).split('/')[-1]
        url = f'{self.url_api}/processos/anexar' 
        payload = {"processo": cod_processo, "nome": nome_arquivo, "tipo": tipo_arquivo}
        res_fase1 = requests.request("POST", url, json=payload, headers=self.headers)
        time.sleep(10)
        cod_res_api = str(res_fase1.status_code)
        if cod_res_api != '200':
            raise Exception(f'Erro ao preparar anexo fluid, processo: {cod_processo}')
        
        payload = res_fase1.json()
        url = payload['url']
        response = requests.post(url, files={
                                            "AWSAccessKeyId": payload['fields'][0]['AWSAccessKeyId'],
                                            "key": payload['fields'][0]['key'],
                                            "policy": payload['fields'][0]['policy'],
                                            "signature": payload['fields'][0]['signature'],
                                            "file": open(path_file, "rb")})
        time.sleep(10)
        cod_res_api = str(response.status_code)

        # observacao, os time.sleep(10) sao uma segurança para não protocolar antes de terminar o upload e corromper o arquivo.
        # caso o arquivo seja muito grande pode ir testando com uma espera maior, ou fazer um if de espera por tamanho de arquivo.
        time.sleep(10)
        if cod_res_api != '204':
            raise Exception(f'Erro ao anexar arquivo no fluid, processo: {cod_processo}')
        else:
            print(f'Arquivos anexados com sucesso no processo: {cod_processo}')
            return cod_res_api
        
        
    def ler_dados_de_excel_no_fluid(self, num_processo: str):
        endpoint = f"{self.url_api}/processos/download"
        data = json.dumps({"hashs":[], "processo": num_processo})
        res_dicionario = requests.post(url=endpoint, data=data, headers=self.headers, verify=True)
        print("Get_link anexos fluid: ", res_dicionario.status_code)
        if str(res_dicionario.status_code) == '200':
            res_json = res_dicionario.json()
            url = res_json[0]['url']
            response = requests.get(url)
            time.sleep(1)
            df  = pd.read_excel(response.content)
            print(df)
            return df
    
    
    def download_anexo_fluid(self, num_processo: str):
        endpoint = f"{self.url_api}/processos/download"
        data = json.dumps({"hashs":[], "processo": num_processo})
        res_dicionario = requests.post(url=endpoint, data=data, headers=self.headers, verify=True)
        print("Get_link anexos fluid: ", res_dicionario.status_code)
        if str(res_dicionario.status_code) == '200':
            res_json = res_dicionario.json()
            url = res_json[0]['url']
            print()
            destino = f'c:\\temp\\planilha_anexo_fluid.xlsx'
            urlretrieve(url, destino)
            time.sleep(5)
            print('baixou o arquivo:', destino)
            return destino
        else:
            destino = 'arquivo nao encontrado para download'
            print(destino)
            return destino
        
        
    def download_multiplos_anexos_fluid(self, num_processo: str, pasta_destino: str):       
        endpoint = f"{self.url_api}/processos/download"
        data = json.dumps({"hashs":[], "processo": num_processo})
        res_dicionario = requests.post(url=endpoint, data=data, headers=self.headers, verify=True)
        print("Get_link anexos fluid: ", res_dicionario.status_code)
        if str(res_dicionario.status_code) == '200':
            res_json = res_dicionario.json()
            print()
            df_files = pd.DataFrame(res_json)
            if '\\' in pasta_destino[-1]:   
                os.system(f'mkdir {pasta_destino}anexos_processo_{num_processo}')
                destino = f'{pasta_destino}anexos_processo_{num_processo}'   
            else:    
                os.system(f'mkdir {pasta_destino}\\anexos_processo_{num_processo}')  
                destino = f'{pasta_destino}\\anexos_processo_{num_processo}\\'
            files = os.listdir(destino)  
            [os.remove(f'{destino}{file}') for file in files]
            time.sleep(5)
            new_files = []
            df_files = df_files[['nome','url']]
            print(df_files)
            
            for nome, url in df_files.values:
                loc = url.find('?')
                extensao = url[loc-4:loc].replace('.','')
                path_file = f'{destino}{nome}.{extensao}'
                urlretrieve(url, path_file)  
                time.sleep(5)
                print('baixou o arquivo em:', path_file)
                new_files.append(path_file)
            return new_files
        else:
            print('arquivo nao encontrado para download')
                
    
    def depara(self, ua):
        '''
            passamos como parâmetro o cod_agencia\n
            a função retorma o cod_agencia_fluid, codigo cadastrado no fluid
        '''      
        # self.ip_planning = str(os.getenv('ip_planning'))
        # self.user_planning = str(os.getenv('user_planning'))
        # self.pw_bd_planning = str(urllib.parse.quote_plus(os.getenv('pw_bd_planning'))) 
        ua =  str(ua).upper()
        db = 'fluid'
        engine = create_engine(f'mysql+mysqlconnector://{self.user_planning}:{self.pw_bd_planning}@{self.ip_planning}/{db}', pool_recycle=3600)
        sql_select_query = f"SELECT cod_fluid FROM fluid.depara_ag_x_cod_fluid WHERE cod_ag = '{ua}'" 
        try: df_depara = pd.read_sql(sql_select_query, con=engine)
        except: df_depara = pd.read_sql(sql_select_query, con=engine)
        if len(df_depara) > 0:
            for i in df_depara.values:
                cod_fluid = str(i[0])
                return str(cod_fluid)
        else:
            cod_fluid = 0
            return str(cod_fluid)
        
        
    def nodo_e_arvore_para_novo_processo(self, id_tipo_processo):
        '''
            retorna ( id_arvore, nodo_inicial ), referente a arvore VIGENTE\n
            caso não exista vigente, retorna ( id_arvore, nodo_inicial ) referente árvore EM CRIAÇÃO
        '''
        ##### Armazenar sessao de login em cookie
        edge_options = EdgeOptions()  
        edge_options.add_argument("start-maximized")  
        edge_options.add_argument("headless")
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("log-level=3")

        url_login = f'{self.url_fluid}/sign-in'
        driver = webdriver.Edge(service=(EdgeService(EdgeChromiumDriverManager().install())), options=edge_options)
        
        driver.get(url_login)
        time.sleep(3)
        driver.find_element(By.XPATH, '''//button/span[contains(text(),"Sicredi")]/..''').click()
        # print('Aguardando url login via ldap...')
        try:
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, '''//input[@id="btnSubmit"]''')))
        except:
            pass
        url = driver.current_url
        # print('url login via ldap obtida com sucesso!')
        driver.get(url)
        
        ##### realizar login no fluid
        driver.find_element(By.ID, '''fieldUser''').send_keys(self.user_fluid)
        driver.find_element(By.ID, '''fieldPassword''').send_keys(self.senha_fluid)
        driver.find_element(By.ID, '''btnSubmit''').click()
        try:
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, '''//*[@id="inbox"]/div/section//span[contains(text(),'Filtrar')]''')))
        except:
            pass
        # print('Login realizado com sucesso!')
        ##### Usar a sessao para acessar outra url da página, pagina de relatorio
        time.sleep(2)
        
        
        # ##### get id da arvore
        try:
            url = f'{self.url_fluid}/cadastro/workflow/versoes/id/{id_tipo_processo}'
            driver.get(url)
            time.sleep(5)
            id_arvore = driver.find_element(By.XPATH, '''//div[contains(text(),'Vigente')]/../../td''').text
            url = f'{self.url_fluid}/cadastro/workflow/index/id/{id_arvore}'
            driver.get(url)
            time.sleep(2)
            nodo_inicial = driver.find_element(By.XPATH, '''//label[contains(@id, 'label-node')]''').get_attribute('id')
            nodo_inicial = nodo_inicial.split('-')[-1]
        except:
            id_arvore = driver.find_element(By.XPATH, '''//div[contains(text(),'Em Criação')]/../../td''').text
            url = f'{self.url_fluid}/cadastro/workflow/index/id/{id_arvore}'
            driver.get(url)
            time.sleep(2)
            nodo_inicial = driver.find_element(By.XPATH, '''//label[contains(@id, 'label-node')]''').get_attribute('id')
            nodo_inicial = nodo_inicial.split('-')[-1]
        return id_arvore, nodo_inicial


    def get_sla(self, id_tipo_processo):
        edge_options = EdgeOptions()  
        edge_options.add_argument("start-maximized")  
        edge_options.add_argument("headless")
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("log-level=3")

        url_login = f'{self.url_fluid}/sign-in'
        driver = webdriver.Edge(service=(EdgeService(EdgeChromiumDriverManager().install())), options=edge_options)
        
        driver.get(url_login)
        time.sleep(3)
        driver.find_element(By.XPATH, '''//button/span[contains(text(),"Sicredi")]/..''').click()
        # print('Aguardando url login via ldap...')
        try:
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, '''//input[@id="btnSubmit"]''')))
        except:
            pass
        url = driver.current_url
        # print('url login via ldap obtida com sucesso!')
        driver.get(url)
        
        ##### realizar login no fluid
        driver.find_element(By.ID, '''fieldUser''').send_keys(self.user_fluid)
        driver.find_element(By.ID, '''fieldPassword''').send_keys(self.senha_fluid)
        driver.find_element(By.ID, '''btnSubmit''').click()
        try:
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, '''//*[@id="inbox"]/div/section//span[contains(text(),'Filtrar')]''')))
        except:
            pass
        # print('Login realizado com sucesso!')
        ##### Usar a sessao para acessar outra url da página, pagina de relatorio
        time.sleep(2)
        
        try:
            url_tempos = f'{self.url_fluid}/cadastro/tipo-processo/tempos/id/{id_tipo_processo}'
            driver.get(url_tempos)
            # print('carregando a pagina...')
            # obter o html da página
            time.sleep(2)
            sla = driver.find_elements(By.XPATH, '''//input[@checked="checked"]''')[0].get_attribute('value')
            print('sla obtido:', sla, 'minutos')
        except:
            sla = '0'
            print('nao foi possivel obter o sla')
        return sla
    
    
    def get_nodo_possiveis_destinos(self, cod_processo: str, nome_do_nodo='selecionado_proximo_nodo', id_usuario = 'default_id'):
        '''
            retorna id_nodo, acao\n
            Exemplos: \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012') \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012', 'Devolver ao parecer anterior') \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012', 'Devolver à confecção') \n
            id_nodo, acao = get_nodo_possiveis_destinos('485012', 'Concluir') \n
        '''
        id_nodo, acao, nodo_nome= 0, 0, 'vazio'
        if id_usuario == 'default_id':
            url = f'{self.url_api}/processos/visualizar/{cod_processo}/{self.id_usuario}'
        else:
            url = f'{self.url_api}/processos/visualizar/{cod_processo}/{id_usuario}'
        headers = {"Content-Type": "application/json; charset=utf-8",  "organization": self.organizacao, "Authorization": self.token_fluid }
        response = requests.get(url, headers=headers)
        cod_res_api = str(response.status_code)
        
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
            
        if cod_res_api == '200': 
            res_json = response.json()
            nome_local = res_json['local']
            local_id = res_json['local_id']
            nodo_atual = res_json['nodo']
            df = pd.DataFrame(res_json['acoes'])
            df.rename(columns={'descricao': 'nome_do_nodo', 'destino': 'codigo_nodo_destino'}, inplace=True)
            print(df)
            for x in df.itertuples():
                nodo_nome = str(x.nome_do_nodo)
                id_nodo = int(x.codigo_nodo_destino)
                acao = int(x.acao)
                if str(nome_do_nodo) == 'selecionado_proximo_nodo' and acao == 0: break
                if nome_do_nodo.upper() in nodo_nome.upper(): break
                else:
                    id_nodo = 0
                    acao = 0
            print()
            print(f'NODO ATUAL ... nodo_atual:   {nodo_atual}, local_atual: {nome_local}, id_local_atual: {local_id}')
            print(f'SELECIONADO... nodo_destino: {id_nodo}, nome_destino: {nodo_nome}, cod_acao: {acao}')
            print()
            return id_nodo, acao
        else:
            msg = str(f'codigo de retorno da api fluid: {cod_res_api}')
            # print(msg)
            # print(response.text)  
            # print('processo identificado como novo') 
            # print()
            return msg, acao 
        
    
    def criar_processo_rascunho(self, id_tipo_processo:str, id_empresa_origem=1, id_empresa_destino=1, id_usuario=0, responsavel_destino=0, arvore=0, tempo_sla_minutos=0):
        '''
            id_processo, nodo_inicial = post_criar_processo(id_tipo_processo)\n
            ou\n
            id_processo, nodo_inicial = post_criar_processo(id_tipo_processo, id_empresa_origem=cod_agencia, id_empresa_destino=cod_agencia)
        '''
        url_final = f'{self.url_api}/processos/novo'
        headers = {"Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        
        if id_empresa_origem != 1: id_empresa_origem = self.depara(id_empresa_origem)
        if id_empresa_destino != 1: id_empresa_destino = self.depara(id_empresa_destino)
        if id_usuario == 0: id_usuario = self.id_usuario
        if responsavel_destino == 0: responsavel_destino = self.id_usuario
        
        time.sleep(1)
        id_versao_arvore = 0
        if arvore == 0:
            id_versao_arvore, nodo_inicial = self.nodo_e_arvore_para_novo_processo(str(id_tipo_processo)) # pega a arvore vigente, ou em criação
        else:
            id_versao_arvore = arvore
        
        if tempo_sla_minutos == 0:
            tempo_minutos = self.get_sla(id_tipo_processo)
        else:
            tempo_minutos = str(tempo_sla_minutos)
        
        obj_acao = {
            "tipo_processo": id_tipo_processo, # id do tipo de processo fluid
            "tempo": tempo_minutos, # tempo em minutos
            "responsavel_criacao": id_usuario, # id do usuário fluid
            "responsavel_origem": id_usuario, # id do usuário fluid
            "responsavel_destino": responsavel_destino,
            "empresa_origem": id_empresa_origem, 
            "empresa_destino": id_empresa_destino,
            "versao_processo": id_versao_arvore # versao da arvore do processo, abra a arvore e veja no final da url o id
            }
        
        # no Método POST passar os parametros {url, headers, json}
        response = requests.post(url_final, headers=headers, json=obj_acao)
        cod_res_api = str(response.status_code) 
        
        if cod_res_api == '200':
            res_dict = response.json()
            id_processo = int(res_dict['id'])
            print(f'Processo fluid {id_processo} criado com sucesso')
            return id_processo
        else:   
            raise Exception(f'Erro ao criar processo novo no fluid: {response.text}')
 

    def get_relatorio_fluid(self, id_relatorio_fluid, data_inicio, data_final, situacao=2):
        '''
            data inicio = dd/mm/yyyy\n
            data_final = dd/mm/yyyy\n
            situacao = 0 (todos os processos)\n
            situacao = 1 (processos em aberto)\n
            situacao = 2 (processos encerrados)\n
            
            df2 = get_relatorio_fluid('357', '19/01/2021', '19/12/2022')\n
            ou\n 
            df2 = get_relatorio_fluid('357', '19/01/2021', '19/12/2022', situacao = 0 )\n  
        '''
        
        edge_options = EdgeOptions()  
        edge_options.add_argument("start-maximized")  
        edge_options.add_argument("headless")
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("log-level=3")

        url_login = f'{self.url_fluid}/sign-in'
        driver = webdriver.Edge(service=(EdgeService(EdgeChromiumDriverManager().install())), options=edge_options)
        
        
        driver.get(url_login)
        time.sleep(3)
        driver.find_element(By.XPATH, '''//button/span[contains(text(),"Sicredi")]/..''').click()
        # print('Aguardando url login via ldap...')
        try:
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, '''//input[@id="btnSubmit"]''')))
        except:
            pass
        url = driver.current_url
        # print('url login via ldap obtida com sucesso!')
        driver.get(url)
        
        df = pd.DataFrame()
        ##### Período do relatório
        id_relatorio = str(id_relatorio_fluid)
        rel_inicio = str(data_inicio)
        rel_final = str(data_final)

         ##### realizar login no fluid
        driver.find_element(By.ID, '''fieldUser''').send_keys(self.user_fluid)
        driver.find_element(By.ID, '''fieldPassword''').send_keys(self.senha_fluid)
        driver.find_element(By.ID, '''btnSubmit''').click()
        time.sleep(3)
        try:
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, '''//*[@id="inbox"]/div/section//span[contains(text(),'Filtrar')]''')))
        except:
            pass
        print('Login realizado com sucesso!')
        ##### Usar a sessao para acessar outra url da página, pagina de relatorio
        time.sleep(2)
        try:
            url_relatorio = f'{self.url_fluid}/relatorio/visualizar/processo/id/{id_relatorio}?dt_ini={rel_inicio}&dt_fim={rel_final}&situacao={situacao}&itens_pagina=1000000&go=true'
            driver.get(url_relatorio)
            print('Carregando relatório...')
            # obter o html da página
            time.sleep(2)
            html_da_pagina = driver.page_source
            tabs = pd.read_html(html_da_pagina)   
            df = tabs[0] 
            print(df.head(5))
        except:
            df = pd.DataFrame()
            print('relatório nao retornou dados para o período')
        return df
        
         
    def get_dados_processo(self, cod_processo, return_response=False, imprimir_json=False, gerar_arquivo_temp=False):
        '''
            retorna valores de campo comuns e campos tabela, existentes no processo fluid\n
            retorna no formato de um dataframe do pandas
        '''
        df1 = pd.DataFrame()
        url = f'{self.url_api}/processos/visualizar/{cod_processo}/{self.id_usuario}'
        headers = { "Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        response = requests.get(url, headers=headers)
        
        if imprimir_json:
            print(response.text)
        if gerar_arquivo_temp:
            file = open(f'c:\\temp\\dados_processo_{cod_processo}.json', 'w')
            file.write(response.text)
            file.close()
        cod_res_api = str(response.status_code)
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
            
        if return_response: return response
        if cod_res_api == '200':
            campos = response.json()
            df1 = pd.DataFrame(campos['atributos'])
            df1["id"] = df1["id"].astype('str')
            
            cont = 0
            for x in df1.itertuples():
                if '[[' in str(x.valor):
                    campo_tabela = campos['atributos'][cont]['valor']
                    L1 = []
                    [L1.append(j) for i in campo_tabela for j in i]
                    df2 = pd.DataFrame(L1)
                    df1 = pd.concat([df1, df2])
                    df1[['nome']] = df1[['nome']].fillna('Campo Tabela')
                    print()
                cont = cont + 1         
        else:
            cod_res_api = str(response.status_code)
            print('codigo de retorno da api fluid: ', cod_res_api) 
            print(response.text)             
        return df1


    def get_processos_fluid(self, array_cod_tipo_processos=[0], id_local_de_processo=542, return_response=False):  
        ''' 
            #### Exemplos:
            - Todos tipo de processos, para usuario e local_id do robô \n
            - df_processos = get_processos_fluid() \n
            - Processos específicos, para usuario e local_id do robô \n
            - df_processos = get_processos_fluid( [941] ) \n
            - df_processos = get_processos_fluid( [852, 941, 792] ) \n
            - df_processos = get_processos_fluid( range(100,800) ) \n
            - Processos , usuario e local_id específicados. \n
            - df_processos = get_processos_fluid( [150, 160],  id_usuario=2535, id_local_de_processo=1 ) \n
        '''
        # entrada do parametro, pode ser int ou str, porque tratei na linha abaixo.
        if array_cod_tipo_processos[0] != 0:
            fluxos_permitidos = [str(x) for x in array_cod_tipo_processos]
        url = f'{self.url_api}/processos/inbox/{self.id_usuario}/01'
        headers = {"Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }

        response = requests.get(url, headers=headers)
        cod_res_api = str(response.status_code) 
        
        if cod_res_api != '200':
            time.sleep(5)
            response = requests.get(url, headers=headers)
            cod_res_api = str(response.status_code)
    
        if return_response: return response
        df1 = pd.DataFrame()
        
        if cod_res_api == '200':
            response_dict = response.json() 
            processos = response_dict['processos']
            df = pd.DataFrame(processos)
            df = df[['numero', 'tipo_id','tipo', 'local_id', 'local']] 
            df = df.astype('str')
            if array_cod_tipo_processos[0] != 0:
                df = df.query(f'tipo_id in {fluxos_permitidos}')
            df = df.query(f'local_id == "{id_local_de_processo}"') # Local de processo 542 - Sede Automacao
            df1 = df[:]
            df1.rename(columns={'numero': 'processo_fuid', 'tipo_id': 'id_fluxo_fluid', 'tipo': 'nome_fluxo_fluid'}, inplace=True)
        else:
            print('codigo de retorno da api fluid: ', cod_res_api) 
            print(response.text)
        return df1
    
    
    def gravar_dados_campos_tabela(self, cod_processo:int, id_tipo_processo:int, id_tabela:int, id_campos_tabela:list, campo_e_valor:list, id_nodo=0, abertura_de_processo=False):
        '''
        CHAMANDO A FUNÇÃO E PASSANDO OS PARÂMETROS \n
        id_tipo_processo = int(945) \n
        cod_processo = '497305' \n
        id_tabela = 3815 - eh o id do campo('Quantidade') qtd linhas da tabela \n
        id_campos_tabela = [5221, 2012] - ids dos campos referente a uma linha da tabela \n

        Passar uma lista de dicionarios, {id_campo: 'valor_a_preencher'} \n
        campo_e_valor = [{5221: 'Galileo Galilei', 2012: '111.222.333-55'}, \n
                        {5221: 'Isaac Newton.', 2012: '333.222.453-77'}, \n
                        {5221: 'Nikola Tesla.', 2012: '555.023.333-99'}] \n

        gravar_dados_campo_tabela(cod_processo, id_tipo_processo, id_tabela, id_campos_tabela, campo_e_valor) \n
        '''

        url = f'{self.url_api}/processos/salvar-campo-tabela'
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        
        lista_de_campos = [] 
        for x in id_campos_tabela:
            dic = {"ttableId": x, "tipoCalc": 0, "value": ""}       
            lista_de_campos.append(dic)
            
        cont = 1
        dict_valores = {}
        for i in campo_e_valor:
            aux = []
            for j in i:
                dict_aux = {}
                print(j, i[j])
                dict_aux["value"] = i[j] 
                dict_aux["ttableId"] = j 
                aux.append(dict_aux)
            cont = cont-1
            indice = str(cont)
            dict_valores[f'{indice}'] = aux
        time.sleep(1)
        
        if id_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)
            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = id_nodo
            
        param = { 
                "processo": cod_processo, 
                "destino": nodo, 
                "usuario": self.id_usuario, 
                "campo": { 
                    "valueTable": dict_valores,
                    "ttableId": id_tabela,
                    "quant": 0,
                    "calcTable": lista_de_campos  
                    }
        } 
                
        res = requests.post(url, headers=headers, json=param)
        if res.status_code != 204:
            raise Exception(f'Erro ao gravar dados no processo {cod_processo}: {res.text}')
        else:
            print(f'Dados gravados com sucesso no processo fluid {cod_processo}')
            return res.status_code
    
    
    def gravar_dados_campos_comuns(self, cod_processo:str, id_tipo_processo:str, dict_campos:dict, abertura_de_processo=False, id_nodo=0):
        '''
            Dicionario {ID:'valor', ID:'valor'} \n
            Conteúdo que vai escrever nos campos \n  
            campos = {5170: '3', \n
                    5171:'2500', \n
                    5177:'123123', \n
                    5175: 'sede', \n
                    5184: '03/02/2023'} \n
            id_tipo_processo = int(945) \n
            cod_processo = '497305' \n
            gravar_dados_multiplos_campos(cod_processo, id_tipo_processo, campos) \n
        '''   
        time.sleep(1)
        if id_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)

            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = id_nodo
        
        url = f'{self.url_api}/processos/salvar-campos'
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        param = { "processo": cod_processo, "destino": nodo, "usuario": self.id_usuario, "campos": dict_campos }

        res = requests.post(url, headers=headers, json=param)
   
        if res.status_code != 204:
            raise Exception(f'Erro ao gravar dados no processo {cod_processo}: {res.text}')
        else:
            print(f'Dados gravados com sucesso no processo fluid {cod_processo}')
            return res.status_code
    
    
    def gravar_unico_campo(self, cod_processo:str, id_tipo_processo:str, campo:int, valor_campo:str, abertura_de_processo=False, id_nodo=0):
        time.sleep(1)
        if id_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo)
            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = id_nodo
        
        url_final = f'{self.url_api}/processos/salvar'
        
        headers = {"Content-Type": "application/json; charset=utf-8", 
                   "organization": self.organizacao, 
                   "Authorization": self.token_fluid }
        
        param = {"processo": cod_processo, 
                 "usuario": self.id_usuario, 
                 "formulario":campo, 
                 "valor":valor_campo, 
                 "destino": nodo}

        response = requests.post(url_final, headers=headers, json = param)
        time.sleep(2)
        cod_res_api = str(response.status_code)
        if cod_res_api != '204':
            response = requests.post(url_final, headers=headers, json = param)
            time.sleep(2)
            if cod_res_api != '204':
                raise Exception(f'Erro ao gravar unico campo no fluid, {response.text}')
        return response.status_code
    
    
    def protocolar_processo_fluid(self, cod_processo: str, id_tipo_processo: str,  mensagem: str, id_empresa_origem='1', id_empresa_destino='1', nome_do_nodo ='selecionado_proximo_nodo', abertura_de_processo= False, cod_nodo=0, cod_acao = 0, id_usuario=0, usuario_destino=0):
        ''' 
            post_protocolar_processo_fluid(processo, id_tipo_processo, msg, nome_nodo_destino, empresa_orig, empresa_dest) \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada') \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', empresa_orig=68, empresa_dest=68) \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', 'Devolver') \n
            post_protocolar_processo_fluid('497305', '945', 'automação realizada', 'Concluir') \n
            
        '''
        
        if id_usuario == 0: id_usuario = self.id_usuario
        if usuario_destino == 0: usuario_destino = self.id_usuario
        
        url = f'{self.url_api}/processos/protocolar'
        headers = { "Content-Type": "application/json; charset=utf-8", "organization": self.organizacao, "Authorization": self.token_fluid }
        if id_empresa_origem  != 1: id_empresa_origem = self.depara(id_empresa_origem)
        if id_empresa_destino != 1: id_empresa_destino = self.depara(id_empresa_destino)
        
        if cod_nodo == 0:
            nodo, acao = self.get_nodo_possiveis_destinos(cod_processo, nome_do_nodo)
            if 'codigo de retorno' in str(nodo) or abertura_de_processo:
                id_arvore, nodo = self.nodo_e_arvore_para_novo_processo(id_tipo_processo)
                acao = 0
        else:
            nodo = cod_nodo
            acao = cod_acao
        
        obj_acao = {
            "acao": acao, # ação 0, protocolar normal com mensagem
            "processo": cod_processo,
            "destino": nodo, # nodo destino da arvore do processo, para onde vai qdo protocolar
            "parecer": mensagem, # mensagem para escrever no parecer ao protocolar
            "parecer_restrito": 0,
            "usuario": id_usuario, # id usuario fluid que esta realizando a operacao por api
            "empresa_origem": id_empresa_origem, # empresa 1
            "empresa_destino": id_empresa_destino, # usar zero para sede, e para agencia passar cod_fluid referente a agencia , fazer depara. 
            "usuario_destino": usuario_destino
            }

        response = requests.post(url, headers=headers, json=obj_acao)    
        cod_res_api = str(response.status_code)
 
    
        if cod_res_api != '204':
            time.sleep(5)
            response = requests.post(url, headers=headers, json=obj_acao)
            cod_res_api = str(response.status_code)
            
        if (cod_res_api == '204'):
            print(f'processo fluid {cod_processo} protocolado com sucesso')
            return cod_res_api
        else:
            raise Exception(f'Erro ao protocolar processo {cod_processo}: {response.text}')


    def tomar_posse(self, cod_processo:str, empresa=1, id_usuario=0):
        time.sleep(1)        
        url = f'{self.url_api}/processos/tomar-posse'
        if id_usuario == 0: id_usuario = self.id_usuario
        
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        param = {"usuario": id_usuario, "empresa": empresa, "processo": cod_processo}
        res = requests.post(url, headers=headers, json=param)

        if res.status_code != 204: raise Exception(f'Erro ao gravar dados no processo {cod_processo}, {res.text}')
        print(f'Ok, tomou posse do processo: {cod_processo}')
        return res.status_code


    def get_usuarios_fluid(self):
        time.sleep(1)        
        url = f'{self.url_api}/usuarios'
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        res = requests.get(url, headers=headers)
        campos = res.json()
        df_usuarios = pd.DataFrame(campos['usuarios'])
        if res.status_code != 200: raise Exception(f'Erro ao obter lista de usuarios fluid, {res.text}')
        print(f'Ok, retornou lista de usuarios fluid')
        return df_usuarios 
    

    def get_empresas_fluid(self):
        time.sleep(1)        
        url = f'{self.url_api}/empresas'
        headers = {"organization": self.organizacao, "Authorization": self.token_fluid }
        res = requests.get(url, headers=headers)
        campos = res.json()
        df_empresas = pd.DataFrame(campos['empresas'])
        if res.status_code != 200: raise Exception(f'Erro ao obter lista de empresas no fluid, {res.text}')
        print(f'Ok, retornou lista de empresas cadastradas no fluid')
        return df_empresas 
    

class Whatsapp:
     
    def __init__(self):
        self.dados = Dados()
        self.url_api_whats = str(gerador_pwd('url_api_whats', 'sistema'))
        self.token_api_whats = str(gerador_pwd('url_api_whats', 'senha'))
        self.template_informa_novo = str(gerador_pwd('template_informa_novo', 'sistema'))
        self.template_informa_com_img = str(gerador_pwd('template_informa_com_img', 'senha'))
        self.template_informa_com_pdf = str(gerador_pwd('template_informa_com_pdf', 'senha'))
        self.whats_user_origem = str(gerador_pwd('whats_user_origem', 'senha'))
        self.cod_coop = str(gerador_pwd('cod_coop', 'senha'))
        
        
    def verificar_opt_in(self, celular:str):   
        url = f'{self.url_api_whats}/optin/55{celular}'
        headers = {"Content-Type": "application/json; API Key","x-api-key": self.token_api_whats}
        response = requests.get(url, headers=headers)
        return response.status_code
    
           
    def enviar_texto_whatsapp(self, celular: str, sistema_envio: str, texto:str, template='sicredi_informa_novo', return_list=False):    
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + str(celular),
            "templateName": template,
            "templateParameters": {"INFORMA": texto},
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio,
            "originUsername": self.whats_user_origem
        }
        response= requests.post(url, headers=headers, json=body)
        if str(response.status_code) == '200':
            try:
                content = json.loads((response.content).decode('utf-8'))
            except:
                content = json.loads(response.content) 
            id_msg = content.get('senderResultId')
        else:
            id_msg = 0
        if return_list:
            return [response.status_code, response, id_msg]
        return response.status_code


    def enviar_texto_e_img_whatsapp(self, celular: str, texto: str,url_imagem:str, sistema_envio: str, template='sicredi_informa_imagem_com_texto', return_list=False):    
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + str(celular),
            "templateName": template,
            "templateParameters": {"INFORMA": texto, "headerImageUrl": url_imagem},
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio,
            "originUsername": self.whats_user_origem
        }
        response = requests.post(url, headers=headers, json=body)
        if str(response.status_code) == '200':
            try:
                content = json.loads((response.content).decode('utf-8'))
            except:
                content = json.loads(response.content)
            id_msg = content.get('senderResultId')
        else:
            id_msg = 0
        if return_list:
            return [response.status_code, response, id_msg]
        return response.status_code


    def enviar_texto_e_pdf_whatsapp(self, celular: str, texto: str,url_pdf:str,nome_do_arquivo:str, sistema_envio: str, template='template_informa_com_pdf', return_list=False):    
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + str(celular),
            "templateName": template,
            "templateParameters": {
                "INFORMA": texto,
                "headerDocumentUrl": url_pdf,
                "headerDocumentCaption": nome_do_arquivo
            },
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio
        }
        response = requests.post(url, headers=headers, json=body)
        if str(response.status_code) == '200':
            try:
                content = json.loads((response.content).decode('utf-8'))
            except:
                content = json.loads(response.content)
            id_msg = content.get('senderResultId')
        else:
            id_msg = 0
        if return_list:
            return [response.status_code, response, id_msg]
        return response.status_code  
           
            
        
    def validar_ajustar_celular(self, celular:str):
        # remover caracteres diferentes de numeros
        celular = celular.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('.', '')
        # valida se é celular e add nove caso necessario
        if len(celular) == 10 and celular[2] in ['7','8','9']:
            celular = celular[:2] + '9' + celular[2:]
               
        if len(celular) > 10 and celular[3] in ['7','8','9']:
            print('celular válido')
            celular = celular
        else:
            # retorna '0' caso nao seja celular e caso nao tenha ddd
            print('celular inválido, ou falta o ddd')
            celular = None
        return celular
    
    
    def add_hist_sem_optin_whatsapp(self, conexao_db_planning, num_celular:str):
        try:
            query = f'''INSERT INTO rpa_hist_sem_optin_whatsapp(num_celular) VALUES("{num_celular}")'''
            self.dados.insert_banco_dados(conexao_db_planning, query)
        except:
            print(f'numero {num_celular} ja se encontra na tabela rpa_hist_sem_optin_whatsapp')
        
        
    def add_hist_central_msg(self, conexao_db_planning, id_envio:str, tel:str, mensagem:str, area_solicitante:str, canal_envio:str = 'whatsapp', template:str = 'NULL', campanha_produto:str = 'NULL', processo_fluid:str = 'NULL', cod_rpa:str = 'NULL', obs:str = 'NULL'):
        try:            
            query = f'''INSERT INTO tbl_central_mensagens(id_envio, tel, mensagem, canal_envio, template, area_solicitante, campanha_produto, processo_fluid, cod_rpa, obs) 
                    VALUES("{id_envio}", "{tel}", "{mensagem}", "{canal_envio}",  "{template}", "{area_solicitante}", "{campanha_produto}", "{processo_fluid}", "{cod_rpa}", "{obs}")'''
            
            self.dados.insert_banco_dados(conexao_db_planning, query)
        except:
            raise Exception(f'Erro ao inserir numero {tel} na tabela tbl_central_mensagens')
        
     
    def possui_opt_in(self, celular:str, return_response:bool = False):   
        url = f'{self.url_api_whats}/optin/55{celular}'
        headers = {"Content-Type": "application/json; API Key","x-api-key": self.token_api_whats}
        response = requests.get(url, headers=headers)
        possui_optin = False
        if response.status_code == 200: possui_optin = True
        if return_response:
            return response
        else:
            return possui_optin


    def enviar_msg_whatsapp(self, celular: str, sistema_envio: str, parametros:dict = {"INFORMA": 'msg_aqui'}, template_name='sicredi_informa_novo', return_response:bool = False): 
        '''
         -parametros texto = {"INFORMA": 'msg_aqui'}\n\n
         -parametros img + texto = {"INFORMA": texto, "headerImageUrl": url_imagem}\n\n
         -parametros pdf + texto = {"INFORMA": texto, "headerDocumentUrl": url_pdf, "headerDocumentCaption": nome_do_arquivo }\n\n
         -parametros inadimp. seguro = {"nome_associado": nome_associado, "numero_apolice": apolice, "nome_produto": nome_produto }\n
         # sicredi_informa_novo
         # sicredi_informa_imagem_com_texto
         # sicredi_informa_pdf_com_texto
         # sicredi_informa_video_com_texto1
         # cancelamento_seguros_0718
        '''   
        url = f'{self.url_api_whats}/notification'
        headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
        body = {
            "customerCoopCode": self.cod_coop,
            "customerBranchNum": "01",
            "customerPhoneNum": "55" + celular,
            "templateName": template_name,
            "templateParameters": parametros,
            "originCompany": "coop_" + self.cod_coop,
            "originSystem": sistema_envio,
            "originUsername": self.whats_user_origem
        }
        response= requests.post(url, headers=headers, json=body)
        print(response.status_code, f': enviou whatsapp para o numero {celular}')
        if str(response.status_code) == '200':
            try:
                content = json.loads((response.content).decode('utf-8'))
            except:
                content = json.loads(response.content) 
            id_msg = str(content.get('senderResultId'))
        else:
            id_msg = str('0')
        if return_response:
            return response
        else:
            return id_msg


    def conferir_se_ja_enviou_msg_hoje(self, conexao_db_planning, celular:str, cod_rpa:str, processo_fluid:str = '0', data_registro:str ='opcional ano-mes-dia'):
        hoje = datetime.now().strftime('%Y-%m-%d')
        data_registro = hoje if data_registro == 'opcional ano-mes-dia' else data_registro
        
        if processo_fluid != '0':
            consulta = f'''SELECT tel, canal_envio, cod_rpa, data_registro 
                            FROM tbl_central_mensagens WHERE tel="{celular}" 
                            AND processo_fluid="{processo_fluid}" AND data_registro like "{data_registro}%"'''
        else: 
            consulta = f'''SELECT tel, canal_envio, cod_rpa, data_registro 
                            FROM tbl_central_mensagens WHERE tel="{celular}" 
                            AND cod_rpa="{cod_rpa}" AND data_registro like "{data_registro}%"'''  
                       
        df = self.dados.consultar_banco_dados(conexao_db_planning, consulta)
        total_linhas = len(df)
        msg_enviada = False
        if total_linhas > 0:
            print(f'ja enviou msg para o numero {celular} hoje, canal {df.canal_envio[0]}')
            msg_enviada = True
        return msg_enviada
        
        
    def atualizar_status_entregas_whatsapp(self, conexao_db_planning, data_registro='opcional ano-mes-dia'):
        try:
            if data_registro == 'opcional ano-mes-dia':
                consulta = f'''SELECT * FROM tbl_central_mensagens WHERE canal_envio="whatsapp" AND status_msg IS NULL'''
            else:
                consulta = f'''SELECT * FROM tbl_central_mensagens WHERE canal_envio="whatsapp" AND status_msg IS NULL AND data_registro like "{data_registro}%"'''
                
            df = self.dados.consultar_banco_dados(conexao_db_planning, consulta)
            
            print('buscando status de entrega das mensagens whatsapp...')
            for line in df.itertuples():
                try:
                    id_msg = str(line.id_de_envio)
                    url = f'{self.url_api_whats}/notification/{id_msg}'
                    headers = {"Content-Type": "application/json; API Key", "x-api-key": self.token_api_whats}
                    # Get status da mensagem pela API através do ID da mensagem
                    resposta = requests.get(url, headers = headers)
                    # print(resposta.text)
                    # Extraindo o motivo da não entrega, caso a mensagem possua status de erro ou não.
                    if json.loads(resposta.text).get('error'):
                        status = json.loads(resposta.text).get('errors')[0]
                        status_entrega = status.get('message')
                    else:
                        status_entrega =  'Mensagem enviada'
                    query_update = f'''UPDATE tbl_central_mensagens SET status_msg="{status_entrega}" WHERE id_de_envio="{id_msg}"'''
                    self.dados.update_banco_dados(conexao_db_planning, query_update)
                except Exception as e:
                    print(f'Erro ao consultar status de entrega a mensagem id {id_msg}. Erro: {str(e)}.')
        except Exception as e:
            raise Exception(f'Erro ao consultar status de entrega de uma ou mais mensagens whats. Erro: {str(e)}.')


class Sms:
        
    def __init__(self):
        self.dados = Dados()
        self.url_api_sms = str(gerador_pwd('url_api_sms', 'sistema'))
        self.token_api_sms = str(gerador_pwd('url_api_sms', 'senha'))
        self.cod_coop = str(gerador_pwd('cod_coop', 'senha'))
        self.sms_from = str(gerador_pwd('sms_from', 'senha'))


    def send_SMS(self, celular: str, texto:str):    
        # nao utilize acentuacao na mensagem do sms, pois exige o valor de 2 mensagens.
        headers = {"Content-Type": "application/json; charset=utf-8", "X-API-TOKEN": self.token_api_sms}
        body = {
            "from": self.sms_from,
            "to": "55" + celular,
            "contents": [
                {"type": "text", "text": texto}   
                ]
            }
        response = requests.post(self.url_api_sms, headers=headers, json=body)
        print(response.status_code, f': enviou sms para o numero {celular}')
        if str(response.status_code) == '200':
            try:
                content = json.loads((response.content).decode('utf-8'))
            except:
                content = json.loads(response.content)
            id_msg = str(content.get('id'))
        else:
            id_msg = str('0')
        return id_msg
        
    
    def add_hist_central_msg(self, conexao_db_planning, id_envio:str, tel:str, mensagem:str, area_solicitante:str, canal_envio:str = 'sms', campanha_produto:str = 'NULL', processo_fluid:str = 'NULL', cod_rpa:str = 'NULL', obs:str = 'NULL'):
        try:            
            query = f'''INSERT INTO tbl_central_mensagens(id_envio, tel, mensagem, canal_envio, area_solicitante, campanha_produto, processo_fluid, cod_rpa, obs) 
                    VALUES("{id_envio}", "{tel}", "{mensagem}", "{canal_envio}", "{area_solicitante}", "{campanha_produto}", "{processo_fluid}", "{cod_rpa}", "{obs}")'''
            
            self.dados.insert_banco_dados(conexao_db_planning, query)
        except:
            raise Exception(f'Erro ao inserir numero {tel} na tabela tbl_central_mensagens')  
        
    
    def validar_ajustar_celular(self, celular:str):
        # remover caracteres diferentes de numeros
        celular = celular.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('.', '')
        # valida se é celular e add nove caso necessario
        if len(celular) > 9 and len(celular) == 10 and celular[2] in ['7','8','9']:
            celular = celular[:2] + '9' + celular[2:]
        else:
            # retorna '0' caso nao seja celular e caso nao tenha ddd
            print('celular invalido, ou falta o ddd')
            celular = None
        return celular
    
    
class Emails:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    
    def __init__(self):
        self.user_mail = gerador_pwd('api_email', 'usuario')
        self.password_mail = gerador_pwd('api_email', 'sistema')
        self.smtpsrv = gerador_pwd('api_email', 'ip_host')


    def enviar_email(self, destinatarios, assunto: str, mensagem='', anexo=None, html_text_img=None, cc=None, cco=None):
        '''
        mail.enviar_email('usuario@dominio.com.br', 'titulo aqui', 'msg aqui') \n\n
        
        lista_dest = ['usuario@dominio.com.br','appuser@dominio.com.br']\n
        mail.enviar_email(lista_dest, 'titulo aqui', 'msg aqui')\n\n
        
        anexos = ['notas.txt', 'README.md']\n
        mail.enviar_email('usuario@dominio.com.br', 'titulo aqui', 'msg aqui', anexos)\n\n
        
        anexos = ['notas.txt', 'README.md', 'imagem.PNG']\n
        html_text_img = '<html><body><h1>msg aqui</h1><img src="cid:imagem_aqui.PNG"></body></html>'\n
        mail.enviar_email('usuario@dominio.com.br', 'titulo aqui', anexos, html_text_img)\n
        '''
        import pathlib
        mail_content = mensagem
        smtpserver = self.smtplib.SMTP(self.smtpsrv,587)
        msg = self.MIMEMultipart('mixed')
        msg = self.MIMEMultipart('alternative')
        if cco: 
            msg['Bcc'] = cco if type(cco) == str else ", ".join(cco)
        if cc: 
            msg['Cc'] = cc if type(cc) == str else ", ".join(cc)
            
        msg['Subject'] = assunto
        msg['From'] = self.user_mail 
        msg['To'] = destinatarios if type(destinatarios) == str else ", ".join(destinatarios)

        
        if html_text_img:
            msg.attach(self.MIMEText(mail_content + html_text_img, 'html', 'utf-8'))
        else:
            msg.attach(self.MIMEText(mail_content,'plain','utf8'))      
        
        if anexo:
            if type(anexo) == str:
                if anexo:
                    attachmentPath = anexo
                    name_file = pathlib.Path(attachmentPath).name
                    try:
                        with open(attachmentPath, "rb") as attachment:
                            p = self.MIMEApplication(attachment.read(),_subtype="png")	
                            p.add_header('Content-Disposition', "attachment; filename= %s" % name_file) 
                            msg.attach(p)
                    except Exception as e:
                        print(str(e))
            elif type(anexo) == list:
                for attachmentPath in anexo:
                    name_file = pathlib.Path(attachmentPath).name
                    try:
                        with open(attachmentPath, "rb") as attachment:
                            p = self.MIMEApplication(attachment.read(),_subtype="png")	
                            p.add_header('Content-Disposition', "attachment; filename= %s" % name_file) 
                            msg.attach(p)
                    except Exception as e:
                        print(str(e))
            
        #Send the Email Message
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(self.user_mail , self.password_mail)

        todos_destinos = []
        if destinatarios and cc and cco:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            if isinstance(cc, list): todos_destinos.extend(cc)
            if isinstance(cc, str): todos_destinos.append(cc)
            if isinstance(cco, list): todos_destinos.extend(cco)
            if isinstance(cco, str): todos_destinos.append(cco) 
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)
        elif destinatarios and cc:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            if isinstance(cc, list): todos_destinos.extend(cc)
            if isinstance(cc, str): todos_destinos.append(cc)
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)
        elif destinatarios and cco:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            if isinstance(cco, list): todos_destinos.extend(cco)
            if isinstance(cco, str): todos_destinos.append(cco) 
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)
        else:
            if isinstance(destinatarios, list): todos_destinos.extend(destinatarios)
            if isinstance(destinatarios, str): todos_destinos.append(destinatarios)
            smtpserver.send_message (msg, from_addr=self.user_mail, to_addrs=todos_destinos)        
        smtpserver.close()
        
                                        
class Acc:
    import pyautogui as p
    import subprocess
    import pyperclip
    
    
    def __init__(self):
        self.usuario_acc = str(gerador_pwd('acc', 'usuario'))
        self.senha_acc = str(gerador_pwd('acc', 'senha'))
        self.janela_sacg = 'janela'
        self.janela_siat = 'janela'
        self.janela_siac = 'janela'

               
    def open_acclient(self, siat_siac_sacg: str | list, transacional=True):
        ''' acc.open_acclient('siac') \n
        acc.open_acclient(['siat', 'sacg'])'''

        opcoes = []
        if isinstance(siat_siac_sacg, str): opcoes.append(siat_siac_sacg)
        else: opcoes = siat_siac_sacg
            
        try: os.system('taskkill /F /FI "WindowTitle eq C:\\ProgramData\\ac\\teoff-exe*" /T')
        except Exception: pass
        
        try: os.system('taskkill /F /FI "WindowTitle eq SIA*" /T')
        except Exception: pass
        
        try: os.system('taskkill /F /FI "WindowTitle eq SACG*" /T')
        except Exception: pass
        
        try: os.system('taskkill /F /IM javaw_ac.exe')
        except Exception: pass
        
        user_acc = self.usuario_acc
        pw_acclient = self.senha_acc
         
        self.subprocess.Popen("C:\\Users\\Public\\Desktop\\AC Client.lnk",shell=True)
        
        # esperar janela de login
        win_login = ahk.win_wait(title=r'Aplicações Core - Login', timeout=20, title_match_mode=2)
        win_login.activate()
        win_login.to_top() 
        self.p.hotkey('shift','tab')
        ahk.type(user_acc)
        self.p.press('tab')
        ahk.type(pw_acclient)
        self.p.press('tab')
        self.p.press('enter')
        print('passou do login')

        # esperar janela de menu, após o login
        self.win_menu = ahk.win_wait(title=r'AC Client', timeout=20, title_match_mode=2)
        self.win_menu.set_title('MENU_ACC')
        self.win_menu.activate()
        self.win_menu.to_top() 
        self.p.sleep(1)
        self.p.press('pgdn')
        self.janela_menu_acc = self.win_menu.get_position()
        
        self.win_sacg = None
        self.win_siat = None
        self.win_siac = None

        # Selecionar o MENU SIAT
        posicao = 0
        pasta_imagens = user_site_packages +  '\\rpa_coop\\img\\'
        
        # clica no botao transacional ou relatório
        if transacional:
            self.p.moveTo(self.janela_menu_acc.x + 48, self.janela_menu_acc.y + 165)
            time.sleep(1)
            self.p.click()
        else:
            self.p.moveTo(self.janela_menu_acc.x + 48, self.janela_menu_acc.y + 245)
            self.p.click()
        time.sleep(3)
            
        self.janelas = []
        opcoes = [x.upper() for x in opcoes]
        controle = 1
        self.win_principal = None
        
        for menu in opcoes:
            time.sleep(2)   
            self.p.press('pgdn')
            time.sleep(1)
            
            if menu == 'SACG':
                try:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_branco.png', confidence=0.9, minSearchTime=2.0)
                except:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'sacg_verde.png', confidence=0.9, minSearchTime=2.0)
                print('posicao do click sacg', posicao)
                self.p.doubleClick(posicao)
                self.win_sacg = ahk.win_wait(title=r'teoff', timeout=20, title_match_mode=2)
                self.win_sacg.set_title('SACG')
                self.win_sacg.activate()
                self.win_sacg.to_top() 
                if controle == 1: self.win_principal = self.win_sacg
                print('clicou no menu: sacg')
                self.win_menu.activate()
                self.win_menu.to_top()
            elif menu == 'SIAT':
                try:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siat_amarelo.png', confidence=0.9, minSearchTime=2.0)
                except:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siat_branco.png', confidence=0.9, minSearchTime=2.0)
                print('posicao do click siat', posicao)
                self.p.doubleClick(posicao)
                self.win_siat = ahk.win_wait(title=r'teoff', timeout=20, title_match_mode=2)
                self.win_siat.set_title('SIAT')
                self.win_siat.activate()
                self.win_siat.to_top() 
                if controle == 1: self.win_principal = self.win_siat
                print('clicou no menu: siat')
                self.win_menu.activate()
                self.win_menu.to_top()
            elif menu == 'SIAC':
                try:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siac_branco.png', confidence=0.9, minSearchTime=2.0)
                except:
                    posicao = self.p.locateOnScreen(pasta_imagens + 'siac_amarelo.png', confidence=0.9, minSearchTime=2.0)
                print('posicao do click siac', posicao)
                self.p.doubleClick(posicao)
                self.win_siac = ahk.win_wait(title=r'teoff', timeout=20, title_match_mode=2)
                self.win_siac.set_title('SIAC')
                self.win_siac.activate()
                self.win_siac.to_top() 
                if controle == 1: self.win_principal = self.win_siac
                print('clicou no menu: siac')
                self.win_menu.activate()
                self.win_menu.to_top()
            time.sleep(1)
            controle = controle + 1
        self.win_principal.activate()
        self.win_principal.to_top() 
        time.sleep(1)
        return self.win_menu, self.win_siat, self.win_siac, self.win_sacg

               
    def select_menu_letras(self, letras, nome_janela=None):
        '''acc.select_menu_letras(letras) \n
         acc.select_menu_letras(letras, nome_janela='sacg')'''
        self.p.sleep(1)
        nome_janela = str(nome_janela).upper()
        if nome_janela == 'SIAT':
            janela = self.win_siat
        elif nome_janela == 'SIAC':
            janela = self.win_siac
        elif nome_janela == 'SACG':
            janela = self.win_sacg
        else:
            janela = ahk.get_active_window()
        renomear_janela = janela.get_title()
        janela.activate()
        
        # Selecionar o Menu de opções
        self.p.sleep(1)
        if len(letras) == 2:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
        elif len(letras) == 3:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)   
        elif len(letras) == 4:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
        elif len(letras) == 5:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
            self.p.typewrite(letras[4])
            self.p.sleep(1)
        elif len(letras) == 6:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
            self.p.typewrite(letras[4])
            self.p.sleep(1)
            self.p.typewrite(letras[5])
            self.p.sleep(1)
        elif len(letras) == 7:
            self.p.typewrite(letras[0])
            self.p.sleep(1)
            self.p.typewrite(letras[1])
            self.p.sleep(1)
            self.p.typewrite(letras[2])
            self.p.sleep(1)
            self.p.typewrite(letras[3])
            self.p.sleep(1)
            self.p.typewrite(letras[4])
            self.p.sleep(1)
            self.p.typewrite(letras[5])
            self.p.sleep(1)
            self.p.typewrite(letras[6])
            self.p.sleep(1)
        else:
            print('ops funcao entende apenas 2, 3, 4, 5, 6 ou 7 letras')
        janela.set_title(renomear_janela)
        
                            
    def get_text(self, ini_linha: int=22, fim_linha: int=632, topo1: int=410, topo2: int=415, tempo_arrastar_soltar: float=1.5, nome_janela: str | None=None):
        ''' acc.get_text('Retorna ao Sistema')\n
         acc.get_text('Retorna ao Sistema', nome_janela = 'sacg')'''
        time.sleep(1)
        nome_janela = str(nome_janela).upper()
        if nome_janela == 'SIAT':
            janela = self.win_siat
        elif nome_janela == 'SIAC':
            janela = self.win_siac
        elif nome_janela == 'SACG':
            janela = self.win_sacg
        else:
            janela = ahk.get_active_window()
        posicao_janela = janela.get_position()
        renomear_janela = janela.get_title()
        janela.activate()
  
        time.sleep(1)
        self.p.moveTo(posicao_janela.x + ini_linha, posicao_janela.y + topo1)
        self.p.sleep(1)
        self.p.dragTo(posicao_janela.x + fim_linha, posicao_janela.y + topo2, tempo_arrastar_soltar, button='left')
        self.p.moveTo(posicao_janela.x + ini_linha, posicao_janela.y + topo2)
        self.p.rightClick()
        capturado = self.pyperclip.paste()
        print(f'texto capturado:{capturado}')
        janela.set_title(renomear_janela)
        return capturado            
            
              
    def exist_text(self, texto_esperado: str, max_tentativas: int=7, segundos_entre_tentativas: int=3, ini_linha: int=22, fim_linha: int=632, topo1: int=412, topo2: int=412, tempo_arrastar_soltar: float=1.5, continua_seerro: bool=False, nome_janela: str |None=None):
        ''' acc.exist_text('Retorna ao Sistema')\n
         acc.exist_text('Retorna ao Sistema', nome_janela = 'sacg')'''
        time.sleep(1)
        self.pyperclip.copy('')
        tentativas = 0
        time.sleep(1)
        captura = self.get_text(ini_linha, fim_linha, topo1, topo2, tempo_arrastar_soltar, nome_janela = nome_janela)
        resultado = True
        while not texto_esperado in captura and tentativas < max_tentativas:
            print('esperando texto: ', texto_esperado)
            self.p.sleep(segundos_entre_tentativas)
            captura = self.get_text(ini_linha, fim_linha, topo1, topo2, tempo_arrastar_soltar, nome_janela = nome_janela)
            tentativas += 1
            if tentativas == max_tentativas:
                resultado = False
        print(resultado)
        if resultado == False and continua_seerro == False:
            raise Exception(f'Execução pausada. O texto: "{texto_esperado}" não foi localizado durante a execução do robô.')
        return resultado
 
         
class Monitorar:
        
    import socket
         
    def __init__(self):
        self.dados = Dados()
        self.data_ini = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + ' 17:30:00'
        self.data_fim = datetime.now().strftime('%Y-%m-%d') + ' 17:30:00'
        self.usuario = str(gerador_pwd('user_monitora_vm', 'senha'))
        self.pwd = str(gerador_pwd('pw_monitora_vm', 'senha'))
        self.linux_host = str(gerador_pwd('vm_linux_host', 'senha'))
        self.linux_ip = str(gerador_pwd('vm_linux_host', 'ip_host'))
        self.linux_user = str(gerador_pwd('vm_linux_user', 'senha'))
        self.linux_pwd = str(gerador_pwd('vm_linux_pw', 'senha'))
        self.conexao = self.dados.criar_engine('cronos')
        
     
            
    def check_vms_running(self, ignorar_vms:list = ['NOTE0012035', 'DESKTOP-J63']):
        hoje_a_noite = datetime.now().strftime('%Y-%m-%d') + ' 18'
        hora_cheia = int(datetime.now().strftime('07'))
        df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM vms_rpa WHERE ativar_monitoramento = 'S' and ativo = 'S' ")
        df = df['vm_host']
        vms = df.to_list()
        dic_vms = {}

        for vm in vms: 
            if vm in ignorar_vms: continue
            
            ### Consulta na fila se teve agendamento de rpa para hoje no intervalo das 18 Horas
            if self.linux_host in vm and 8 >= hora_cheia <= 17:
                try:
                    df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM rpa_fila WHERE data_agendamento like '%{hoje_a_noite}%' ")
                    qtd_agendados_para_hj_noite = len(df)
                    if qtd_agendados_para_hj_noite > 0:
                        print('ok - agendador_python_new.py executou hoje de manhã')
                        status_vm = 'ok'
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_python = 'S' WHERE vm_host = '{vm}'")
                    else:
                        print('Erro, agendador_python_new.py nao foi executado hoje')
                        status_vm = 'erro'
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
                        self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET agendador_python = 'N' WHERE vm_host = '{vm}'")   
                except:
                    pass    
                            
            
            ### Consulta as VMs que possuem os executores de RPAs, consomem a fila do cronos
            try:
                host = self.socket.gethostbyname(vm)
                processos = os.popen(f'wmic /node:{host} /user:{self.usuario} /password:{self.pwd} process get description').read()
            except:
                status_vm = 'erro'
                print('{:<20} {:<8}'.format(vm, status_vm))
                continue
            if 'python.exe' in processos: 
                status_vm = 'ok'
                print('{:<20} {:<8}'.format(vm, status_vm))
            else:
                status_vm = 'erro'
                print('{:<20} {:<8}'.format(vm, status_vm))
            dic_vms[vm] = status_vm
            self.dados.update_banco_dados(self.conexao, f"UPDATE vms_rpa SET vm_status = '{status_vm}' WHERE vm_host = '{vm}'")
        print()
        return dic_vms
                
              
                
    def check_status_rpas_na_fila(self, tipo_status='erro', ver_todos_status=False):
        if ver_todos_status:
            df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM rpa_fila")
        else:
            df = self.dados.consultar_banco_dados(self.conexao, f"SELECT * FROM rpa_fila WHERE status_rpa='{tipo_status}'")
        df = df[['cod_rpa', 'executar_na_vm', 'status_rpa']]
        print(df)
        print()
        return df
    
                             
class Escrever_por_extenso:  
            
    def __init__(self):
        self.unidades = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']
        self.especiais = ['dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
        self.dezenas = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
        self.centenas = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
   
    
    def calc_3digitos(self, num: str):
        C = ''   
        num = int(num)             
        num = str(num)
        if int(len(num)) == 3:
            if int(num[-3]) == 1 and int(num[-2:]) == 0: C = 'cem'
            elif int(num[-3]) >= 1 and int(num[-2:]) == 0: C = self.centenas[int(num[-3])] 
            elif int(num[-3]) >= 1 and int(num[-2]) == 0 and int(num[-1]) > 0: C = self.centenas[int(num[-3])] + ' e ' + self.unidades[int(num[-1])]
            elif int(num[-3]) >= 1 and int(num[-2]) == 1 and int(num[-1]) >= 0: C = self.centenas[int(num[-3])] + ' e ' +  self.especiais[int(num[-1])]
            elif int(num[-3]) >= 1 and int(num[-2]) > 0 and int(num[-1]) == 0: C = self.centenas[int(num[-3])] + ' e ' +  self.dezenas[int(num[-2])]
            elif int(num[-3]) >= 1 and int(num[-2]) > 0 and int(num[-1]) > 0: C = self.centenas[int(num[-3])] + ' e ' +  self.dezenas[int(num[-2])] + ' e ' + self.unidades[int(num[-1])]  
        elif int(len(num)) == 2:
            if int(num[-2]) == 1: C = self.especiais[int(num[-1])]
            elif int(num[-2]) > 1 and int(num[-1]) == 0: C = self.dezenas[int(num[-2])]
            elif int(num[-2]) > 1 and int(num[-1]) > 0: C = self.dezenas[int(num[-2])] + ' e ' + self.unidades[int(num[-1])]   
        else:
            C = 'um' if int(num) == 1 else self.unidades[int(num)]
        return C 


    def taxa_por_extenso(self, taxa: float | str, nome_separador: str = 'virgula') -> str:
        '''taxa_texto = taxa_por_extenso(128.09)\n
            cento e vinte e oito virgula zero nove por cento
        ''' 
        
        if isinstance(taxa, float):
            taxa = str(taxa).replace('.', ',')
            if taxa[-2] == ',': taxa = taxa + '0'
        else:
            taxa = str(taxa).replace('.', ',').replace(' ', '')
            if ',' not in taxa: 
                taxa = taxa + ',00'
            elif taxa[-2] == ',': 
                taxa = taxa + '0'
            
        if ',' in taxa:
            valor_aux = taxa.split(',')
            valor_dir = valor_aux[0]
            valor_esq = valor_aux[1]
        else:
            valor_dir = taxa
            valor_esq = '0'   
    
        if int(valor_dir) > 999: return 'erro, valor maximo 999,99 por cento'    
        if int(valor_dir) > 0:
            valor_dir_extenso = ''   
            valor_dir_extenso = self.calc_3digitos(valor_dir)
        else:
            valor_dir_extenso = 'zero'
            
        if int(valor_esq) > 0:
            valor_esq_extenso = ''
            valor_esq_extenso = self.calc_3digitos(valor_esq)
            if valor_esq[-2] == '0': valor_esq_extenso = 'zero ' + valor_esq_extenso
            return valor_dir_extenso + ' ' + nome_separador + ' ' + valor_esq_extenso + ' por cento'
        else:
            return valor_dir_extenso + ' por cento'
            
                    
    def numero_por_extenso(self, numero: float | str, monetario: bool = True, moeda_unit: str ='real', moeda_plural: str ='reais', nome_separador: str = 'virgula') -> str:
        '''valor_texto = numero_por_extenso(100306000000.01)\n
        cem bilhões e trezentos e seis milhões de reais e um centavo
        '''
        C , num , centavos, cents = '0', str(numero), '', '' 
            
        def calc_centavos(cents: str):
            if int(cents[-2]) == 0 and int(cents[-1]) > 0: D = self.unidades[int(cents[-1])]
            elif int(cents[-2]) == 1 and int(cents[-1]) >= 0: D = self.especiais[int(cents[-1])]
            elif int(cents[-2]) > 1 and int(cents[-1]) == 0: D = self.dezenas[int(cents[-2])] 
            else: D = self.dezenas[int(cents[-2])] + ' e ' + self.unidades[int(cents[-1])]    
            return D
        
        num = num.replace('.','').replace(',','.') if '.' in num and ',' in num else num.replace(',', '.')
        if num == '0' or num == '0.0' or num == '0.00': return 'zero'
        num_aux = num.split('.') if '.' in num else ''
        num = str(num_aux[0]) if num_aux != '' else num
        cents = str(num_aux[1]) if num_aux != '' else ''
        cents = cents + '0' if int(len(cents)) < 2 else cents[:2]
                
        if cents != '' and cents != '0' and cents != '00':
            centavos = calc_centavos(cents)
            if monetario:
                centavos = ' e ' + centavos + ' centavo' if cents == '01' else ' e ' + centavos + ' centavos'
            else:
                if cents[-2] == '0':
                    centavos = ' ' + nome_separador + ' zero ' + centavos 
                else:
                    centavos = ' ' + nome_separador + ' ' + centavos 
                
        if not monetario:
            moeda_unit = ''
            moeda_plural = ''

        # Começa a montar as strings de numero para texto  
        if len(num) > 12:
            print('valor numerico muito grande, nao suportado, max 999 bilhoes')
            return 'valor numerico muito grande, nao suportado, max 999 bilhoes'
        elif len(num) > 9:
            C = self.calc_3digitos(num[-3:])
            M = self.calc_3digitos(num[-6:-3])
            ML = self.calc_3digitos(num[-9:-6])  
            BL = self.calc_3digitos(num[:-9])     

            if int(num[-6:-3]) > 0 and int(num[-3:]) == 0: texto_m = ' mil'
            elif int(num[-6:-3]) > 0 and int(num[-3:]) > 0: texto_m = ' mil e '
            else: texto_m = ''
                
            if int(num[-6:-3]) == 0 and int(num[-9:-6]) == 1 and int(num[-3:]) >= 1: texto_ml = ' milhão e '
            elif int(num[-6:-3]) == 0 and int(num[-9:-6]) == 1: texto_ml = ' milhão de'
            elif int(num[-6:-3]) > 0 and int(num[-9:-6]) == 1: texto_ml = ' milhão e '
            elif int(num[-6:-3]) == 0 and int(num[-9:-6]) > 1: texto_ml = ' milhões de'
            elif int(num[-6:-3]) > 0 and int(num[-9:-6]) > 1: texto_ml = ' milhões e '
            else: texto_ml = ''
            
            if int(num) == 1000000000: texto_bl = ' bilhão de'
            elif int(num) > 1000000000 and int(num[-9:]) > 0 and int(num) < 2000000000: texto_bl = ' bilhão e '
            elif int(num) > 1000000000 and int(num[-9:]) == 0: texto_bl = ' bilhões de'
            elif int(num) > 2000000000 and int(num[-9:]) > 0: texto_bl = ' bilhões e '
            else: texto_bl = ''
            
            if not monetario:
                texto_ml = texto_ml.replace(' milhão de', ' milhão')
                texto_ml = texto_ml.replace(' milhões de', ' milhões')
                texto_bl = texto_bl.replace(' bilhão de', ' bilhão')
                texto_bl = texto_bl.replace(' bilhões de', ' bilhões')

            r = BL + texto_bl + ML + texto_ml + M + texto_m + C + ' ' + moeda_plural + centavos if cents != '' else ML + texto_ml + M + texto_m + C + ' ' + moeda_plural
            return r.replace('  ', ' ') 
        elif len(num) > 6:
            C = self.calc_3digitos(num[-3:])
            M = self.calc_3digitos(num[-6:-3])
            ML = self.calc_3digitos(num[:-6])       

            if int(num[-6:-3]) > 0 and int(num[-3:]) == 0: texto_m = ' mil'
            elif int(num[-6:-3]) > 0 and int(num[-3:]) > 0: texto_m = ' mil e '
            else: texto_m = ''
                        
            if int(num) == 1000000: texto_ml = ' milhão de'
            elif int(num) > 1000000 and int(num[-6:]) > 0 and int(num) < 2000000: texto_ml = ' milhão e '
            elif int(num) > 1000000 and int(num[-6:]) == 0: texto_ml = ' milhões de'
            elif int(num) > 2000000 and int(num[-6:]) > 0: texto_ml = ' milhões e '
            else: texto_ml = ''
            
            if not monetario:
                texto_ml = texto_ml.replace(' milhão de', ' milhão')
                texto_ml = texto_ml.replace(' milhões de', ' milhões')
                
            r = ML + texto_ml + M + texto_m + C + ' ' + moeda_plural + centavos if cents != '' else ML + texto_ml + M + texto_m + C + ' ' + moeda_plural
            return r.replace('  ', ' ')  
        elif len(num) > 3:
            C = self.calc_3digitos(num[-3:])
            M = self.calc_3digitos(num[:-3])
            if cents != '': r = M + ' mil ' + moeda_plural if str(num)[-3:] == '000' else M + ' mil e ' + C + ' ' + moeda_plural + centavos
            else: r = M + ' mil ' + moeda_plural if str(num)[-3:] == '000' else M + ' mil e ' + C + ' ' + moeda_plural
            return r.replace('  ', ' ')  
        elif len(num) <= 3:
            C = self.calc_3digitos(num)
            if cents != '' and C == '': r = centavos[2:] 
            elif cents != '': r = C + ' ' + moeda_unit if int(num) == 1 else C + ' ' + moeda_plural + centavos
            else: r = C + ' ' + moeda_unit if int(num) == 1 else C + ' ' + moeda_plural
            return r.replace('  ', ' ') 
        
                            
class Gerador_de_codigo:
    
    def __init__(self):
        pass
    
    
    def comentar_linha(self, path:str, search:str):
        f = open(path, 'r')
        texto= str(f.read())
        texto = texto.replace(search, '#' + search)
        f.close()
        # time.sleep(1)
        f = open(path, 'w')
        f.write(texto)
        # time.sleep(1)
        f.close()

                        
    def template_novo_rpa(self, script_file_path:str):
        '''
        from rpa_coop import gerador_de_codigo\n
        gerador_de_codigo.template_novo_rpa( __file__ )
        '''
              
        txt = '''def main(processo=0):
    qtd_atividades = 1
    msg_log = "em andamento"
    update_status = "andamento"
    try:

        # SEU CODIGO AQUI 

        qtd_atividades = 1
        msg_log = "Concluido com sucesso"
        update_status = "sucesso"
    except Exception as e:
        msg_log = str(e)
        update_status = "erro"
        qtd_atividades = 1
    finally:
        qtd_atividades = str(qtd_atividades)
        return update_status, msg_log, qtd_atividades'''
        
        file = open(script_file_path, 'a')
        file.write(txt)
        file.close()
        self.comentar_linha(script_file_path, 'gerador_de_codigo.')
        
           
    def pandas_add_linhas_to_DataFrame(self, script_file_path:str):
        '''
        from rpa_coop import gerador_de_codigo\n
        gerador_de_codigo.pandas_add_linhas_to_DataFrame( __file__ )
        '''
        
              
        txt = '''import pandas as pd

# Exemplo dados de entrada em formato DataFrame
df = pd.DataFrame([{'cod_area': 1, 'ag': 2, 'cep': 3}, {'cod_area': 4, 'ag': 5, 'cep': 6}, {'cod_area': 7, 'ag': 8, 'cep': 9}])

# Novo DataFrame vazio que receberá os valores filtrados
df2 = pd.DataFrame()

for linha in df.itertuples():
    # FILTRAR AS AGENCIA PARES
    if int(linha.ag) % 2 == 0:
        
        CODIGO = str(linha.cod_area)
        AGENCIA = 'AG-' + str(linha.ag).zfill(2)
               
        df1 = pd.DataFrame(
            [{
            'CODIGO_AREA': CODIGO,
            'AGENCIA ': AGENCIA
            }], 
            index= None)
        df2 = pd.concat([df1, df2])
        
print(df2)'''
        
        file = open(script_file_path, 'a')
        file.write(txt)
        file.close()        
        self.comentar_linha(script_file_path, 'gerador_de_codigo.')
        
           
class Selenium:
    
    def __init__(self):
        pass
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.alert import Alert
    
    from selenium.webdriver.chrome.service import Service as ChromeService 
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options as chrome_options
    
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.options import Options as edge_options
    
    
    def driver_chrome(self):
        driver = self.webdriver.Chrome(service=(self.ChromeService(self.ChromeDriverManager().install())))
        return driver
    
    
    def driver_edge(self):
        driver = self.webdriver.Edge(service=(self.EdgeService(self.EdgeChromiumDriverManager().install())))
        return driver
    
    
    def aguardar_elemento(self, driver, xpath, espera_em_segundos=60):
        '''Espera por um elemento até o tempo máximo definido, interrompe a espera assim que encontrar o elemento'''
        elemento_esperado = self.WebDriverWait(driver, espera_em_segundos).until(self.ec.visibility_of_element_located((self.By.XPATH, xpath)))
        encontrou = str(elemento_esperado.is_displayed())
        return encontrou
        
        
class Dia_util:
    
    ano_atual = int(datetime.now().strftime('%Y'))
    dd = int(datetime.now().strftime('%d'))
    mm = int(datetime.now().strftime('%m'))
    yyyy = int(datetime.now().strftime('%Y'))
      
      
    def feriados_nacionais(self, ano= ano_atual, retorna=True, imprime=False):
        self.ano = int(ano)
        datas_arr = []
        datas_dict = {}
        self.calculo_pascoa()
        
        # Monta a data exata da Páscoa no Ano
        dtPA = date(ano, self.mes, self.dia)
        # Carnaval ocorre 47 dias antes da páscoa
        dtCN = date.fromordinal(dtPA.toordinal() - 47)
        # Corpus Christ ocorre 60 dias depois da páscoa
        dtCC = date.fromordinal(dtPA.toordinal() + 60)
        # Sexta-feira Santa ocorre 2 dias antes da páscoa
        dtSS = date.fromordinal(dtPA.toordinal() - 2)
        
        # Ano Novo
        dt_aux = f'01/01/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Confraternização - Ano Novo'})
        
        # Carnaval
        dt_aux = dtCN.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Carnaval - facultativo'})
        
        # Sexta-feira Santa
        dt_aux = dtSS.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Sexta-feira Santa'})
        
        # Pascoa
        dt_aux = dtPA.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Pascoa'})
        
        # Tiradentes
        dt_aux = f'21/04/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Tiradentes'})
        
        # Dia do Trabalho
        dt_aux = f'01/05/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Dia do Trabalho'})
        
        # Corpus Christ
        dt_aux = dtCC.strftime('%d/%m/%Y')
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Corpus Christ - facultativo'})
        
        # 07 de Setembro - Independencia do Brasil
        dt_aux = f'07/09/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '07 Setembro - Independencia do Brasil'})
        
        # 12 de Outubro - Nossa Sra Aparecida
        dt_aux = f'12/10/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '12 de Outubro - Nossa Sra Aparecida'})
        
        # 02 de Novembro - Finados
        dt_aux = f'02/11/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '02 de Novembro - Finados'})
        
        # 15 de Novembro - Proclamação da República
        dt_aux = f'15/11/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : '15 de Novembro - Proclamação da República'})
        
        # Natal
        dt_aux = f'25/12/{self.ano}'
        datas_arr.append(dt_aux)
        datas_dict.update({dt_aux : 'Natal'})
                   
        self.feriados = datas_arr
        
        if imprime:
            # Imprimir data e descrição
            for dt, descr in datas_dict.items():
                print(dt, descr)
                
        if retorna:
            # return datas_dict
            return datas_arr
    
    
    def dias_uteis_mes(self, mes=mm, ano=yyyy, imprime=False):
        mes = int(mes)
        ano = int(ano)
        import calendar
        calc_dias = calendar.monthrange(ano, mes)
        total_dias_mes = calc_dias[1] 
        
        semana = [
            'Segunda-feira',
            'Terça-feira',
            'Quarta-feira',
            'Quinta-Feira',
            'Sexta-feira',
            'Sábado',
            'Domingo'
            ]
        
        self.feriados_nacionais(ano, False)
        feriados = self.feriados
        dias_uteis_br = []
        dias_uteis_us = []
        
        for x in range(1, total_dias_mes+1):
            dia_us = date(ano, mes, x)
            dia_br = str(x).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano).zfill(4)
            indice_semana = dia_us.weekday()
            dia_da_semana = semana[indice_semana]
            if dia_da_semana != 'Sábado' and dia_da_semana != 'Domingo':
                if dia_br not in feriados:
                    if imprime:
                        print(dia_br, dia_da_semana)
                    dias_uteis_br.append(dia_br)
                    dias_uteis_us.append(str(ano).zfill(4) + '/' + str(mes).zfill(2) + '/' + str(x).zfill(2))
        
        # return dias_uteis_us
        return dias_uteis_br

    
    def hoje_eh_dia_util(self, dia=dd, mes=mm, ano=yyyy):
        hoje = str(dia).zfill(2) + '/' + str(mes).zfill(2) + '/' + str(ano).zfill(4)
        dias_uteis_br = self.dias_uteis_mes(mes, ano, False)
        # print()
        # print('hoje: ', hoje)
        if hoje in dias_uteis_br:
            # print('OK - Hoje eh dia útil')
            util_day = True
        else:
            # print('NAO - Hoje não eh dia útil')
            util_day = False
        return util_day
            

    def calculo_pascoa(self):
        p1 = (19 * (self.ano % 19) + 24) % 30
        p2 = (2 * (self.ano % 4) + 4 * (self.ano % 7) + 6 * p1 + 5) % 7
        res = p1 + p2
        if res > 9:
            self.dia = res - 9
            self.mes = 4
        else:
            self.dia = res + 22
            self.mes = 3


    def dia_util_anterior(self, dd_mm_yy=True, yy_mm_dd=False):
        hoje = datetime.now()
        dia_anterior = (hoje - timedelta(days=1)).strftime('%d-%m-%Y')
        eh_util = False
        while not eh_util:
            hoje = hoje - timedelta(days=1)
            dd = hoje.strftime('%d')
            mm = hoje.strftime('%m')
            yy = hoje.strftime('%Y')
            eh_util = self.hoje_eh_dia_util(dd, mm, yy)
            if eh_util:
                dia_br = dd.zfill(2) + '-' + mm.zfill(2) + '-' + yy.zfill(4)
                dia_us = yy.zfill(4) + '-' + mm.zfill(2) + '-' + dd.zfill(2)
                
        if yy_mm_dd:
            dia_anterior = dia_us
        else:
            dia_anterior = dia_br
            
        return dia_anterior
    
    
    def dia_util_posterior(self, dd_mm_yy=True, yy_mm_dd=False):
        hoje = datetime.now()
        dia_util_proximo = (hoje + timedelta(days=1)).strftime('%d-%m-%Y')
        eh_util = False
        while not eh_util:
            hoje = hoje + timedelta(days=1)
            dd = hoje.strftime('%d')
            mm = hoje.strftime('%m')
            yy = hoje.strftime('%Y')
            eh_util = self.hoje_eh_dia_util(dd, mm, yy)
            if eh_util:
                dia_br = dd.zfill(2) + '-' + mm.zfill(2) + '-' + yy.zfill(4)
                dia_us = yy.zfill(4) + '-' + mm.zfill(2) + '-' + dd.zfill(2)
                
        if yy_mm_dd:
            dia_util_proximo = dia_us
        else:
            dia_util_proximo = dia_br
            
        return dia_util_proximo
        
        
class Get_errors:
    import traceback
    import re
    import pyautogui as p 
  
    def __init__(self):
        pass
    
    def pegar_erro(self, cod_rpa = '123', id_fila = '123', pasta_img_erro = 'H:\\rpa\\ERROS_IMAGENS_CAPTURADAS\\erro_rpa\\') -> str:
        '''usar dentro do except do try, captura informações do erro'''
        try:
            nome_img_erro = f'{pasta_img_erro}erro_rpa_{cod_rpa}__id_{id_fila}.png'
        except:
            pass
        self.p.screenshot(nome_img_erro)
        str_traceback = self.traceback.format_exc().replace('Traceback (most recent call last):', '').replace('^','').replace('~','').replace('File ','').replace('"','').replace("'","")
        try:
            dica1 = str(self.re.findall('line\s\d+', str_traceback)[0]).replace('line', 'linha') + ' em ' + str(self.re.findall('\D:.+py', str_traceback)[0]).split('\\')[-1]
        except:
            dica1 = ''
        try:
            dica2 = str(self.re.findall('line\s\d+', str_traceback)[1]).replace('line', 'linha') + ' em ' + str(self.re.findall('\D:.+py', str_traceback)[1]).split('\\')[-1]
        except:
            dica2 = ''
        try:
            list_traceback = str_traceback.splitlines()
            erro = str(list_traceback[-3]).strip() + ' : ' + str(list_traceback[-1]).strip()
            msg_log = f'{dica1} --> {str(list_traceback[2]).strip()} \n{dica2} --> {erro}'
        except:
            try:
                list_traceback = str_traceback.splitlines()
                msg_log = f'{dica1} --> {str(list_traceback[2]).strip()} \n{dica2}'
            except:      
                msg_log = f'{dica1} \n{dica2}'
        msg_log = msg_log + f'\nImagem do erro em... {nome_img_erro}'
        msg_log = msg_log[:490]
        return msg_log

    
    




