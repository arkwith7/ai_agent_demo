from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import json

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = 3600  # 1시간

    async def get(self, key: str) -> Optional[Any]:
        """
        캐시에서 데이터를 조회합니다.
        """
        try:
            if key not in self._cache:
                return None
                
            cache_data = self._cache[key]
            if datetime.now() > cache_data['expires_at']:
                del self._cache[key]
                return None
                
            return cache_data['value']
        except Exception as e:
            print(f"Cache get error: {str(e)}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        데이터를 캐시에 저장합니다.
        """
        try:
            ttl = ttl or self.default_ttl
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
            return True
        except Exception as e:
            print(f"Cache set error: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """
        캐시에서 데이터를 삭제합니다.
        """
        try:
            if key in self._cache:
                del self._cache[key]
            return True
        except Exception as e:
            print(f"Cache delete error: {str(e)}")
            return False

    async def clear(self) -> bool:
        """
        모든 캐시를 삭제합니다.
        """
        try:
            self._cache.clear()
            return True
        except Exception as e:
            print(f"Cache clear error: {str(e)}")
            return False

    async def exists(self, key: str) -> bool:
        """
        키가 캐시에 존재하는지 확인합니다.
        """
        try:
            if key not in self._cache:
                return False
                
            cache_data = self._cache[key]
            if datetime.now() > cache_data['expires_at']:
                del self._cache[key]
                return False
                
            return True
        except Exception as e:
            print(f"Cache exists error: {str(e)}")
            return False

    async def ttl(self, key: str) -> int:
        """
        키의 남은 TTL을 반환합니다.
        """
        try:
            if key not in self._cache:
                return -1
                
            cache_data = self._cache[key]
            if datetime.now() > cache_data['expires_at']:
                del self._cache[key]
                return -1
                
            remaining = cache_data['expires_at'] - datetime.now()
            return int(remaining.total_seconds())
        except Exception as e:
            print(f"Cache ttl error: {str(e)}")
            return -1 