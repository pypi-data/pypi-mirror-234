import logging
import src.database.connection as database
import src.database.utils as utils
import src.api.api_mplace as api_Mplace
from src.database.queries import IntegrationType
from src.jobs.system_jobs import OnlineLogger
from src.database.utils import DatabaseConfig
import src.api.okinghub as api_okHUB
import src.api.okvendas as api_okVendas
from src.api import slack
from src.database import queries
import src
from threading import Lock

from src.jobs.utils import executa_comando_sql

logger = logging.getLogger()
send_log = OnlineLogger.send_log
lock = Lock()


def job_send_stocks(job_config_dict: dict):
    """
    Job para realizar a atualização dos estoques padrão
    Args:
        job_config_dict: Configuração do job
    """
    with lock:
        global depositoMplace
        global unidade_distribuicao
        db_config = utils.get_database_config(job_config_dict)
        # Exibe mensagem monstrando que a Thread foi Iniciada
        logger.info(f'==== THREAD INICIADA -job: ' + job_config_dict.get('job_name'))
        # LOG de Inicialização do Método - Para acompanhamento de execução
        send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
                 f'Estoque - Iniciado', 'exec', 'envia_estoque_job', 'ESTOQUE')
        # Executa o Comando da Semaforo Antes do Query Principal
        if job_config_dict['executar_query_semaforo'] == 'S':
            logger.info(f'Executando a query semáforo')
            executa_comando_sql(db_config, job_config_dict)

        # Executa a query Principal
        logger.info(f'Executando a query principal')
        stocks = query_stocks_erp(job_config_dict, db_config)

        # atualizados = []
        if stocks is not None and len(stocks) or 0 > 0:
            send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
                     f'Total de estoques a serem atualizados: {len(stocks)}', 'info', 'envia_estoque_job', 'ATUALIZAÇÃO')

            api_stocks = []
            for stock in stocks:
                try:
                    # time.sleep(1)
                    if api_stocks.__len__() < 50:
                        api_stocks.append(stock)
                    else:
                        send_log(job_config_dict.get('job_name'), False, False, f'Enviando Pacote: {api_stocks.__len__()}',
                                 'info', 'envia_estoque_job', 'ESTOQUE')
                        if src.client_data['operacao'].lower().__contains__('okvendas'):
                            response = api_okVendas.send_stocks(api_stocks)
                            unidade_distribuicao = api_stocks[0]['unidade_distribuicao']
                        elif src.client_data['operacao'].lower().__contains__('mplace'):
                            response = api_Mplace.send_stocks_mplace(api_stocks)
                            depositoMplace = api_stocks[0]['dc_code']  # Procurar maneira de fazer get do deposito 9643 1704
                        else:
                            response = api_okHUB.send_stocks_hub(api_stocks)

                        api_stocks = []
                        send_log(job_config_dict.get('job_name'), False, False, f'Tratando retorno', 'info', 'envia_estoque_job',
                                 'ESTOQUE')
                        validade_response_stocks(response, db_config, job_config_dict)

                except Exception as e:
                    send_log(job_config_dict.get('job_name')
                             , job_config_dict.get('enviar_logs')
                             , True
                             , f'Erro genérico ao atualizar o estoque, Erro: {str(e)}'
                             , 'error'
                             , 'envia_estoque_job'
                             , 'ESTOQUE')

            # Se ficou algum sem processa
            if api_stocks.__len__() > 0:
                send_log(job_config_dict.get('job_name'), False, False, f'Enviando Pacote: {api_stocks.__len__()}', 'info',
                         'ESTOQUE', 'ESTOQUE')
                if src.client_data['operacao'].lower().__contains__('okvendas'):
                    response = api_okVendas.send_stocks(api_stocks)
                    unidade_distribuicao = api_stocks[0]['unidade_distribuicao']
                elif src.client_data['operacao'].lower().__contains__('mplace'):
                    response = api_Mplace.send_stocks_mplace(api_stocks)
                    depositoMplace = api_stocks[0]['dc_code']  # Procurar maneira de fazer get do deposito
                else:
                    response = api_okHUB.send_stocks_hub(api_stocks)
                send_log(job_config_dict.get('job_name'), False, False, f'Tratando retorno', 'info', 'envia_estoque_job', 'ESTOQUE')
                validade_response_stocks(response, db_config, job_config_dict)
        else:
            send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
                     f'Nao ha produtos para atualizar estoque no momento', 'warning', 'envia_estoque_job', 'ESTOQUE')


