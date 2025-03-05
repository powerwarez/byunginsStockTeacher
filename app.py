import streamlit as st
from supabase import create_client, Client
import os

# 환경변수에서 설정값 불러오기
kakao_redirect_uri_env = os.getenv("KAKAO_REDIRECT_URI")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def main():
    # 로그인 상태를 저장하기 위한 세션 변수 초기화
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    # URL 파라미터에서 access_token과 refresh_token 확인
    params = st.experimental_get_query_params()
    if "access_token" in params and "refresh_token" in params:
        # 토큰이 있으면 로그인 성공으로 간주
        st.session_state["logged_in"] = True
        st.session_state["access_token"] = params["access_token"][0]
        st.session_state["refresh_token"] = params["refresh_token"][0]
        # 토큰 정보 저장 후 URL 파라미터 제거
        st.experimental_set_query_params()

    st.sidebar.title("메뉴")
    if not st.session_state.get("logged_in", False):
        if st.sidebar.button("카카오 로그인"):
            try:
                # Supabase의 OAuth 로그인 기능 사용
                auth_response = supabase.auth.sign_in_with_oauth({
                    "provider": "kakao",
                    "options": {
                        "redirect_to": kakao_redirect_uri_env
                    }
                })
                
                # 로그인 URL로 리다이렉트
                if auth_response and "url" in auth_response:
                    login_url = auth_response["url"]
                    # JavaScript를 사용하여 새 창에서 로그인 URL 열기
                    js = f"""
                    <script>
                        window.open("{login_url}", "_blank");
                    </script>
                    """
                    st.markdown(js, unsafe_allow_html=True)
                else:
                    st.sidebar.error("로그인 URL을 가져올 수 없습니다.")
            except Exception as e:
                st.sidebar.error(f"로그인 오류: {str(e)}")
    else:
        st.sidebar.success("로그인 성공!")
        if st.sidebar.button("로그아웃"):
            # 로그아웃 처리
            supabase.auth.sign_out()
            st.session_state["logged_in"] = False
            st.session_state.pop("access_token", None)
            st.session_state.pop("refresh_token", None)
            st.experimental_rerun()

    st.title("초등학생 모의 주식 관리")
    st.write("학생의 계정 및 모의 주식 투자 데이터를 관리하는 시스템입니다.")

if __name__ == "__main__":
    main() 