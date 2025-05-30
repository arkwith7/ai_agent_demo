#!/usr/bin/env python3
"""
관리자 사용자 생성 스크립트
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from api.routers.crud.crud_user import create_user, get_user_by_username, get_user_by_email
from schemas.user import UserCreate
from db.models.user import UserRole

async def create_admin_user():
    """관리자 사용자 생성"""
    print("관리자 사용자 생성을 시작합니다...")
    
    # 사용자 입력 받기
    username = input("관리자 사용자명을 입력하세요: ").strip()
    if not username:
        print("사용자명은 필수입니다.")
        return False
    
    email = input("관리자 이메일을 입력하세요: ").strip()
    if not email:
        print("이메일은 필수입니다.")
        return False
    
    password = input("관리자 비밀번호를 입력하세요: ").strip()
    if not password:
        print("비밀번호는 필수입니다.")
        return False
    
    # 관리자 사용자 생성
    admin_user = UserCreate(
        username=username,
        email=email,
        password=password,
        role=UserRole.ADMIN
    )
    
    try:
        # 데이터베이스 세션 생성
        from db.session import async_engine
        from sqlalchemy.ext.asyncio import async_sessionmaker
        
        async_session = async_sessionmaker(async_engine, expire_on_commit=False)
        
        async with async_session() as db:
            # 중복 확인
            existing_user = await get_user_by_username(db, username=username)
            if existing_user:
                print(f"사용자명 '{username}'은 이미 존재합니다.")
                return False
            
            existing_email = await get_user_by_email(db, email=email)
            if existing_email:
                print(f"이메일 '{email}'은 이미 존재합니다.")
                return False
            
            # 관리자 사용자 생성
            new_admin = await create_user(db, admin_user)
            print(f"관리자 사용자가 성공적으로 생성되었습니다!")
            print(f"- ID: {new_admin.id}")
            print(f"- 사용자명: {new_admin.username}")
            print(f"- 이메일: {new_admin.email}")
            print(f"- 역할: {new_admin.role.value}")
            print(f"- 생성 시간: {new_admin.created_at}")
            
            return True
            
    except Exception as e:
        print(f"관리자 사용자 생성 중 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(create_admin_user())
    sys.exit(0 if success else 1)
