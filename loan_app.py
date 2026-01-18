import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="전박사의 시크릿 계산기", layout="centered", page_icon="🎓")

# ==========================================
# [기능 1] 비밀번호(로그인) 체크 함수
# ==========================================
def check_password():
    """비밀번호가 맞는지 확인하는 함수"""
    
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        # 로그인 화면 디자인
        st.title("🔒 전박사의 VIP 부동산 계산기")
        st.markdown("### 부동산학(Real Estate) 데이터 분석 도구")
        st.write("이 프로그램은 **전박사 부동산 멤버십** 전용입니다.")
        st.info("비밀번호를 입력해야 사용할 수 있습니다.")

        # 오픈채팅방 유도 버튼 (링크 수정 필요)
        st.markdown(
            """
            <a href="https://open.kakao.com/o/your_link_here" target="_blank">
                <button style="
                    width: 100%;
                    background-color: #FEE500;
                    color: #000000;
                    padding: 15px;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-bottom: 20px;">
                    💬 비밀번호 확인하러 가기 (오픈채팅방 입장)
                </button>
            </a>
            <p style="text-align:center; font-size:12px; color:grey;">
            ※ 채팅방 공지사항에서 '입장코드'를 확인하세요.
            </p>
            """,
            unsafe_allow_html=True
        )

        # 비밀번호 입력창
        password = st.text_input("비밀번호(Access Code) 입력", type="password")
        
        if st.button("로그인"):
            if password == "rich2026":  # <--- [중요] 비밀번호 설정
                st.session_state.password_correct = True
                st.rerun()  # 화면 새로고침
            else:
                st.error("비밀번호가 틀렸습니다. 채팅방 공지를 확인해주세요.")
        
        return False # 아직 로그인 안됨
    
    return True # 로그인 성공

# ==========================================
# [기능 2] 메인 프로그램 (로그인 성공 시 실행)
# ==========================================
if check_password():
    # --- 헤더 및 소개 ---
    st.title("🎓 전박사의 부동산 슈퍼 앱")
    st.markdown("### 2026년형 차세대 부동산 분석 알고리즘")
    st.write("강화된 DSR 3단계와 최신 청약 제도를 반영한 연구용 모델입니다.")
    
    # 탭(Tab) 생성
    tab1, tab2 = st.tabs(["💰 대출 한도 분석", "🏆 청약 가점 진단"])

    # [탭 1] 대출 한도 계산기
    with tab1:
        st.header("대출 한도 정밀 분석 (DSR 3단계)")
        st.info("💡 소득과 부채 정보를 입력하시면 전박사의 알고리즘이 분석합니다.")
        
        income_input = st.number_input("연소득 (단위: 억)", value=1.0, step=0.1, key="income")
        price_input = st.number_input("매매가 (단위: 억)", value=15.0, step=0.1, key="price")
        
        debt_input = st.number_input("기존대출 연원리금 (단위: 만원)", value=1000, step=100, key="debt")
        with st.expander("🚨 [전박사 노트] 정확한 입력을 위한 가이드"):
            st.markdown("""
            **금융권 심사 기준(DSR)에 맞게 입력해야 오차가 없습니다.**
            
            1. **일반 대출:** 실제 납부하는 (원금 + 이자) × 12개월
            2. **★ 마이너스 통장 (핵심):**
               - 실제 쓴 돈이 아니라 **한도 금액**이 기준입니다.
               - **(총 한도금액 ÷ 5년)** 값을 입력하세요.
               - *이 부분을 놓치면 한도 계산이 크게 틀립니다.*
            """)

        rate_input = st.number_input("예상 금리 (%)", value=4.0, step=0.1, key="rate")
        
        col1, col2 = st.columns(2)
        with col1:
            region = st.radio("지역 선택", ["규제지역(서울 등)", "비규제지역(지방/경기일부)"])
        with col2:
            is_first = st.checkbox("생애최초 구입")

        if st.button("💰 대출 한도 분석 실행", type="primary"):
            # 계산 로직
            income = income_input * 100000000
            price = price_input * 100000000
            debt_year = debt_input * 10000
            rate = rate_input
            stress_rate = 1.5 
            
            if region == "규제지역(서울 등)":
                ltv_ratio = 0.8 if is_first else 0.4
            else:
                ltv_ratio = 0.8 if is_first else 0.7
            ltv_limit = price * ltv_ratio

            dsr_ratio = 0.4
            virtual_rate = (rate + stress_rate) / 100
            max_annual_payment = (income * dsr_ratio) - debt_year
            
            if max_annual_payment <= 0:
                dsr_limit = 0
            else:
                loan_term = 40
                monthly_rate = virtual_rate / 12
                num_payments = loan_term * 12
                max_monthly = max_annual_payment / 12
                dsr_limit = (max_monthly / monthly_rate) * (1 - (1 + monthly_rate) ** (-num_payments))

            final_limit = min(ltv_limit, dsr_limit)
            constraint = "LTV(집값)" if final_limit == ltv_limit else "DSR(소득)"

            st.divider()
            st.success(f"전박사 분석 결과: 예상 대출 한도는 **{int(final_limit // 1000000):,} 백만 원** 입니다.")
            st.caption(f"제약 요인: {constraint} 규제 적용됨")

    # [탭 2] 청약 가점 계산기
    with tab2:
        st.header("청약 가점 정밀 진단 (84점 만점)")
        st.info("💡 정확한 진단을 위해 본인의 정보를 선택해주세요.")

        no_house_years = st.slider("무주택 기간 선택", 0, 15, 0, format="%d년 이상")
        if no_house_years >= 15: score_1 = 32
        elif no_house_years == 0: score_1 = 0 
        else: score_1 = (no_house_years * 2) + 2
        st.write(f"👉 점수: **{score_1}점**")

        dependents = st.number_input("본인 제외 부양가족 수 (명)", 0, 6, 0)
        score_2 = (dependents * 5) + 5
        st.write(f"👉 점수: **{score_2}점**")

        bank_years = st.slider("통장 가입 기간 선택", 0, 15, 0, format="%d년 이상")
        if bank_years >= 15: score_3 = 17
        elif bank_years == 0: score_3 = 1 
        else: score_3 = bank_years + 2
        st.write(f"👉 점수: **{score_3}점**")

        total_score = score_1 + score_2 + score_3
        
        st.divider()
        st.metric(label="🏆 전박사가 진단한 청약 가점", value=f"{total_score}점", delta="/ 84점 만점")
        
        if total_score >= 70:
            st.balloons()
            st.success("🎉 [진단] 강남권 로또 청약 당첨 안정권입니다.")
        elif total_score >= 60:
            st.success("👍 [진단] 서울 주요 단지 당첨 가능성이 매우 높습니다.")
        else:
            st.warning("🤔 [진단] 가점보다는 추첨제 등 전략 수정이 필요합니다.")

    # [하단부] 개발자 크레딧
    st.divider()
    st.markdown(
        """
        <style>
        .footer { text-align: center; color: grey; font-size: 14px; margin-top: 50px; }
        </style>
        <div class="footer">
            <p>ⓒ 2026 Developed by <b>전박사 (Dr. Jeon)</b></p>
            <p>Real Estate Investment Lab & Data Analysis</p>
        </div>
        """,
        unsafe_allow_html=True
    )
