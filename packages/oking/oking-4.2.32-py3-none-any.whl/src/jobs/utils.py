import logging
import src
import src.database.connection as database
from src.jobs.system_jobs import OnlineLogger

logger = logging.getLogger()
send_log = OnlineLogger.send_log


def executa_comando_sql(db_config, job_config):
    conexao = database.Connection(db_config)
    conn = conexao.get_conect()
    cursor = conn.cursor()
    if db_config.db_type.lower() == 'firebird':
        semaforo_sql = db_config.semaforo_sql.replace('openk_semaforo.', "")
    else:
        semaforo_sql = db_config.semaforo_sql

    if src.print_payloads:
        print(semaforo_sql)

    try:
        logger.info(job_config.get('job_name') + ' ===============================')
        logger.info(job_config.get('job_name') + ' == Executando Query Semáforo ==')
        cursor.execute(semaforo_sql)
        logger.info(job_config.get('job_name') + ' == Query Semáforo Executada  ==')
        logger.info(job_config.get('job_name') + ' ===============================')

        # Fecha o Cursor e a Conexão
        cursor.close()
        conn.commit()
        conn.close()

    except Exception as ex:
        send_log(job_config.get('job_name'), job_config.get('enviar_logs'), True,
                 f'Erro ao executar Comando SQL: {ex}', 'warning', job_config.get('job_name')
                 , job_config.get('job_name'))
