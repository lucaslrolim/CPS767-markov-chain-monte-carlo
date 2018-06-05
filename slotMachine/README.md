# Descrição trabalho MCMC


## Projeto da disciplina Monte Carlo Markov Chain - CPS767
## Problema a ser estudado

Iremos estudar, de maneira geral, como funciona uma máquina de apostas em um cassino. Simularemos usando o método de Monte Carlo o funcionamento dessa máquina e a relação entre ganho e perda, tanto do cassino como dos jogadores.

Nossa máquina a ser simulada segue o modelo tradicional de um caça-níquel, onde ao puxar uma alavanca um determinado arranjo de figuras dentre um conjunto S de figuras possível será sorteado aleatoriamente.  Cada uma de desses arranjos terá um valor de recompensa definido por uma dada função R(w), a qual a máquina será programada.  Além disso, cada jogador possui montantes diferentes para apostar e também podem realizar apostas diferentes na máquina a ser simulada.

Pretendemos estudar principalmente como o dono do cassino define qual será a probabilidade de os jogares ganharem cada um dos prêmios e também como um jogador com bons conhecimentos em estatística pode tirar proveito desses conhecimentos e, sem acesso a função re recompensa da máquina, estimar o valor médio de sua aposta.

## Objetivos
1. Simular uma máquina na qual podemos estabelecer um retorno estimado qualquer para o dono do cassino *(Edge House)* ;
2. Estimar o retorno que o cassino tem com uma máquina através de amostras de jogadas;
3. Estudar o número de jogadas esperado para que um jogador perca tudo ao apostar em uma dada máquina;
4. Estimar o valor médio de uma aposta em uma dada máquina


## Simulando uma máquina caça-níquel

Em uma máquina caça-níquel, e em jogos de aposta em geral, o dono do cassino obtém seu lucro de forma probabilística, com um valor esperado que converge para o definido pelo dono do cassino conforme um grande número de jogadores fazem apostas, tal como previsto pela Lei dos Grandes Números.

O valor esperado de lucro possui como suas duas variáveis principais a função de recompensa definida e o quão ¨viciada¨ a máquina é. Podemos definir esse valor esperado de lucro para o cassino pela seguinte função:

$$E(X) = P(cassino Ganha) * aposta + P(cassino Perde) * recompensa$$

No caso de uma máquina completamente honesta, o valor esperado de lucro para o cassino seria zero. Podemos visualizar isso de maneira clara ao imaginar um simples lançar de moeda, onde a recompensa para o jogador seria o dobro de sua aposta. Vejamos o exemplo que o jogador aposta R$1,00.

$$0.5 * (+1) + 0.5 * (-1) = 0$$

Mas o que acontece na verdade é que o dono do cassino estabelece uma pequena vantagem nesse valor esperado, de modo a viciar a moeda. Podemos ver abaixo que ao estabelecer uma recompensa de R$1,90 no exemplo anterior o dono do cassino teria um lucro esperado de 5% sobre a aposta de todos os jogadores.

$$E(X) = 0.5 * (+1) + 0.5 * (-0.9) = 0.05$$

No caso da nossa máquina a ser simulada teremos como parâmetros o número de figuras da máquina *(valores possíveis)*, o número de slots, o percentual de lucro que desejamos obter com nossa máquina e também nossa função de recompensa.  Com base nesses parâmetros iremos definir a probabilidade de um jogador vencer ou não em nossa máquina, independente do valor a ser apostado.

**Função de recompensa**

A função de recompensa padrão que escolhemos para nossa máquina oferece n prêmios diferentes, onde n é o número de figuras possíveis na máquina. Cada uma das figuras possui um valor de 1 a n atribuído a si e cada vez que todos os slots caem na mesma figura o jogador recebe o valor de sua aposta multiplicado pelo valor atribuído a figura.