def query_stocks_erp(job_config_dict: dict, db_config: DatabaseConfig):
    """
    Consulta no banco de dados os estoques pendentes de atualização padrão
    Args:
        job_config_dict: Configuração do job
        db_config: Configuração do banco de dados

    Returns:
    Lista de estoques para realizar a atualização
    """
    stocks = None
    if db_config.sql is None or db_config.sql == '':
        slack.register_warn("Query estoque de produtos nao configurada!")
        send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
                 f'Query estoque de produtos nao configurada', 'warning', 'envia_estoque_job', 'ESTOQUE')
    else:
        try:
            # monta query com EXISTS e NOT EXISTS
            # verificar se já possui WHERE
            newsql = utils.final_query(db_config)
            conexao = database.Connection(db_config)
            conn = conexao.get_conect()
            cursor = conn.cursor()

            print("========================================")
            if src.print_payloads:
                print(newsql)
            print("=== Executando Query PRINCIAPL ")
            print("========================================")

            cursor.execute(newsql.lower().replace('#v', ','))

            print("========================================")
            print("=== RETORNOU DO BANCO ")
            print("========================================")
            rows = cursor.fetchall()
            # print(rows)
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            conn.close()
            stocks = []
            if len(results) > 0:
                stocks = stock_dict(results)

        except Exception as ex:
            send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True, f'{str(ex)}', 'error',
                     'envia_estoque_job', 'ESTOQUE')
            if src.exibir_interface_grafica:
                raise ex
            else:
                logger.error(f'Falha na conexão com o bando de dados: {str(ex)}')

    return stocks


def stock_dict(stocks):
    lista = []
    for row in stocks:
        if src.client_data['operacao'].lower().__contains__('mplace'):
            pdict = {
                'sku_seller_id': str(row['sku']),
                'variation_option_id': int(row['variation_id']),
                'dc_code': str(row['deposito']),
                'quantity': int(row['quantidade']),
                'deactivation_date': ""
            }
        elif src.client_data['operacao'].lower().__contains__('okvendas'):
            pdict = {
                'unidade_distribuicao': str(row['deposito']),
                'produto_id': '',
                'codigo_erp': str(row['sku']),
                'quantidade_total': int(row['quantidade']),
                'quantidade_reserva': 0,
                'protocolo': '',
                'parceiro': 0
            }
        else:
            pdict = {
                'sku': str(row['sku']),
                'token': str(src.client_data.get('token_oking')),
                'quantidade': int(row['quantidade']),
                'deposito': str(row['deposito'])
            }

        lista.append(pdict)

    return lista


