from RPG.dado.rolar_dado_notacao import rolar_dado_notacao
import re


def verifica_resultado_fora_alcance(valor_rolado, indice_menor, indice_maior, tabela, resultado):
    """
    Caso o rolamento seja fora do alcance pega o menor valor se estiver abaixo e o maior valor se estiver acima

    :param valor_rolado:
    :param indice_menor:
    :param indice_maior:
    :param tabela:
    :param resultado:
    :return:
    """
    if not resultado and (valor_rolado < indice_menor or valor_rolado > indice_maior):
        indice = 0 if valor_rolado < indice_menor else -1
        return tabela[indice][1]
    return resultado


def rola_dados_resultado(rolar_dados: bool, resultado: str) -> str:
    """
    Transforma o texto que contenha notação de _dados em texto com resultado
    :param rolar_dados:
    :param resultado:
    :return:
    """
    if rolar_dados and type(resultado) == str:
        palavras = resultado.split()
        texto_regex = []

        for palavra in palavras:
            if re.match(r'\d*d\d+(?:[-+*/]\d+)?', palavra):
                rolado = rolar_dado_notacao(palavra)
                texto_regex.append(str(rolado))
            else:
                texto_regex.append(palavra)

        resultado = ' '.join(texto_regex)

    return resultado
