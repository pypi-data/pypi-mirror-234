import logging
from loguru import logger


class PropogateHandler(logging.Handler):
    def emit(self, record) -> None:
        logging.getLogger(record.name).handle(record)


logger.add(PropogateHandler(), format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")


# # 创建一个logger
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# # 再创建一个handler，用于输出到控制台
# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
#
# # 定义handler的输出格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
#
# # 给logger添加handler
# if not logger.handlers:
#     logger.addHandler(ch)

