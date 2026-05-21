import logging
import os

_PASTA   = os.path.dirname(os.path.abspath(__file__))
_LOG     = os.path.join(_PASTA, "app.log")

def obter_logger(nome: str) -> logging.Logger:
    """
    Devolve um logger configurado com o nome do módulo.
    Formato: data hora | nome_modulo | funcao | mensagem
    Escreve para app.log e também para a consola (WARNING+).
    """
    logger = logging.getLogger(nome)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(funcName)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler ficheiro — regista tudo (DEBUG+)
    fh = logging.FileHandler(_LOG, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # Handler consola — só WARNING+
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
