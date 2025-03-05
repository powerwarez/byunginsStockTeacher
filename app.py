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
    params = st.query_params
    if "access_token" in params and "refresh_token" in params:
        # 토큰이 있으면 로그인 성공으로 간주
        st.session_state["logged_in"] = True
        st.session_state["access_token"] = params["access_token"]
        st.session_state["refresh_token"] = params["refresh_token"]
        # 토큰 정보 저장 후 URL 파라미터 제거
        params.clear()

    st.sidebar.title("메뉴")
    if not st.session_state.get("logged_in", False):
        if st.sidebar.button("카카오 로그인"):
            try:
                # 환경 변수 확인
                st.sidebar.write(f"SUPABASE_URL: {supabase_url[:10]}..." if supabase_url else "SUPABASE_URL 없음")
                st.sidebar.write(f"SUPABASE_KEY: {supabase_key[:5]}..." if supabase_key else "SUPABASE_KEY 없음")
                st.sidebar.write(f"REDIRECT_URI: {kakao_redirect_uri_env}" if kakao_redirect_uri_env else "REDIRECT_URI 없음")
                
                # Supabase의 OAuth 로그인 기능 사용
                auth_response = supabase.auth.sign_in_with_oauth({
                    "provider": "kakao",
                    "options": {
                        "redirect_to": kakao_redirect_uri_env
                    }
                })
                
                # API 응답 구조 확인 및 디버깅
                st.sidebar.write("API 응답 타입:", type(auth_response))
                st.sidebar.json(auth_response)
                
                # 응답에서 URL 추출 (다양한 방법 시도)
                login_url = None
                
                # 1. 딕셔너리로 처리
                if isinstance(auth_response, dict):
                    if "url" in auth_response:
                        login_url = auth_response["url"]
                    elif "data" in auth_response and "url" in auth_response["data"]:
                        login_url = auth_response["data"]["url"]
                
                # 2. 객체 속성으로 처리
                elif hasattr(auth_response, "url"):
                    login_url = auth_response.url
                elif hasattr(auth_response, "data") and hasattr(auth_response.data, "url"):
                    login_url = auth_response.data.url
                
                # URL이 있으면 새 창에서 열기
                if login_url:
                    st.sidebar.success(f"로그인 URL 생성 성공: {login_url[:30]}...")
                    js = f"""
                    <script>
                        window.open("{login_url}", "_blank");
                    </script>
                    """
                    st.markdown(js, unsafe_allow_html=True)
                else:
                    st.sidebar.error("로그인 URL을 찾을 수 없습니다. API 응답 구조를 확인하세요.")
            except Exception as e:
                st.sidebar.error(f"로그인 오류: {str(e)}")
                import traceback
                st.sidebar.code(traceback.format_exc())
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