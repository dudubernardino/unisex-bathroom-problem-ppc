# ⛷️ Problema da Pista de Esqui 🎿

[![Python 3.9.13](https://img.shields.io/badge/python-3.9.13-blue.svg)](https://www.python.org/downloads/release/python-3913/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-blue)](https://github.com/PyCQA/pylint)

## Instrução de primeiro uso em linux

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install pip-tools
$ make req-install
$ make run
```

## Introdução

Esquiar é uma atividade muito praticada em países de clima frio durante o inverno. Um dos locais mais apreciados é a estação de esqui de Gornergrat nos Alpes, localizada na cidade de Zermatt na Suiça. Gornergrat é famosa pelo pico Matterhorn, pico que ilustra as embalagens do famoso chocolate Toblerone....

Esse trabalho visa simular o controle do elevador de uma pista de ski.

## Descrição do Projeto

### Regras Gerais

Esse problema é basicamente um produtos-consumidor com quatro filas. Para simplificar nosso problema vamos considerar uma fila bem grande para não ocorrer transbordamento (consideramos filas com tamanho 20).

Cada esquiador deverá chegar no elevador com intervalo de 1 segundo. Fazer um daemon que cria um
esquiador por segundo.

Executar o programa com 120 (cento e vinte) esquiadores. O tempo total de execução do programa deve ser de aproximadamente 2 minutos.

O elevador deverá funcionar a cada 5 segundos, isto é, a cada 5 seg o processo Elevador vai retirar até 4 esquiadores das filas.

Ao final da execução deve exibir os seguintes resultados:

- Taxa de aproveitamento, número de assentos ocupados dividido pelo número total de assentos
- Tempo médio que o esquiador espera na fila (discriminar o tempo por fila e o tempo médio total)

### Implementação

O trabalho prático consiste em escrever um programa em C, C++, Java ou Python para simular o controle do elevador. Não precisa fazer interface gráfica.
Não poderá haver deadlock nem starvation.

## Descrição do Problema

A nossa pista de ski tem uma cadeira quadrupla, com capacidade de quatro pessoas por vez. Para isso são organizadas quatro filas de carregamento distintas:

```txt
LS (Left Single): Fila de uma pessoa no lado esquerdo
LT (Left Triple): Fila de uma tripla no lado esquerdo
RT (Right Triple): Fila de uma tripla no lado direito
RS (Right Single): Fila de uma pessoa no lado direito
```

Sabemos que, na realidade, as pessoas não se alinham apenas em triplas e individuais, elas se alinham às vezes em duplas, às vezes em triplas, e às vezes em quadrupla. Isso, no entanto, aumenta a complexidade do nosso problema, então vamos considerar apenas triplas e individuais. Abaixo um diagrama do esquema proposto.

[![visualização do problema](https://i.imgur.com/k0MEkSW.png)](https://i.imgur.com/k0MEkSW.png)

Nas filas triplas, 3 pessoas dessa fila se senta no elevador, que pode ser completado com pessoas das filas individuais. A seguir a explicação do algoritmo.

## Procedimentos

### Esquiador selecionar a fila de carregamento

Um esquiador (isto é, um processo concorrente), ao chegar ao elevador de esqui, olha para o comprimento de cada fila (isto é, conta o número de pessoas) e escolhe a fila a entrar conforme o seguinte algoritmo:

1. Escolhe a fila LS se o tamanho da fila LS for:

   a) Menor que 2 \* tamanho da fila LT, E

   b) Menor que 2 \* tamanho da fila RT, E

   c) Menor que o tamanho da fila RS.

2. Escolhe a fila RS se o tamanho da fila RS for:

   a) Menor que 2 \* tamanho da fila LT, E

   b) Menor que 2 \* tamanho da fila RT, E

   c) Menor ou igual ao tamanho da fila LS.

3. Escolhe a fila LT se o comprimento da fila LT for menor ou igual ao tamanho da fila RT, senão,

4. Escolhe a fila RT

### Carregar o elevador

Considere que existe um processo Elevador que retira os esquiadores das filas conforme o procedimento
abaixo.

As filas LT e RT tem a prioridade sobre as filas LS e RS que são servidas alternadamente quando ambas não
estão vazias. Quer dizer, se LT está vazio, vai servir RT seguidamente até ter pessoas suficiente na fila LT. Se as filas LT ou RT tiver uma ou duas pessoas, ela é considerada vazia, é necessário ter um mínimo de três pessoas para servir as filas LT e RT.

Como a cadeira tem quatro lugares, a quarta posição será ocupada por um esquiador das filas LS ou RS alternadamente. Novamente, se uma fila estiver vazia, a outra fila é servida continuamente.

Se as filas LT e RT estiverem vazias é permitido atender as filas LS e RS até preencher todos as quatro posições.

Caso as filas LS e RS estejam vazias é permitido que a cadeira viaje com apenas três pessoas sentadas.
