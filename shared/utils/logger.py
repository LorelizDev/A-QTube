import logging


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Evitar handlers duplicados
    if logger.handlers:
        return logger

    # Crear un handler para escribir en la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Añadir el handler al logger
    logger.addHandler(console_handler)
    return logger
