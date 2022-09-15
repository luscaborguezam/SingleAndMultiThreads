from servidor import Servidor

#instanciando a classe servidor singlethread
serv = Servidor('localhost', 9000)
serv.start()
