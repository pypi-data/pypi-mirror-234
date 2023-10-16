

import locale


__DEFAULT_LANG__ = "en"

texts = \
    dict(
        en = dict(
            wrong_sol = "Wrong type for solutions argument",
            correct = "correct",
            error = "ERROR",
            points = "points",
            total_points = "Total points",
            wrong_var = "is a variable with a wrong value",
            wrong_func = "return a wrong value for inputs"
        ),
        es = dict(
            wrong_sol="Tipo incorrecto del fichero de soluciones",
            correct="correcto",
            error="ERROR",
            points="puntos",
            total_points="Puntos totales",
            wrong_var="es una variable con valor incorrecto",
            wrong_func = "devuelve un valor incorrecto para la entrada"
        )
)

def gettext(label):
    try:
        lang = locale.getlocale()[0].split("_")[0]
        return texts[lang][label]
    except:
        return texts[__DEFAULT_LANG__][label]





