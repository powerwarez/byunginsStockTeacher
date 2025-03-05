import streamlit as st
from supabase import create_client, Client

# Supabase 설정, 실제 URL과 Key로 교체 필요
import os
kakao_client_id_env = os.getenv("KAKAO_CLIENT_ID")
kakao_redirect_uri_env = os.getenv("KAKAO_REDIRECT_URI")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def main():
    st.sidebar.title("메뉴")
    # 카카오 로그인 버튼
    if st.sidebar.button("카카오 로그인"):
        # 카카오 OAuth 로그인 URL 설정, 실제 client_id와 redirect_uri로 교체 필요
        kakao_client_id = kakao_client_id_env
        redirect_uri = kakao_redirect_uri_env # 필요에 따라 변경
        login_url = f"https://kauth.kakao.com/oauth/authorize?client_id={kakao_client_id}&redirect_uri={redirect_uri}&response_type=code"
        # 새 창에서 로그인할 수 있도록 링크 생성
        st.sidebar.markdown(f'<a href="{login_url}" target="_blank">새 창에서 카카오 로그인하기</a>', unsafe_allow_html=True)
    
    st.title("초등학생 모의 주식 관리")
    st.write("학생의 계정 및 모의 주식 투자 데이터를 관리하는 시스템입니다.")


if __name__ == "__main__":
    main() 