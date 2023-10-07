import random

def palavra():
    consoantes = 'bcdfghjklmnpqrstvwxyz'
    vogais = 'aeiou'
    
    sil1 = random.choice(consoantes) + random.choice(vogais)
    sil2 = random.choice(consoantes) + random.choice(vogais)
    
    return sil1 + sil2

def gerar_palavra(qtd):
    palavras = [palavra() for _ in range(qtd)]
    return palavras


