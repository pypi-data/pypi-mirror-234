import math


def map_value(x, in_min, in_max, out_min, out_max,
              raise_error=False, returned_no_error_min=None, returned_no_error_max=None):
    if x < in_min:
        if not raise_error:
            return returned_no_error_min
        raise Exception('Valor no incluido')
    if x > in_max:
        if not raise_error:
            return returned_no_error_max
        raise Exception('Valor no incluido')
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Incremental_math_operations:

    @staticmethod
    def media_incremental_adicion(media_original, longitud_original, nuevo_valor):
        return (media_original * longitud_original + nuevo_valor) / (longitud_original + 1)

    @staticmethod
    def media_incremental_substitucion(media_original, longitud_original, nuevo_valor, valor_eliminar):
        if longitud_original == 0:
            return None
        return (media_original * longitud_original + nuevo_valor - valor_eliminar) / longitud_original

    @staticmethod
    def std_incremental_adicion(std_original, longitud_original, nuevo_valor, media_original):
        return math.sqrt((longitud_original * pow(std_original, 2) + (
                nuevo_valor - Incremental_math_operations.media_incremental_adicion(media_original,
                                                                                    longitud_original, nuevo_valor))
                          * (nuevo_valor - media_original)) / (longitud_original + 1))

    @staticmethod
    def std_incremental_substitucion(std_original, longitud_original, nuevo_valor, valor_eliminar, media_original):
        if longitud_original == 0:
            return None
        m_i_s = Incremental_math_operations.media_incremental_substitucion(media_original,
                                                                           longitud_original,
                                                                           nuevo_valor, valor_eliminar)
        return math.sqrt(pow(std_original, 2) + pow((m_i_s - media_original), 2) + (
                (pow((nuevo_valor - m_i_s), 2) - pow((valor_eliminar - m_i_s), 2)) / longitud_original))


imo = Incremental_math_operations
