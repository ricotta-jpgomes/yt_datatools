Conjunto de notebooks que buscam recriar, com algumas limitações, claro, o YouTube Data Tools, da galera da Digital Methods Initiative. Por enquanto, temos três módulos:

- Um mecanismo de busca simples para canais (retorna um csv com as informações dos canais obtidos)
- Um mecanismo de busca simples para vídeos (retorna um csv com as informações dos canais obtidos)
- Um sisteminha de busca para obter uma rede de vídeos relacionados, a partir de um vídeo seed definido pelo usuário

O projeto inteiro foi desenvolvido utilizando python, desde a biblioteca para criar e gerenciar um cliente de API, desenvolvida pelo Google, até libs como os, sys, e python-dotenv para gerenciar minha chave de api e arquivos .py externos. 
