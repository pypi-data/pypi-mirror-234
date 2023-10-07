from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from .divs import Divs
from typing import List
import os
from time import sleep


class ApostaAutomaticaDouble:
    def __init__(
            self,
            user: str,
            senha: str,
            headless: bool = False,
            full_scream: bool = False,
            save_section: bool = False,
    ) -> None:
        self.senha = senha
        self.user = user
        self.url = "https://blaze-1.com/pt/games/double?modal=auth&tab=login"
        path = os.getcwd()
        options = Options()
        service = Service(ChromeDriverManager().install())
        if headless:
            options.add_argument("--headless=new")
        if full_scream:
            options.add_argument("--start-maximized")
        if save_section:
            options.add_argument(
                r"user-data-dir=" + path + "profile/Aviator"
            )
        self.chrome = Chrome(options=options, service=service)
        self.chrome.get(self.url)
        self.entrar()

        # --Elementos da pagina double-- #
        self._btn_cores = self.espera_elementos(
            self.chrome, Divs.BTN_CORES, 30
        )
        self._cpo_valor = self.espera_elemento(
            self.chrome, Divs.IPT_VALOR, 30
        )
        self._valor_banca = self.espera_elemento(
            self.chrome, Divs.BANK, 30
        )
        self._apostar = self.espera_elemento(
            self.chrome, Divs.BTN_APOSTA, 30
        )
        self._profile = self.espera_elementos(
            self.chrome, Divs.PROFILE, 30
        )

    @property
    def time_rodadas(self) -> str | None:
        self._time_rodadas = self.espera_elemento(
            self.chrome, Divs.BAR_TIME, 30
        )
        return self._time_rodadas.text

    @property
    def valor_banca(self) -> float:

        """
        Propiedade da classe responsável por raspar o valor
        da conta de usuario!
        """

        try:
            return float(self._valor_banca.text.replace(
                ",",
                "."
            ).replace(
                "R$",
                ""
            ))
        except Exception:
            assert 0, "Valor não foi raspado erro ao tentar!"

    def nivel_conta(self):
        ...

    def espera_elemento(
            self,
            driver: WebDriver,
            selector: str,
            time: int
    ) -> WebElement:

        """
        Função responsável por esperar o elemento aparecer na tela
        sem gerar erro para o sistema!
        """

        for _ in range(time):
            try:
                return driver.find_element(Divs.CSS, selector)
            except Exception:
                sleep(1)
                continue
        assert 0, "Erro ao tentar selecionar o elemento na pagina"

    def espera_elementos(
            self,
            driver: WebDriver,
            selector: str,
            time: int
    ) -> List[WebElement]:

        """
        Função responsável por esperar o elemento aparecer na tela
        sem gerar erro para o sistema!
        """

        for _ in range(time):
            try:
                return driver.find_elements(Divs.CSS, selector)
            except Exception:
                sleep(1)
                continue
        assert 0, "Erro ao tentar selecionar o elemento na pagina"

    def entrar(self) -> None:
        """
        Função responsável por logar cada elemento selecionado em sequencia
        para que possa iserir o user a senha e clicar no botão de login!
        """
        try:
            self.chrome.find_element(
                "name", "username"
            ).send_keys(self.user)
            sleep(1)
            self.chrome.find_element(
                "name", "password"
            ).send_keys(self.senha)
            sleep(1)
            self.chrome.find_element(Divs.CSS, "button.submit").click()
            sleep(5)
            return
        except Exception:
            assert 0, "Erro ao logar na Blaze por favor reinicie o BOT!"

    def selecionar_botao_cor(self, cor: str) -> None:
        """
        Função responsável por selecionar o botão das cores
        Parâmetro cor: str = '🔴' ou '⚪️' ou '⚫️'

        ex: self.selecionar_botao_cor('🔴') :: seleciona a cor vermelha!
        """
        if cor == "🔴":
            self._btn_cores[0].click()
            return
        if cor == "⚪️":
            self._btn_cores[2].click()
            return
        if cor == "⚫️":
            self._btn_cores[4].click()
            return
        assert 0, "Cor selecionada errada por favor selecionar a cor correta!"

    def inserir_quantia(self, quantia: str) -> None:
        """
        Função responsável por inserir a quantia da aposta no campo
        primeiro ela apaga o campo apos apagar digita o valor!

        Parâmetro quantia = int ou float :
        exemplo1 float: self.inserir_quantia(quantia=0.10)
        exemplo2 int: self.inserir_quantia(10)
        """

        try:
            self._cpo_valor.send_keys(Keys.BACK_SPACE)
        except Exception:
            assert 0, "Erro ao apagar valor!"

        try:
            self._cpo_valor.send_keys(quantia)
        except (Exception, ValueError):
            assert 0, "Erro ao digitar o valor no campo!"

    def clicar_btn_aposta(self) -> None:

        """
        Função responsável por apostar realiza o click
        no botão apstar.
        """

        try:
            self._apostar.click()
        except Exception:
            return

    def realizar_aposta(self, stake: str, _cor: str) -> None:

        """
        Principal função do bot realiza as apostas de acordo com sua
        escolha por favor num mexer nessa função.

        Parânetro:: stake: str exemplo:(stake='0,50')
        Parânetro:: stake: str exemplo:(cor='red')

        Retorna Booleano: sucesso retorna True | erro retorna False;
        """

        try:
            banca = float(self._valor_banca.text.replace(
                "R$",
                ""
            ).replace(
                ",",
                "."
            ))

            self.selecionar_botao_cor(cor=_cor)
            sleep(1.5)

            self.inserir_quantia(quantia=stake)
            sleep(1.5)

            self.clicar_btn_aposta()

            nova_banca = float(self._valor_banca.text.replace(
                "R$",
                ""
            ).replace(
                ",", "."
            ))

            if banca > nova_banca:
                print(f"Valor em banca: R${nova_banca}")
                print(f"Valor Aposta: R${stake} ")
                print(f"Cor Aposta: {_cor} ")
                return
            print("Falha ao apostar! (Revise seu saldo ou reinicie o bot!)")
            return
        except Exception:
            return

    def clicar_em_profile(self) -> None:
        try:
            self._profile[1].click()
        except Exception:
            print("Erro ao abrir menu")
        return

    def clicar_saque(self) -> None:
        try:
            sacar = self.chrome.find_elements(
                Divs.CSS, Divs.LISTA_PROFILE
            )
            sacar[2].click()
            sleep(5)
        except Exception:
            print("Erro na hora de clicar em saque")
        return

    def selecionar_metodo_de_saque(self) -> None:
        try:
            menu_dropdow = self.chrome.find_elements(
                Divs.CSS, Divs.PAYMENT_METHOD
            )
            menu_dropdow[0].click()
            sleep(5)
        except Exception:
            print("Erro na hora de selecionar metodos de pagamento")
        return

    def inserir_valor_de_saque(self, valor_saque: str) -> None:
        try:
            input_sacar = self.chrome.find_element(
                "name", Divs.CMP_VALOR_SAQUE
            )
            input_sacar.send_keys(valor_saque)
        except Exception:
            print("Erro na hora de inserir valor de saque")
        return

    def clicar_no_btn_de_saque(self) -> str:
        try:
            btn = self.chrome.find_element(Divs.CSS, Divs.BTN_SACAR)
            btn.click()
            sleep(5)
            print("Saque realizado com sucesso!")
        except Exception:
            print("Erro na hora de clicar em sacar")
        return

    def sacar_e_sair(self, valor: str) -> None:
        self.clicar_em_profile()
        self.clicar_saque()
        self.selecionar_metodo_de_saque()
        self.inserir_valor_de_saque(valor_saque=valor)
        self.clicar_no_btn_de_saque()
        self.chrome.close()
        print("Apostas finalizadas com sucesso!")
        return


if __name__ == "__main__":
    robo = ApostaAutomaticaDouble("ramonma31@gmail.com", "Manu.0512")
