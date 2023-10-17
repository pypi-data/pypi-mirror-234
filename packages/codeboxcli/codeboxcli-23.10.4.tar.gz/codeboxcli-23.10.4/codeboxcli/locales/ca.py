# -*- coding: utf-8 -*-
help_default = """
    Ús: codebox COMANDA [ARGS]

    Comandes:
      add       Afegir un element.
      list      Llistar elements.
      delete    Esborrar un element.
      edit      Editar un element.
      share     Compartir un element.
"""

help_add = """
    Ús: codebox add [ARGS]
    
    Arguments:
      --help                 Mostrar aquest missatge d'ajuda i sortir.
      --name TEXT            Especificar un nom pel fragment. (Requerit)
      --description TEXT     Especificar el contingut pel fragment.
      --tags TEXT            Afegir etiquetes per categoritzar aquest fragment. Separa diverses etiquetes amb espai.
    """

help_delete = """
    Ús: codebox delete [ARGS] ID_DEL_FRAGMENT, ...
    
    Arguments:
      --help          Mostrar aquest missatge d'ajuda i sortir.
    """

help_edit = """
    Ús: codebox edit [ARGS] ID_DEL_FRAGMENT
    
    Arguments:
      --help          Mostrar aquest missatge d'ajuda i sortir.
    """


help_share = """
    Ús: codebox share ID_DEL_FRAGMENT [ARGS]
    
    Arguments:
      --help          Mostrar aquest missatge d'ajuda i sortir.
      --expire-date   Especificar la data d'expiració.
      --dev-key       Especificar la clau de desenvolupador.
      --share-file    Especificar l'arxiu a compartir.
    """


error_invalid_subcommand = """
    Error: Subcomanda invàlida.
    """


error_missing_value = """
    Error: Falta el valor després de {value}.
    """


error_missing_argument = """
    Error: Falta l'argument {value}.
    """


error_unknown_argument = """
    Error: Argument desconegut {value}.
    """


error_saving = """
    Error: Fragment no guardat.
    """


error_not_found = """
    Error: Fragment amb ID {value} no trobat.
    """


share_url = """
    El fragment s'ha compartit amb èxit.
    {value}.
    """


share_error = """
    Error: No es pot compartir el fragment.
           {value}.
    """