Por exemplo, ao apostar R$1,00 em uma máquina como 3 figuras diferentes possíveis o jogador pode receber o valor da sua aposta *( caso [1,1,1])*, o valor de sua aposta dobrado *(caso [2,2,2])* ou o valor de sua aposta triplicado *(caso [3,3,3])*. Esses prêmios estão distribuídos de forma que, dado que o usuário ganhou a aposta, ele tem a seguinte probabilidade de ganhar o prêmio de valor n:


    def setProbabilities(self):
        self.prizeStatesProb = []
        prob = 1 / (self.figures * (1+self.figures)/2)
        index = 1
        for figure in reversed(self.states):
            self.prizeStatesProb.append(figure * prob) 
            index += 1

Ou seja, a **probabilidade de ganhar o prêmio n será inversamente proporcional a n**.  Como mostrar os resultados do jogo não é necessariamente um requisito de nossa simulação, iremos primeiro definir aleatoriamente se um usuário ganhou ou não a aposta e depois faremos uma outra decisão aleatória sobre o seu prêmio. Dessa forma ganhamos em eficiência computacional, pois essa implementação é mais eficiente permutar aleatoriamente um vetor de tamanho s **(número de slots)* e extremamente mais eficiente que gerar todas as s! permutações possíveis e escolher uma delas.

Em nosso exemplo, um usuário que ganhasse uma aposta tem chance de ser recompensando da seguinte forma:

$$R(1) = 0,5 ; R(2) = 0,33 ; R(3) = 0,17$$

**Definindo ¨vício¨ da máquina**

Um dos argumentos da nossa classe é o **house edge**, ou seja, o percentual de lucro que o dono do cassino deseja obter do valor apostado por seus jogadores. Dado que já definimos nossa função de recompensa,  podemos definir nossa probabilidade de vitória por parte do cassino como sendo:

$$P = (houseEdge - premioMedio)/(valorApostado-premioMedio)$$

Nesse caso definiremos o valor esperado da nossa função de recompensa como nosso prêmio médio.

**Apostando na máquina**

A cada aposta realizada na máquina seguimos o seguinte algoritmo:


    u = random.uniform(0, 1)
    if(u < self.probabilityToWin):
        self.jackpot += self.bid
        return -self.bid
    else:
        figure = self.states[alias_draw(self.j,self.q)]
        self.jackpot -= self.prize[figure]
        self.prizesConceived.append(self.prize[figure])
        return self.prize[figure]

Ou seja, geramos primeiro uma uniforme para saber se nessa jogada o usuário deve ganhar uma recompensa ou não. Caso o usuário perca o valor para o jogador dessa aposta será a subtração do valor que ele apostou. Caso o jogador vença a aposta,  usamos o **Alias Method** para definir qual dos prêmios ele irá ganhar.

**Avaliando a qualidade das soluções encontradas**

Para avaliar a qualidade da soluções encontradas iremos recorrer ao cálculo da variância, do valor esperado amostral e análises gráficas.

Para o cálculo da variância usaremos as seguintes relações:

$$M_1 = \sum\limits_{i=1}^n T_i; M_2 = \sum\limits_{i=1}^n (T_i)^2$$  

$$S^2_{T,n} = \frac{M2 - \frac{M^2_1}{n}}{n-1}$$

Onde S representa o estimador da variância amostral sem viés.

## Resultados

**Estimador do House Edge**

Ao simular 10 mil jogadores, com valor inicial para apostar de R$10,00 e realizando 10 apostas cada, obtemos o resultado: 


