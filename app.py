import streamlit as st
from supabase import create_client, Client
import os

# 환경변수에서 설정값 불러오기
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
redirect_url = os.getenv("KAKAO_REDIRECT_URI")
supabase: Client = create_client(supabase_url, supabase_key)


def main():
    st.sidebar.title("메뉴")
    st.title("초등학생 모의 주식 관리")
    st.write("학생의 계정 및 모의 주식 투자 데이터를 관리하는 시스템입니다.")
    
    # 카카오 로그인 버튼 추가
    if st.sidebar.button("카카오 로그인"):
        try:
            sign_in_response = supabase.auth.sign_in_with_oauth({
                "provider": "kakao",
                "options": {
                    "redirect_to": redirect_url,
                    "scopes": "account_email"
                }
            })
            if sign_in_response and hasattr(sign_in_response, "url"):
                login_url = sign_in_response.url
                st.sidebar.success("로그인 URL 생성 완료! 아래 버튼을 클릭해주세요.")
                st.sidebar.markdown(
                    f'<a href="{login_url}" target="_self" style="display: inline-block; padding: 10px 20px; background-color: #FEE500; color: black; text-decoration: none; border-radius: 5px; font-weight: bold; text-align: center;">카카오 로그인 페이지로 이동</a>',
                    unsafe_allow_html=True
                )
            else:
                st.sidebar.error("로그인 URL 생성 실패.")
        except Exception as e:
            st.sidebar.error(f"로그인 요청 중 오류 발생: {str(e)}")
    

if __name__ == "__main__":
    main() 