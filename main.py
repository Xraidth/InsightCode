import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

text = """
def destroy_universe():
    print("Iniciando secuencia de destrucción del universo...")
    print("⚠️ ADVERTENCIA: Esta acción es irreversible ⚠️")
    print("Eliminando la realidad...")
    for i in range(5, 0, -1):
        print(f"{i}...")
    print("💥 ¡BOOM! 💥 El universo ha sido destruido. Gracias por usar Python.")
    print("P.D.: Por supuesto, el universo sigue intacto. 😅")

destroy_universe()
"""

def Segmentacion(text):
    sentences = text.strip().splitlines()
    return sentences

def detect_ai_comments(code_line):
    ai_indicators = ["generated by", "automatically created", "AI generated", "machine generated"]
    return any(indicator in code_line.lower() for indicator in ai_indicators)

def detect_common_patterns(code_line):
    common_patterns = [
        r'\bfor\s+\w+\s+in\s+range\(', # Patrón de bucles for con range
        r'\bprint\(', # Uso común de print para depuración
        r'\bwhile\s+True:', # Bucle while infinito
    ]
    return any(re.search(pattern, code_line) for pattern in common_patterns)

def detect_redundant_code(code_line):
    redundant_patterns = [
        r'\breturn\s+None\s*\n', # Retornos innecesarios
        r'\bif\s+True:', # Condiciones siempre verdaderas
    ]
    return any(re.search(pattern, code_line) for pattern in redundant_patterns)

def detect_unusual_structures(code_line):
    unusual_structures = [
        r'\b(?:list|dict|set|tuple)\(\s*\)\s*=\s*\[\]',  # Inicialización inusual de colecciones vacías
        r'\b(?:try|except)\s+.*:',  # Uso de bloques try-except en contextos inusuales
    ]
    return any(re.search(pattern, code_line) for pattern in unusual_structures)

def predict_ai_code(line):
    lines = [
        "for i in range(10):",
        "This code was automatically created by the AI.",
        "def my_function(x): return x + 1",
        "while True: pass",
    ]
    labels = [0, 1, 0, 1]  # 0: Humano, 1: IA

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(lines)
    model = MultinomialNB()
    model.fit(X, labels)

    X_test = vectorizer.transform([line])
    return model.predict(X_test)[0]

# Ejecutar el análisis
os.system('cls')  # O 'clear' si estás en un sistema basado en Unix


oraciones = Segmentacion(text)
cant_lineas = len(oraciones)
"""
for line in oraciones:
    print("Line:", line)
    print("AI Comments Detected:", detect_ai_comments(line))
    print("Common Patterns Detected:", detect_common_patterns(line))
    print("Redundant Code Detected:", detect_redundant_code(line))
    print("Unusual Structures Detected:", detect_unusual_structures(line))
    print("Predicted AI Code:", predict_ai_code(line))
    print()
"""

puntos = 7

print(puntos*100 / cant_lineas,"%","de codigo generado por Ai")