![Valor médio de cada aposta para um jogador](https://lh6.googleusercontent.com/ASVa6OOofdJVE23Z-LqDmTS6a8JwqBmACk0OH91Fh6be36JEkPwgJxfBqqMoRwAEq1o8YilH1NmGPoTDYRBwxjBdOCtTJ3ptSaXvS3LA32yIXo_jYLI3s2cek24lbEoPYWONVS_Ozow)


Nessa simulação o valor que estamos tentando aproximar de forma amostral é o house edge da máquina em que os jogadores estão jogando, a qual configuramos para ser de 0.1. De forma amostral obtivemos uma média de retorno de -0.1000608 para o jogador em cada aposta. Como o retorno para o jogador é igual - (house edge), nosso estimador conta com menos de 10^3 de erro. A variância nesse caso convergir para 0.02.

Ao aumentar o número de apostas realizado por cada jogador para 40 obtemos que o lucro estimado para o cassino aumenta para aproximadamente 35%, mesmo sem alterarmos nosso House Edge. Isso acontece porque podemos imaginar que estávamos apostando cada real apenas uma vez, agora estamos ¨apostando cada real 4 vezes¨. Isso dá para um jogador um valor esperado de n * (0,9)^4 , onde n é o valor inicial da aposta.


![Retorno do cassino no caso em que o jogador jogador aposta 4 vezes mais do que possui como valor inicial](https://d2mxuefqeaa7sj.cloudfront.net/s_DEEFBB2368C2E9318EA20CD4F47A9A8E9B58A123E593C81D75FCAB6018A6E139_1528164860021_jackpots_4_g4.png)


**Estimador do prêmio médio**

Com um número reduzido de amostras conseguimos estabelecer uma boa estimativa para nosso prêmio médio.  Observou-se que simulando 300 jogadores apostando 10 vezes cada já é possível estabelecer com uma margem de erro de menos de 1% para o prêmio médio de uma máquina com 7 figuras possíveis e 4 slots (7^n estados possíveis), considerando todos os estados e figuras possíveis.

![Prêmio médio vs número de jogadores (apostando 10 vezes cada)](https://d2mxuefqeaa7sj.cloudfront.net/s_DEEFBB2368C2E9318EA20CD4F47A9A8E9B58A123E593C81D75FCAB6018A6E139_1528165606540_meanMeanPrize.png)


**Número de jogadas até um jogador zerar**

Simulamos um milhão de jogadores, cada um com R$5,00 iniciais e jogando em uma máquina com 0.1 de house edge até perderem tudo. O valor esperado para que esses jogadores perdessem tudo convergiu para 50 jogadas, o que era o valor teórico esperado dado que cada aposta realizada é de R$1,00 e a casa possui vantagem de 10% sobre o jogador. A variância nesse caso convergiu para 0.02.
  

![Número de jogadas estimado para perder tudo (iniciando em R$5,00)](https://d2mxuefqeaa7sj.cloudfront.net/s_DEEFBB2368C2E9318EA20CD4F47A9A8E9B58A123E593C81D75FCAB6018A6E139_1528167489042_meanUntilZero_x.png)


Por fim, podemos observar também a distribuição de quanto cada jogador possui em sua carteira após iniciar com R$5,00. Simulamos esses resultados para após 5, 10 e 50 jogadas.


![Após 5 jogadas](https://lh3.googleusercontent.com/BjfCeMqTYUNe89aU4EixS_IE4UTw6XkJePZ_YLQjqorp1crfnPDU_U7sUjhVYfvRBjNINzBF0GMd9_mDV4V9rQ-2DPIpZikHXg8Hdl9bZLGHt2H0EfjfSVFQut-hEByNFhs3m56t3Zk)



![Após 10 jogadas](https://lh6.googleusercontent.com/NtGe38UytAqhpxPg8v42ZzyaLmT9LmUZEhKJSVxqkx5YdNFxLtqS_pJA729qcKcNXhNNOmFLWJpTbQ7koFZk1G-AJPKqFYb4veBssuOeTfNtfoJz26tHMdNJL5JCU8qHuVpnAgdbNAE)

![Após 50 jogadas](https://lh5.googleusercontent.com/ynjjKRQ7z-Gdd78E-AGjaDpAUhzWskEVcTki2ff27BroajG2fCZ2FTcDUIUrgntoPG3PfvSvbRfQrmTa1tZFnyerQhHA1K0LGkmr8tSJNBrUUz3QAZOfhZMUF5yGawP-nHly6TvuJvE)



