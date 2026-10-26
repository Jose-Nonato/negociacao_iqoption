from iqoptionapi_master.iqoptionapi.stable_api import IQ_Option
from datetime import datetime


class Corretora:
    def __init__(self, email: str, password: str, entrada: float, martigale: int, stop_win: float, stop_loss: float):
        self.email = email
        self.password = password
        self.api = IQ_Option(self.email, self.password)
        self.conectado = False
        self.entrada = entrada
        self.martigale = martigale
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.lucro = 0.0


    def conectar(self):
        status, error = self.api.connect()
        if status:
            self.conectado = True
            return self.conectado
        else:
            print(f">> Erro ao conectar com a corretora. {error}")
            return self.conectado


    def selecionar_conta(self, conta: int):
        tipo_conta = "REAL" if conta == 1 else "PRACTICE" if conta == 2 else None
        self.api.change_balance(tipo_conta)
        return self.api.get_balance()


    def velas(self, ativo: str, quantidade: int = 1000, timeframe: int = 60):
        velas = self.api.get_candles(ativo, timeframe, quantidade, int(datetime.now().timestamp))
        if not velas:
            return None
        velas.sort(key = lambda c: c["from"])
        return velas


    def operacao(self, ativo: str, direcao: str, timeframe: int = 1):
        valor_entrada = self.entrada
        for gale in range(self.martigale):
            check, order_id = self.api.buy(valor_entrada, ativo, direcao, timeframe)
            print(check, order_id)
            if check:
                print(f">> Ordem aberta - Gale {gale + 1}")
                while True:
                    print(f"Aguardando resposta - {datetime.now().strftime('%H:%M:%S')}")
                    status, resultado = self.api.check_win_v3(order_id)
                    print(status, resultado)
                    if status:
                        lucro = round(resultado, 2)
                        if resultado > 0:
                            print(f">> Resultado: WIN no ativo {ativo}\n>> Lucro: R$ {lucro}\n")
                            self.lucro += lucro
                            return resultado
                        elif resultado < 0:
                            print(f'>> Resultado: LOSS no ativo {asset}\n>> Prejuízo: R$ {lucro}\n')
                            entrada *= 2
                            self.lucro += lucro
                            break
                        else:
                            print(f">> Resultado: EMPATE no ativo {asset}\n>> Lucro: R$ {lucro}\n")
                            return resultado
            else:
                print(f">> Falha ao abrir ordem - Gale {gale + 1}")
        print(">> Todas as tentativas de entrada falharam ou resultaram em loss ...")
        return -entrada
