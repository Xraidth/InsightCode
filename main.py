import os
import re

text = """
from PIL import Image, ImageDraw, ImageFont
def text_to_image(text, font_path='arial.ttf', font_size=50, image_size=(800, 400), text_color=(255, 255, 255), bg_color=(0, 0, 0)):    
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)
    # Calcular la posición del texto (centrado)
    x = (image_size[0] - text_width) / 2
    y = (image_size[1] - text_height) / 2
    # Dibujar el texto en la imagen
    draw.text((x, y), text, font=font, fill=text_color)
    # Guardar la imagen
    image.save('text_image.png')
    image.show()
# Uso de la función
text_to_image('¡Hola, Mundo!', font_size=70, text_color=(255, 215, 0), bg_color=(0, 0, 255))
"""

def Segmentacion(text):
    return text.strip().splitlines()

def test_comentariosCortos(oraciones):
    return round(sum('#' in o for o in oraciones) / len(oraciones), 2)

def test_comentariosLargos(oraciones):
    multiline_comment_pattern = re.compile(r'""".*?"""', re.DOTALL)
    multiline_comments = multiline_comment_pattern.findall(text)
    return len(multiline_comments) / len(oraciones) if oraciones else 0

def test_comentariosVacios(oraciones):
    return sum('' in o.strip() and '#' in o for o in oraciones) / len(oraciones) if oraciones else 0

def test_funciones(oraciones):
    funciones = [line.split()[1].split('(')[0] for line in oraciones if line.strip().startswith("def ")]
    total_funciones = len(funciones)
    if total_funciones == 0:
        return 0.00
    funciones_con_guiones = sum('_' in nf for nf in funciones)
    return round(funciones_con_guiones / total_funciones, 2)

def test_complejidadCiclomatica(oraciones):
    decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'catch', 'finally']
    complexity = sum(line.count(keyword) for line in oraciones for keyword in decision_keywords)
    return round(complexity / len(oraciones) if oraciones else 0, 2)

def test_lineasPorFuncion(oraciones):
    funciones = re.findall(r'def \w+\(.*?\):', text)
    lineas_funciones = []
    for funcion in funciones:
        start = text.index(funcion) + len(funcion)
        end = text.find('def ', start)
        if end == -1:
            end = len(text)
        lineas_funciones.append(len(text[start:end].splitlines()))
    return round(sum(lineas_funciones) / len(funciones) if funciones else 0, 2)

def test_numeroParametros(oraciones):
    funciones = re.findall(r'def \w+\((.*?)\):', text)
    num_parametros = [len(func.split(',')) for func in funciones]
    return round(sum(num_parametros) / len(funciones) if funciones else 0, 2)

def test_importaciones(oraciones):
    imports = re.findall(r'import (\w+)|from (\w+) import', text)
    return len(set([i for sublist in imports for i in sublist if i])) / len(oraciones) if oraciones else 0

os.system('cls')

oraciones = Segmentacion(text)

t1 = test_comentariosCortos(oraciones)
t2 = test_comentariosLargos(oraciones)
t3 = test_comentariosVacios(oraciones)
t4 = test_funciones(oraciones)
t5 = test_complejidadCiclomatica(oraciones)
t6 = test_lineasPorFuncion(oraciones)
t7 = test_numeroParametros(oraciones)
t8 = test_importaciones(oraciones)

t6 = t6/10
t7 = t7/10
tt = ((t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8) * 100) / 8
print(f"Porcentaje de Ai Code: {tt:.2f}%")
