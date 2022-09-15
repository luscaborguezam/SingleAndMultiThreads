# servidor.py
import socket


class Servidor():
    """
    Classe Servidor - Calculadora Remota - API Socket
    """

    # 1° - Método __init__, o qual serve para inicialiar os argumentos
    # host(ip) -- port(porta,a qual tem que ser diferente das portas que ja estao rodando no pc)
    def __init__(self, host, port):
        """
        Construtor da classe Servidor
        """
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # OBJETO TCP,QUE RECEBE AS CONFIGURAÇÕES DO SOCKET
        # socket(tipo/classes de endereço)
        # socket_AF_INET - classe de endereços padrão
        # SOCK_STREAM - modo TCP



    def start(self):
        """
        inicia a execução do serviço
        """
        endpoint = (self._host, self._port)
        try:
            self._tcp.bind(endpoint)  # anexar o servoço ao ip e porta
            self._tcp.listen(1)  # habilitar a escuta pro cliente,ou seja,estou apto a receber clientes
            print(f"Servidor iniciado em {self._host}:{self._port}")
            while True:
                con, client = self._tcp.accept()  # comando bloqueante,ele fica parado ai ate o cliente se conectar
                self._service(con, client)
        except Exception as e:
            print("Erro ao inicializar o servidor ", e.args)


    def _service(self, con, client):
        """
        Implementa o serviço de calculadora remota
        :param con: objeto socket utilizado para enviar e receber os dados
        :param client: é o endereço e porta do cliente
        """

        print("Atendendo cliente ", client)
        operadores = ['+', '-', '*', '/']
        while True:
            try:
                msg = con.recv(1024)
                msg_s = str(msg.decode('ascii'))  # 'op1OPERATORop2' -> '10+2'
                op = 'none'
                # identificar a operação
                for x in operadores:
                    if msg_s.find(x) > 0:
                        op = x
                        msg_s = msg_s.split(op)  # '10+2' -> split(+) -> ['10', '2']
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

                # enviar a resposta
                con.send(bytes(str(resp), 'ascii'))
                print(client, " -> requisiçãoa atendida")

            except OSError as e:
                # 1° - erro de conexão
                print("Erro de conexão ", client, ": ", e.args)
                return  # encerra o método service
            except Exception as e:
                # 2° - excessão geral
                print("Erro nos dados recebidos do cliente ->  ", client, ": ", e.args)
                con.send(bytes(f'{msg_s}\n{op}\nErro: {e}', 'ascii'))
