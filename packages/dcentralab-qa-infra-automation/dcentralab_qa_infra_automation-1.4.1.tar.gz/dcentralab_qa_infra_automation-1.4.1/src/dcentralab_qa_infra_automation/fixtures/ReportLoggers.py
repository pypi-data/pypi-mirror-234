import logging
"""
Initialized of logger for html reports

@Author: Efrat Cohen
@Date: 04.2023
"""


def before_test(request):
    """
    Init logger instance for using anywhere to write logs to pytest html reports
    :param request: the requesting test context
    """
    logger = logging.getLogger(request.node.name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    request.cls.logger = logger