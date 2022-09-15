# SingleAndMultiThreads
Esse projeto é uma calculadora funcionando no servidor local, com arquitetura cliente servidor utilizando a biblioteca socket e threading.

Dois exemplos de uso da calculadora remota:

1°   cliente utilizando o servidor single-thread (servSingleThreading).

2 °  cliente utilizando o servidor multi-threads (servMultiThreading).

Detalhes:
* cliente é uma interface do software que não tem poder de execução de calculo. Apenas conecta os argumentos e envia ao servidor

* Servidor processa a informação e devolve a menssagem ao cliente.


