from servidor import ServidorMT
# instanciando a classe servidor multithread
servMT = ServidorMT('localhost', 9000)
servMT.start()
