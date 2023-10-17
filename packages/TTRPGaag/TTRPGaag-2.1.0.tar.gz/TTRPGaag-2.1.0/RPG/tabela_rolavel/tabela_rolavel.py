from .rolar_tabela import rolar_tabela
from .helpers.ajeita_tabela import ajeita_tabela
from .helpers.busca_index_item_tabela import busca_index_item_tabela
from .helpers.rolamento_dado import DadoRolado
from RPG.dado import rolar_dado_notacao


class TabelaRolavel:
    def __init__(self, tabela: list = None, dados: str | int = None):
        """
        Cria um objeto com uma tabela vazia ou já existente para ser rolada e métodos para que busquem o
        resultado diretamente nela.

        :param tabela: a tabela a ser buscada, se não passar o parâmetro, cria uma tabela vazia (que deve ser preenchida com .insere_linha_tabela()
        :param dados: a notação de dados a ser usado para rolar na tabela. Também pode ser passado um valor fixo (que pode ser alterado com o método .rolar())
        """
        self._tabela = ajeita_tabela(tabela) if tabela else []
        self._dados = dados
        self._dado_rolado = DadoRolado(rolamento=0, modificador=0)
        self._resultado = ''

        if dados:
            self.rolar()

    def __repr__(self):
        return f'<Tabela Rolável={self._tabela},\n dado usado: {self._dados}>'

    def __str__(self):
        return f'Rolamento de {self._dados} + mod ({self.rolamento.modificador}): {self.rolamento.total}. Resultado: {self._resultado}'

    # Métodos de edição da _tabela ====================================================================================
    def insere_linha_tabela(self, valor_menor: int, valor_maior: int, resultado) -> None:
        self._tabela.append([(valor_menor, valor_maior), resultado])

    def edita_alcance_da_linha(self, valor_da_busca: int, novo_minimo: int, novo_maximo: int) -> None:
        """
        Altera o alcance de uma linha da _tabela.

        :param valor_da_busca: Um valor que esteja entre o alcance da _tabela anterior
        (exemplo, se quiser alterar (1,10) para (1, 15) o valor_da_busca pode ser qualquer número entre 1 e 10
        :param novo_minimo: O novo valor mínimo
        :param novo_maximo: O novo valor máximo
        """
        nova_tupla = (novo_minimo, novo_maximo)
        index = busca_index_item_tabela(self._tabela, valor_da_busca)

        self._tabela[index][0] = nova_tupla

    def edita_resultado_da_linha(self, valor_da_busca: int, novo_resultado) -> None:
        """
        Altera o resultado que pode ser obtido naquela linha. Exemplo: [(1, 10), **"resultado 1"**] pode virar [(1,
        10), **"tesouro 1"**]

        :param valor_da_busca: Um valor que esteja entre o alcance da _tabela anterior (exemplo,
        se quiser alterar (1,10) para (1, 15) o valor_da_busca pode ser qualquer número entre 1 e 10
        :param novo_resultado: O texto a ser substituído
        """
        index = busca_index_item_tabela(self._tabela, valor_da_busca)
        self._tabela[index][1] = novo_resultado

    # Métodos de resultado da rolagem ================================================================================
    def rolar(self, valor_fixo: int = None, modificador_dado: int = 0, coluna: str = None) -> None:
        """
        Rola novamente a tabela e altera o resultado. Tem a opção de incluir a coluna escolhida e com isso rolar
        eventuais dados do texto (exemplo: "3d6 moedas"). Se preferir o resultado puro de texto, não passe a coluna
        como parâmetro, mas use objeto.resultado["coluna"] no lugar
        :param valor_fixo: Procura por um valor específico dentro da tabela. Se omitido vai pegar o valor passado na atribuição da classe em "dados"
        :param modificador_dado: Para o caso de haver algum modificador não básico aplicado na tabela (ex.: role na tabela X com +10)
        :param coluna: Caso o resultado tenha mais de uma coluna. Seleciona a coluna e rola dos dados dentro dela
        """
        valor_fixo = self._dados if not valor_fixo else valor_fixo
        dado = valor_fixo if type(valor_fixo) == int else rolar_dado_notacao(valor_fixo)

        self._dado_rolado = DadoRolado(dado, modificador_dado)
        self._resultado = rolar_tabela(self._dado_rolado.total, self._tabela, coluna)

    # Getters ========================================================================================================
    @property
    def tabela(self):
        return self._tabela

    @property
    def rolamento(self):
        return self._dado_rolado

    @property
    def resultado(self):
        return self._resultado
