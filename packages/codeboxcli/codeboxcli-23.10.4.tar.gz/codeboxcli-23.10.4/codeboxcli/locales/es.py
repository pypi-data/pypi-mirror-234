# -*- coding: utf-8 -*-
help_default = """
    Uso: codebox COMANDO [ARGS]

    Comandos:
      add       Agregar un elemento.
      list      Listar elementos.
      delete    Eliminar un elemento.
      edit      Editar un elemento.
      share     Compartir un elemento.
"""

help_add = """
    Uso: codebox add [ARGS]
    
    Argumentos:
      --help                 Mostrar este mensaje de ayuda y salir.
      --name TEXTO            Especificar un nombre para el fragmento. (Requerido)
      --description TEXTO     Especificar el contenido para el fragmento.
      --tags TEXTO            Agregar etiquetas para categorizar este fragmento. Separa varias etiquetas con espacios.
    """

help_delete = """
    Uso: codebox delete [ARGS] ID_DEL_FRAGMENTO, ...
    
    Argumentos:
      --help          Mostrar este mensaje de ayuda y salir.
    """

help_edit = """
    Uso: codebox edit [ARGS] ID_DEL_FRAGMENTO
    
    Argumentos:
      --help          Mostrar este mensaje de ayuda y salir.
    """


help_share = """
    Uso: codebox share ID_DEL_FRAGMENTO [ARGS]
    
    Argumentos:
      --help          Mostrar este mensaje de ayuda y salir.
      --expire-date   Especificar la fecha de vencimiento.
      --dev-key       Especificar la clave de desarrollador.
      --share-file    Especificar el archivo a compartir.
    """


error_invalid_subcommand = """
    Error: Subcomando inválido.
    """


error_missing_value = """
    Error: Falta el valor después de {value}.
    """


error_missing_argument = """
    Error: Falta el argumento {value}.
    """


error_unknown_argument = """
    Error: Argumento desconocido {value}.
    """


error_saving = """
    Error: Fragmento no guardado.
    """


error_not_found = """
    Error: Fragmento con ID {value} no encontrado.
    """


share_url = """
    El fragmento se ha compartido exitosamente.
    {value}.
    """


share_error = """
    Error: No se pudo compartir el fragmento.
           {value}.
    """
