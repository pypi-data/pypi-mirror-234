def salvar_palavra(palavras):
    with open('base_palavras.txt', 'a') as arquivo:
        for palavra in palavras:
            arquivo.write(palavra + '\n')

def ler_palavras():
    with open('base_palavras.txt', 'r') as arquivo:
        palavras = arquivo.read().splitlines()
    return palavras