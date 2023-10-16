import random


class Baralho:
    def __init__(self, usa_coringa: int = 2, as_menor: bool = False, ordem: bool = None):
        """
        Essa classe cria uma pilha de cartas de baralho.

        Também tem funções para a manipulação dos deques e de saque de cartas.

        Cada carta no baralho tem uma pontuação para o caso de precisar comparar a "força"
        :param usa_coringa: int (0, 1, 2); opcional. Determina se vai usar coringa se omitido, aceita 2
        :param as_menor: Se o Ás e a maior ou menor carta, se omitido, entra False
        :param ordem: A ordem de força dos naipes. Fazer a lista na ordem de importância Padrão: ['Espada', 'Copas', 'Ouros', 'Paus'] Caso vá usar menos naipes, omita os que não interessa.
        """
        if ordem is None:
            ordem = ['Espada', 'Copas', 'Ouros', 'Paus']

        usa_coringa = max(0, min(usa_coringa, 2))  # uso de coringa é entre 0 ou 2

        self._usa_coringa = usa_coringa
        self._as_menor = as_menor
        self._ordem = ordem
        self._baralho = self.criar_baralho()

    def __str__(self):
        return f'Cartas disponíveis para saque: {self._baralho}'

    def __len__(self):
        return len(self._baralho)

    def __getitem__(self, item):
        return self._baralho[item]

    # ---------------------- INICIADORES ----------------------------
    def _criar_cartas(self, nome):
        """
        Função interna
        Retorna um baralho com os naipes, que inclui a carta, o naipe, o valor da
        carta, o símbolo do naipe, e a representação carta + naipe

        * nome: O nome do naipe
        """

        naipes = {
            'Espada': '♠️',
            'Copas': '♥️',
            'Ouros': '♦️',
            'Paus': '♣️'
        }
        basicas = [
            {'valor': 1, 'nome': 'A'},
            {'valor': 2, 'nome': '2'},
            {'valor': 3, 'nome': '3'},
            {'valor': 4, 'nome': '4'},
            {'valor': 5, 'nome': '5'},
            {'valor': 6, 'nome': '6'},
            {'valor': 7, 'nome': '7'},
            {'valor': 8, 'nome': '8'},
            {'valor': 9, 'nome': '9'},
            {'valor': 10, 'nome': '10'},
            {'valor': 11, 'nome': 'J'},
            {'valor': 12, 'nome': 'Q'},
            {'valor': 13, 'nome': 'K'},
        ]

        if not self._as_menor:
            basicas[0]['valor'] *= (len(basicas) + 1)
            basicas.sort(key=lambda c: c['valor'])

        for carta in basicas:
            carta['naipe'] = nome
            carta['carta'] = carta['nome'] + ' ' + naipes[nome]

        return basicas

    def criar_baralho(self):
        """
        Retorna um baralho montado com todas as cartas.
        Pode usar para reiniciar o baralho
        """

        baralho = []

        for naipe in self._ordem:
            baralho_naipe = self._criar_cartas(naipe)
            mod_valor = self._ordem.index(naipe) * 0.1
            for item in baralho_naipe:
                item['valor'] += mod_valor
                baralho.append(item)

        i = 0
        while i < self._usa_coringa:
            baralho.append({
                'nome': 'Joker',
                'valor': 100,
                'carta': '🃏'
            })
            i += 1

        return baralho

    # -------------------- FUNÇÕES DE USUÁRIO ----------------------
    def sacar_carta(self):
        """
        Saca uma carta do baralho.

        Retorna a carta
        """
        if len(self._baralho) > 0:
            sacada = random.choice(self._baralho)
            return self._baralho.pop(self._baralho.index(sacada))
        else:
            return {'nome': 'Não tem mais o que sacar', 'valor': 0, 'carta': '0'}


if __name__ == "__main__":
    baralho_teste = Baralho()
    print(baralho_teste)
    print("Mão com 5 cartas:")
    mao_extra = [
        baralho_teste.sacar_carta()
        for _ in range(5)
    ]
    print(mao_extra)
