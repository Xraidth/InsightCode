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


def test_usoClases(oraciones):
    clases = [line.strip() for line in oraciones if line.strip().startswith("class ")]
    return len(clases) / len(oraciones) if oraciones else 0

def test_documentacionFunciones(oraciones):
    docstrings = 0
    in_function = False
    for line in oraciones:
        if line.strip().startswith("def "):
            in_function = True
        elif in_function and line.strip().startswith('"""'):
            docstrings += 1
            in_function = False
        elif in_function and line.strip() == "":
            in_function = False
    funciones = [line.strip() for line in oraciones if line.strip().startswith("def ")]
    return (docstrings / len(funciones)) if funciones else 0

def test_nombresVariablesDescriptivos(oraciones):
    variables = re.findall(r'\b\w+\s*=\s*', text)
    malos_nombres = [v.split('=')[0].strip() for v in variables if len(v.split('=')[0].strip()) < 3]
    return 1 - len(malos_nombres) / len(variables) if variables else 0
def test_usoExcepciones(oraciones):
    excepciones = sum(1 for line in oraciones if "try:" in line or "except" in line)
    return excepciones / len(oraciones) if oraciones else 0
def test_complejidadExpresiones(oraciones):
    expresiones_complejas = [line for line in oraciones if re.search(r'\+|\-|\*|\/|\%', line)]
    expresiones_muy_complejas = [expr for expr in expresiones_complejas if expr.count('+') + expr.count('-') + expr.count('*') + expr.count('/') + expr.count('%') > 3]
    return 1 - len(expresiones_muy_complejas) / len(expresiones_complejas) if expresiones_complejas else 0
def test_usoListComprehensions(oraciones):
    comprehensions = [line for line in oraciones if '[' in line and 'for' in line and ']' in line]
    return len(comprehensions) / len(oraciones) if oraciones else 0
def test_modificacionGlobales(oraciones):
    globales = [line for line in oraciones if 'global ' in line]
    return 1 - len(globales) / len(oraciones) if oraciones else 0
def test_usoFuncionesLambda(oraciones):
    lambdas = [line for line in oraciones if 'lambda ' in line]
    return len(lambdas) / len(oraciones) if oraciones else 0









import ast

def test_funcionesRecursivas(oraciones):
    """
    Verifica la presencia de funciones recursivas en el código.
    """
    def es_recursiva(func):
        return func in func_calls.get(func, [])

    func_calls = {}
    current_func = None

    for line in oraciones:
        if line.strip().startswith("def "):
            current_func = line.split()[1].split('(')[0]
            func_calls[current_func] = set()
        elif current_func and '(' in line and ')' in line:
            called_func = re.findall(r'\b\w+\b', line)
            func_calls[current_func].update(called_func)

    recursivas = sum(1 for func in func_calls if es_recursiva(func))
    return recursivas / len(func_calls) if func_calls else 0

def test_usoDecoradores(oraciones):
    """
    Calcula el porcentaje de funciones que utilizan decoradores.
    """
    decorador_pattern = re.compile(r'@\w+')
    decoradores = [line for line in oraciones if line.strip().startswith("def ") and any(decorador_pattern.search(line) for line in oraciones)]
    return len(decoradores) / len([line for line in oraciones if line.strip().startswith("def ")]) if oraciones else 0

def test_complejidadNesting(oraciones):
    """
    Evalúa la complejidad de anidamiento de bloques (if, for, while).
    """
    nesting = 0
    max_nesting = 0
    for line in oraciones:
        if any(keyword in line for keyword in ['if', 'for', 'while']):
            nesting += 1
            max_nesting = max(max_nesting, nesting)
        elif 'else' in line:
            max_nesting = max(max_nesting, nesting)
        elif line.strip() == "":
            nesting = 0
    return max_nesting / len(oraciones) if oraciones else 0

def test_usoAsync(oraciones):
    """
    Calcula el porcentaje de funciones que utilizan `async`.
    """
    async_functions = [line for line in oraciones if line.strip().startswith("async def ")]
    return len(async_functions) / len([line for line in oraciones if line.strip().startswith("def ")]) if oraciones else 0

def test_clasesHerencia(oraciones):
    """
    Evalúa la cantidad de clases que heredan de otras clases.
    """
    clases = [line.split()[1].split('(')[0] for line in oraciones if line.strip().startswith("class ")]
    herencia = [line for line in oraciones if 'class ' in line and '(' in line and ')' in line]
    return len(herencia) / len(clases) if clases else 0

def test_usoGeneradores(oraciones):
    """
    Calcula el porcentaje de generadores utilizados en el código.
    """
    generadores = [line for line in oraciones if 'yield' in line]
    return len(generadores) / len(oraciones) if oraciones else 0

def test_variablesNoUsadas(oraciones):
    """
    Calcula el porcentaje de variables declaradas que no se utilizan en el código.
    """
    vars_declaradas = re.findall(r'\b\w+\s*=\s*', text)
    vars_usadas = set(re.findall(r'\b\w+\b', text))
    vars_no_usadas = [v.split('=')[0].strip() for v in vars_declaradas if v.split('=')[0].strip() not in vars_usadas]
    return len(vars_no_usadas) / len(vars_declaradas) if vars_declaradas else 0

def test_usoTypeHints(oraciones):
    """
    Calcula el porcentaje de funciones que utilizan anotaciones de tipo.
    """
    type_hints = [line for line in oraciones if 'def ' in line and '->' in line]
    return len(type_hints) / len([line for line in oraciones if line.strip().startswith("def ")]) if oraciones else 0

def test_dependenciasExternas(oraciones):
    """
    Calcula el porcentaje de importaciones que provienen de módulos externos.
    """
    imports = re.findall(r'import (\w+)|from (\w+) import', text)
    external_imports = [i for i in set([i for sublist in imports for i in sublist if i]) if i not in ['os', 're', 'sys', 'math', 'datetime']]  # Modificar según los módulos estándar
    return len(external_imports) / len(set([i for sublist in imports for i in sublist if i])) if imports else 0





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

t9 = test_usoClases(oraciones)
t10 = test_documentacionFunciones(oraciones)
t11 = test_nombresVariablesDescriptivos(oraciones)
t12 = test_usoExcepciones(oraciones)
t13 = test_complejidadExpresiones(oraciones)
t14 = test_usoListComprehensions(oraciones)
t15 = test_modificacionGlobales(oraciones)
t16 = test_usoFuncionesLambda(oraciones)
t17 = test_funcionesRecursivas(oraciones)
t18 = test_usoDecoradores(oraciones)
t19 = test_complejidadNesting(oraciones)
t20 = test_usoAsync(oraciones)
t21 = test_clasesHerencia(oraciones)
t22 = test_usoGeneradores(oraciones)
t23 = test_variablesNoUsadas(oraciones)
t24 = test_usoTypeHints(oraciones)
t25 = test_dependenciasExternas(oraciones)

t6 = t6/10
t7 = t7/10
tt = ((t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12 + t13 + t14 +t15+t16+t17+t18+t19+t20+t21+t22+t23+t24+t25) * 100) / 25
print(f"Porcentaje de Ai Code: {tt:.2f}%")





    