import socket
# Socket provê a comunicação entre duas pontas (fonte e destino) - também conhecido como
# two-way communication - entre dois processos que estejam na mesma máquina (Unix Socket)
# ou na rede (TCP/IP Sockets). Na rede, a representação de um socket se dá por ip:porta , por exemplo: 127.0.0.1:4477 (IPv4)
import threading


class Servidor():
    """
    Classe Servidor - Calculadora Remota - API Socket
    """

    # 1° - Método __init__ inicializa os argumentos(atributos) da classe Servidor
    # O socket API o servidor sempre vai rodar na máquina com um determinado IP e porta de comunicação
    # host(ip) -- port(porta,a qual tem que ser diferente das portas que ja estao rodando no pc)
    def __init__(self, host, port):
        """
        Método Construtor da classe Servidor
        """
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.AF_INET - Conjunto de endereços padrão global
        # socket.SOCK_STREAM - Modo TCP
        # self._tcp é OBJETO TCP,QUE RECEBE AS CONFIGURAÇÕES DO SOCKET

    def start(self):
        """
        Método que inicializa a execução do serviço
        """
        # Tupla(IP:PORTA), onde o servidor está fornecendo o serviço
        endpoint = (self._host, self._port)

        try:
            # anexar socket (slf_tcp) a um ip e porta
            self._tcp.bind(endpoint)
            # habilitar a escuta pro cliente,ou seja,estou apto a receber clientes
            self._tcp.listen(1)
            print(f"Servidor iniciado em {self._host}:{self._port}")
            while True:
                con, client = self._tcp.accept()
                # método que oferece o serviço ao cliente
                # comando bloqueante, nada acontece até um cliente se conectar
                self._service(con, client)

        except Exception as e:
            print("Erro ao inicializar o servidor ", e.args)

    def _service(self, con, client):
        """
        Método privado que Implementa o serviço de calculadora remota
        :param con: objeto socket utilizado para enviar e receber os dados
        :param client: é o endereço e porta do cliente
        """

        print("Atendendo cliente ", client)
        operadores = ['+', '-', '*', '/']
        while True:
            try:
                # a conexao com socket é feita com dados brutos (bytes tabela ascii)
                msg = con.recv(1024)
                # 'Operando1OperaçãoOpeando2' ex: '10+2'
                msg_s = str(msg.decode('ascii'))
                op = 'none'
                # identificar a operação
                for x in operadores:
                    if msg_s.find(x) > 0:
                        op = x
                        msg_s = msg_s.split(op)
                        # ex: '10+2' -> split(+) -> ['10', '2']
                        break
                if op == '+':
                    resp = float(msg_s[0]) + float(msg_s[1])
                elif op == '-':
                    resp = float(msg_s[0]) - float(msg_s[1])
                elif op == '*':
                    resp = float(msg_s[0]) * float(msg_s[1])
                elif op == '/':
                    resp = float(msg_s[0]) / float(msg_s[1])
                else:
                    resp = f"Operação Inválida"

                # enviar a informação(resposta) em bytes(ascii)
                con.send(bytes(str(resp), 'ascii'))
                print(client, " -> requisiçãoa atendida")

            except OSError as e:
                # OsError(excessões de I/O) - erro de conexão
                print("Erro de conexão ", client, ": ", e.args)
                return  # encerra o método service
            except Exception as e:
                # 2° - excessão geral
                print("Erro nos dados recebidos do cliente ->  ", client, ": ", e.args)
                con.send(bytes(f'Erro:', 'ascii'))


class ServidorMT(Servidor):
    '''
    Classe ServidorMT - Calculadora Remota - Multithreading'
    '''

    def __init__(self, host, port):
        """
        Método construtor da classe ServidorMT
        """
        # metodo super() para invocar o construtor da classe Servidor passando ip e porta
        super().__init__(host, port)
        self.__threadPool = {}

    def start(self):
        """
        Método que inicializa a execução do serviço
        """
        # Tupla(IP:PORTA), onde o servidor está fornecendo o serviço
        endpoint = (self._host, self._port)

        try:
            # anexar socket (slf_tcp) a um ip e porta
            self._tcp.bind(endpoint)
            # habilitar a escuta pro cliente,ou seja,estou apto a receber clientes
            self._tcp.listen(1)
            print(f"Servidor iniciado em {self._host}:{self._port}")
            while True:
                # comando bloqueante, nada acontece até um cliente se conectar
                con, client = self._tcp.accept()
                # para cada cliente cria uma thread que executa o self._service
                self.__threadPool[client] = threading.Thread(target=self._service, args=(con, client))
                # comando não bloqueante
                self.__threadPool[client].start()
                # Em uma thread roda o método start

        except Exception as e:
            print("Erro ao inicializar o servidor ", e.args)