from corretora import Corretora


def main():
    email = ""
    senha = ""
    corretora = Corretora(email, senha, 2.0, 3, 20.0, 10.0)

    status = corretora.conectar()
    if status:
        print(">> Conectado com sucesso!")

    valor_conta = corretora.selecionar_conta(2)
    print(f">> Valor em conta selecionada: R$ {valor_conta}")

    resultado = corretora.operacao("EURUSD-OTC", "put")
    print(resultado)


if __name__ == "__main__":
    main()
