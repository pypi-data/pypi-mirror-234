from .helpers.ajeita_tabela import ajeita_tabela
from .helpers.ajusta_resultados import verifica_resultado_fora_alcance, rola_dados_resultado


def rolar_tabela(valor: int, tabela: list, coluna=None, rolar_dados=True) -> str:
    """
    Busca o resultado em uma tabela de RPG retornando a linha e a eventual
    coluna, caso tenha. Se o texto possuir notação de dados (exemplo: 1d6)
    também já rola o resultado.

    O padrão de cada linha é ((inicio, fim), resultado da busca).
    É possível colocar apenas um valor na primeira tupla caso esse item só tenha
    um valor. Resultado da busca pode ser uma string como "1d6 gp" ou um
    dicionário com o formato { "col 1": "resultado col 1", "col2": "valor col2" }

    :param valor: o valor a ser buscado
    :param tabela: a lista a ser usada conforme indicado acima.
    :param coluna: qual a coluna a ser buscada pelo resultado, se não tiver colunas, ignore
    :param rolar_dados: booleano para indicar se o resultado que contenha dados a ser rolado (ex.: "1d10 gp"). Se não quiser que já retorne o dado rolado,     marque False

    :return:
    """
    # Ajeita a _tabela para o caso da tupla não ter dois itens
    nova_tabela = ajeita_tabela(tabela)

    # pega os índices a serem buscados
    indice_menor = nova_tabela[0][0][0]
    indice_maior = nova_tabela[-1][0][1]

    # Busca a linha da _tabela
    resultado = next(
        (item for (x, y), item in nova_tabela if x <= valor <= y),
        None
    )

    resultado = verifica_resultado_fora_alcance(valor, indice_menor, indice_maior, nova_tabela, resultado)

    # se tiver mais de uma coluna, seleciona a coluna
    resultado = resultado[coluna] if coluna else resultado

    # transforma o texto que contenha notação de _dados em texto com resultado
    resultado = rola_dados_resultado(rolar_dados, resultado)

    return resultado


if __name__ == "__main__":
    # Exemplo de uso
    exemplo_tabela = [
        ((1, 6), {"coluna 1": "2d6 moedas de ouro", "coluna 2": "2d10+1d6 moedas de ouro e 1d6 de prata",
                  "coluna 3": "d8*2 moedas de ouro"}),
        ((7, 9), {"coluna 1": "2d6 moedas de ouro", "coluna 2": "2d10+1d6 moedas de ouro e 1d6 de prata",
                  "coluna 3": "d8*2 moedas de ouro"}),
        (10, {"coluna 1": "2d6 moedas de ouro", "coluna 2": "2d10+1d6+100 moedas de ouro e 1d6 de prata",
              "coluna 3": "d8*2 moedas de ouro"})
    ]

    print('-------------------------------------------------------------------------')
    print("Tabela:")
    print(*exemplo_tabela, sep='\n')
    print('-------------------------------------------------------------------------')
    print(f"O resultado foi: {rolar_tabela(rolar_dado_notacao('d10'), exemplo_tabela, 'coluna 2')}")
    print('-------------------------------------------------------------------------')