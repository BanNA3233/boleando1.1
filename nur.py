import random
import string

def gerar_string_aleatoria(tamanho):
    caracteres = string.ascii_letters
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

tamanho_da_string = 6
