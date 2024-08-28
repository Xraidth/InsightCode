import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

text = """
def destroy_universe(): # Aqui hay algo
    print("Iniciando secuencia de destrucción del universo...") # Aqui hay algo
    print("⚠️ ADVERTENCIA: Esta acción es irreversible ⚠️") # Aqui hay algo
    print("Eliminando la realidad...")# Aqui hay algo
    for i in range(5, 0, -1):
        print(f"{i}...") 
    
    print("💥 ¡BOOM! 💥 El universo ha sido destruido. Gracias por usar Python.")  
    print("P.D.: Por supuesto, el universo sigue intacto. 😅") 

destroy_universe() 
"""

def Segmentacion(text):
    sentences = text.strip().splitlines()
    return sentences


def test_comentarios(oraciones):
    porcentaje = round(sum(1 for o in oraciones if "#" in o.split()) / len(oraciones), 2)
    return porcentaje >= 0.5




os.system('cls')  
oraciones = Segmentacion(text)


print(test_comentarios(oraciones))

