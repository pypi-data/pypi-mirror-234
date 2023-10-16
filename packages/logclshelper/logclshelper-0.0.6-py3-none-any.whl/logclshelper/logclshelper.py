import logging

class LogClsHelper():
    _logger = None

    @classmethod
    def create_logger(cls):
        logger = logging.getLogger(f'{cls.__name__}_{str(id(cls))}')
        logger.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            fmt = '%(asctime)s \t %(name)s \t %(levelname)s \t %(message)s \t ',
            datefmt = '%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)

        return logger

    @classmethod
    def logger(cls):
        if(cls._logger is None):
            cls._logger = cls.create_logger()

        return cls._logger









