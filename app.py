import streamlit as st
from supabase import create_client, Client
import secrets
import os

# Supabase 설정, 실제 URL과 Key로 교체 필요
kakao_client_id_env = os.getenv("KAKAO_CLIENT_ID")
kakao_redirect_uri_env = os.getenv("KAKAO_REDIRECT_URI")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def main():
    # 로그인 상태를 저장하기 위한 세션 변수 초기화
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    st.sidebar.title("메뉴")
    if not st.session_state["logged_in"]:
        # OAuth state 생성
        state = secrets.token_urlsafe(16)
        st.session_state["oauth_state"] = state
        kakao_client_id = kakao_client_id_env
        redirect_uri = kakao_redirect_uri_env  # 필요에 따라 변경
        login_url = (
            f"https://kauth.kakao.com/oauth/authorize?client_id={kakao_client_id}"
            f"&redirect_uri={redirect_uri}&response_type=code&state={state}"
        )
        
        # HTML 버튼에 링크를 합쳐서 새 창에서 열리도록 설정
        button_html = f"""
        <style>
            .login-button {{
                background-color: #FEE500;
                border: none;
                color: #000000;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }}
        </style>
        <a href='{login_url}' target='_blank'>
            <button class='login-button'>카카오 로그인</button>
        </a>
        """
        st.sidebar.markdown(button_html, unsafe_allow_html=True)
    else:
        st.sidebar.success("로그인 성공!")
        st.sidebar.button("카카오 로그인", disabled=True)

    st.title("초등학생 모의 주식 관리")
    st.write("학생의 계정 및 모의 주식 투자 데이터를 관리하는 시스템입니다.")


if __name__ == "__main__":
    main() 