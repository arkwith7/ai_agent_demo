import logging
from datetime import datetime
from typing import Optional

class LoggerService:
    def __init__(self):
        self.logger = logging.getLogger('stock_analysis')
        self.logger.setLevel(logging.INFO)
        
        # 이미 핸들러가 있는지 확인
        if not self.logger.handlers:
            # 콘솔 핸들러 설정
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 포맷터 설정
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            # 핸들러 추가
            self.logger.addHandler(console_handler)
        
        # 부모 로거로의 전파 방지
        self.logger.propagate = False

    def info(self, message: str, **kwargs):
        """
        정보 로그를 기록합니다.
        """
        self.logger.info(message, **kwargs)

    def error(self, message: str, **kwargs):
        """
        에러 로그를 기록합니다.
        """
        self.logger.error(message, **kwargs)

    def warning(self, message: str, **kwargs):
        """
        경고 로그를 기록합니다.
        """
        self.logger.warning(message, **kwargs)

    def debug(self, message: str, **kwargs):
        """
        디버그 로그를 기록합니다.
        """
        self.logger.debug(message, **kwargs) 