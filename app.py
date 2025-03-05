import streamlit as st
from supabase import create_client, Client
import os
from typing import Optional
import urllib.parse

# 환경변수에서 설정값 불러오기
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
redirect_url = os.getenv("REDIRECT_URL", "https://stocksimulteacher.streamlit.app")
supabase: Client = create_client(supabase_url, supabase_key)

# 로그인 상태 확인 함수
def get_session():
    """현재 세션에서 사용자 정보를 가져옵니다."""
    try:
        return supabase.auth.get_session()
    except Exception:
        return None

# 사용자 정보 가져오기 함수
def get_user():
    """현재 로그인된 사용자 정보를 가져옵니다."""
    session = get_session()
    if session and hasattr(session, "user"):
        return session.user
    return None

def main():
    # 사이드바 설정
    st.sidebar.title("메뉴")
    
    # 세션 상태 초기화
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None
    
    # URL 파라미터 확인
    params = st.query_params
    
    # 오류 메시지 확인 및 표시
    if "error" in params and "error_description" in params:
        error = params["error"]
        error_description = params["error_description"]
        st.sidebar.error(f"로그인 오류: {error}")
        st.sidebar.error(f"오류 설명: {urllib.parse.unquote(error_description)}")
        # 오류 파라미터 제거
        params.clear()
        st.experimental_rerun()
    
    # OAuth 콜백 처리 (access_token, refresh_token 확인)
    if "access_token" in params and "refresh_token" in params:
        try:
            # 토큰으로 세션 설정
            supabase.auth.set_session(params["access_token"], params["refresh_token"])
            # 세션 정보 가져오기
            session = get_session()
            if session:
                st.session_state.authenticated = True
                st.session_state.user = session.user
                st.sidebar.success("로그인에 성공했습니다!")
            # URL 파라미터 제거
            params.clear()
            st.experimental_rerun()
        except Exception as e:
            st.sidebar.error(f"로그인 처리 중 오류가 발생했습니다: {str(e)}")
            params.clear()
    
    # 현재 세션 확인
    current_session = get_session()
    if current_session and not st.session_state.authenticated:
        st.session_state.authenticated = True
        st.session_state.user = current_session.user
    
    # 로그인 상태에 따른 UI 표시
    if not st.session_state.authenticated:
        # 카카오 로그인 버튼
        if st.sidebar.button("카카오 로그인", key="kakao_login"):
            try:
                # Supabase OAuth 로그인 요청
                sign_in_response = supabase.auth.sign_in_with_oauth({
                    "provider": "kakao",
                    "options": {
                        "redirect_to": redirect_url,
                        "scopes": "account_email"
                    }
                })
                
                # 로그인 URL 확인 및 리다이렉트
                if sign_in_response and hasattr(sign_in_response, "url"):
                    login_url = sign_in_response.url
                    # 현재 창에서 로그인 페이지 열기
                    js = f"""
                    <script>
                        window.location.href = "{login_url}";
                    </script>
                    """
                    st.markdown(js, unsafe_allow_html=True)
                    st.stop()
                else:
                    st.sidebar.error("로그인 URL을 가져올 수 없습니다.")
            except Exception as e:
                st.sidebar.error(f"로그인 요청 중 오류가 발생했습니다: {str(e)}")
    else:
        # 로그인 성공 시 사용자 정보 표시
        user = st.session_state.user
        st.sidebar.success(f"로그인 성공! 안녕하세요, {user.email if hasattr(user, 'email') and user.email else '사용자'}님!")
        
        # 로그아웃 버튼
        if st.sidebar.button("로그아웃"):
            try:
                # Supabase 로그아웃 처리
                supabase.auth.sign_out()
                # 세션 상태 초기화
                st.session_state.authenticated = False
                st.session_state.user = None
                st.experimental_rerun()
            except Exception as e:
                st.sidebar.error(f"로그아웃 중 오류가 발생했습니다: {str(e)}")
    
    # 메인 콘텐츠
    st.title("초등학생 모의 주식 관리")
    st.write("학생의 계정 및 모의 주식 투자 데이터를 관리하는 시스템입니다.")
    
    # 로그인 상태에 따른 콘텐츠 표시
    if st.session_state.authenticated:
        st.write("로그인되었습니다. 학생 데이터를 관리할 수 있습니다.")
        # 여기에 로그인 후 표시할 콘텐츠 추가
    else:
        st.info("로그인이 필요합니다. 왼쪽 사이드바에서 카카오 로그인을 진행해주세요.")

if __name__ == "__main__":
    main() 