def validade_response_stocks(response, db_config, job_config_dict):
    logger.info("Validando o Response de Estoque")
    if response is not None:
        conexao = database.Connection(db_config)
        conn = conexao.get_conect()
        cursor = conn.cursor()

        print(f'=== Operacao: ' + src.client_data['operacao'].lower())
        # Percorre todos os registros
        if src.client_data['operacao'].lower().__contains__('mplace'):
            for item in response:
                identificador = item.sku_seller_id
                identificador2 = depositoMplace  # colocar variavel Deposito
            if item.success == 1 or item.success == 'true' or item.message == 'Estoque não atualizado, produto não encontrado ou desativado!':
                msgret = 'SUCESSO'
            else:
                msgret = item.message
                send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
                         f'Erro ao atualizar estoque para o sku: {identificador},'
                         f'Deposito:{identificador2} {msgret}',
                         'warning',
                         'envia_estoque_job', 'ESTOQUE')

            try:
                cursor.execute(queries.get_insert_update_semaphore_command(db_config.db_type),
                               queries.get_command_parameter(db_config.db_type, [identificador, identificador2,
                                                                                 IntegrationType.ESTOQUE.value,
                                                                                 msgret]))
                # atualizados.append(response['identificador'])
            except Exception as e:
                send_log(job_config_dict.get('job_name')
                         , job_config_dict.get('enviar_logs')
                         , True
                         ,
                         f'Erro ao atualizar estoque do sku: {identificador}, Deposito:{identificador2},'
                         f'Erro: {str(e)}'
                         , 'error'
                         , 'envia_estoque_job'
                         , 'ESTOQUE')

        elif src.client_data['operacao'].lower().__contains__('okvendas'):
            db = database.Connection(db_config)
            conn = db.get_conect()
            cursor = conn.cursor()
            try:
                for item in response:
                    if item.Status == 1:
                        msgret = 'SUCESSO'
                    else:
                        msgret = item.Message[:150]
                    if item.Identifiers is not None:
                        if src.print_payloads:
                            print(f"Identificadores: Identificador = {item.Identifiers}, Identificador2 = {item.Identifiers2}")
                        for identificador in item.Identifiers:
                            cursor.execute(queries.get_semaphore_command_data_sincronizacao(db_config.db_type),
                                           queries.get_command_parameter(db_config.db_type,
                                                                         [identificador, item.Identifiers2,
                                                                          IntegrationType.ESTOQUE.value,
                                                                          msgret]))
                count = cursor.rowcount
                cursor.close()
                conn.commit()
                conn.close()
                return count > 0
            except Exception as e:
                send_log(job_config_dict.get('job_name')
                         , job_config_dict.get('enviar_logs')
                         , True
                         ,
                         f'Erro ao atualizar estoque do sku: {identificador},'
                         f'Erro: {str(e)}'
                         , 'error'
                         , 'envia_estoque_job'
                         , 'ESTOQUE')

            # for item in response:
            #     identificador = item.codigo_erp
            #     identificador2 = unidade_distribuicao
            #     if item.Status == 1:
            #         msgret = 'SUCESSO'
            #     else:
            #         msgret = item.Message
            #         send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
            #                  f'Erro ao atualizar estoque para o sku: {identificador}, {msgret}',
            #                  'warning',
            #                  'ESTOQUE', identificador)
            #     try:
            #         cursor.execute(queries.get_insert_update_semaphore_command(db_config.db_type),
            #                        queries.get_command_parameter(db_config.db_type,
            #                                                      [identificador, identificador2,
            #                                                       IntegrationType.ESTOQUE.value,
            #                                                       msgret]))
            #     except Exception as e:
            #         send_log(job_config_dict.get('job_name')
            #                  , job_config_dict.get('enviar_logs')
            #                  , True
            #                  ,
            #                  f'Erro ao atualizar estoque do sku: {identificador}, Deposito:{identificador2},'
            #                  f'Erro: {str(e)}'
            #                  , 'error'
            #                  , 'ESTOQUE'
            #                  , 'ESTOQUE')

        else:
            for item in response:
                identificador = item.identificador
                identificador2 = item.identificador2
                if item.sucesso == 1 or item.sucesso == 'true':
                    msgret = 'SUCESSO'
                else:
                    msgret = item.mensagem
                    send_log(job_config_dict.get('job_name'), job_config_dict.get('enviar_logs'), True,
                             f'Erro ao atualizar estoque para o sku: {identificador},'
                             f'Deposito:{identificador2} {msgret}',
                             'warning',
                             'envia_estoque_job', 'ESTOQUE')
                # Mesmo se der erro retira da Fila, mas grava a mensagem no Banco
                try:
                    cursor.execute(queries.get_insert_update_semaphore_command(db_config.db_type),
                                   queries.get_command_parameter(db_config.db_type, [identificador, identificador2,
                                                                                     IntegrationType.ESTOQUE.value,
                                                                                     msgret]))
                    # atualizados.append(response['identificador'])
                except Exception as e:
                    send_log(job_config_dict.get('job_name')
                             , job_config_dict.get('enviar_logs')
                             , True
                             ,
                             f'Erro ao atualizar estoque do sku: {item.identificador}, Deposito:{item.identificador2}, '
                             f'Erro: {str(e)} '
                             , 'error'
                             , 'envia_estoque_job'
                             , 'ESTOQUE')

        cursor.close()
        conn.commit()
        conn.close()
