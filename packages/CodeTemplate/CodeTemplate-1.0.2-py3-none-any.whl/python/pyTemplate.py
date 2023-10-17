import datetime
import time
import logging
import ctypes
from psycopg2 import Error, connect
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from potatoscript.potatoConfig import Config as Config
from potatoscript.potatoEmail import Config as EmailConfig
from potatoscript.potatoPostgreSQL import Config as PostgreSQLConfig
from colorama import init, Fore, Back, Style

class DatabaseConnector:
    def __init__(self, db, host, user, pw, port, schemas):
        self.db = db
        self.host = host
        self.user = user
        self.pw = pw
        self.port = port
        self.schemas = schemas

    def connect(self):
        try:
            # PostgreSQLConfigクラスを使用してデータベースに接続
            connection = PostgreSQLConfig(self.db, self.host, self.user, self.pw, self.port, self.schemas)
            return connection
        except (Exception, Error) as error:
            # データベースへの接続中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"データベースへの接続エラー: {error}")

class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, sender):
        # EmailConfigクラスを使用してEmail通知のための初期設定
        self.email_config = EmailConfig(smtp_server, smtp_port, sender)

    def send_email(self, subject, message_header, message_body, message_footer, recipient, recipient_cc):
        try:
            # Email通知の送信
            self.email_config.send(subject, message_header, message_body, message_footer, recipient, recipient_cc)
        except Exception as e:
            # Email通知の送信中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"Email通知の送信エラー: {e}")

class Index:
    def __init__(self):
        # Configクラスを使用して設定ファイルから設定を読み込む
        self.config = Config('config.ini')

        self.recipient = self.config.get('EMAIL_ITEM', 'recipient')
        self.recipient_cc = self.config.get('EMAIL_ITEM', 'recipient_cc')
        self.subject = self.config.get('EMAIL_ITEM', 'subject')
        self.message_header = self.config.get('EMAIL_ITEM', 'message_header')
        self.message_header2 = self.config.get('EMAIL_ITEM', 'message_header2')
        self.message_footer = self.config.get('EMAIL_ITEM', 'message_footer')
        self.message_footer2 = self.config.get('EMAIL_ITEM', 'message_footer2')
        self.log = self.config.get('PARAM', 'log')

        # DatabaseConnectorおよびEmailNotifierの初期化
        self.database_connector = DatabaseConnector(
            self.config.get('DB', 'db'),
            self.config.get('DB', 'host'),
            self.config.get('DB', 'user'),
            self.config.get('DB', 'pw'),
            self.config.get('DB', 'port'),
            self.config.get('DB', 'schemas')
        )
        self.email_notifier = EmailNotifier(
            self.config.get('EMAIL', 'smtp_server'),
            self.config.get('EMAIL', 'smtp_port'),
            self.config.get('EMAIL', 'sender')
        )

        # その他の変数の初期化...
        self.console_title = self.config.get('PARAM', 'console_title')

        console_handle = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.kernel32.SetConsoleTitleW(self.console_title)

        init(autoreset=True)                                            # autoreset=Trueを設定して、Coloramaのテキストリセットを有効にします。
        logging.basicConfig(filename=self.log, level=logging.INFO)

    def db_fetchall(self,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connect()
            # クエリの実行
            return db_connection.fetchall(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def db_commit(self,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connect()
            # クエリの実行
            return db_connection.commit(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def db_commit_many(self, query, values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connect()
            # クエリの実行
            return db_connection.commit_many(query, values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)


    def run_interval(self):
        while True:
            print("システムを起動しています")
            if not self.in_process_flag:
                self.in_process_flag = True
                try:
                    self.main()
                finally:
                    self.in_process_flag = False
            interval = int(self.interval)
            time.sleep(interval)

    
    def handle_error(self, error):
        print("Error2:", error)
        logging.basicConfig(filename="error.log", level=logging.ERROR)
        # 現在の日時を取得
        now = datetime.datetime.now()
        # エラーログを記録
        logging.error(now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(error))

    def print_info(self, OKNG,info):
        now = datetime.datetime.now()
        if OKNG == "OK":
            # OKの場合のメッセージ
            message = f" {Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}{now.strftime('%H:%M:%S')}{Back.BLACK} {info} {Style.NORMAL}"
        else:
            # NGの場合のメッセージ
            message = f" {now.strftime('%H:%M:%S')}{Fore.WHITE}{Back.RED}{Style.BRIGHT} {info} {Style.NORMAL}"
            log_message = f" {now.strftime('%H:%M:%S')} {info}"
        print(message)
        logging.info(log_message)

    def send_notification_email(self, message_body):
        recipient = self.recipient.split(';')
        recipient_cc = self.recipient_cc.split(';')
        subject = self.subject
        message_header = f"{self.message_header}<br><br>"
        message_header += f"<font style='color:blue;font-weight:bold;font-size:18px'>{self.message_header2}</font><br><br>"
        message_footer = f"<br><br>{self.message_footer}<br><br>{self.message_footer2}"
        # Email通知の送信
        self.email_notifier.send_email(subject, message_header,message_body, message_footer, recipient, recipient_cc)

