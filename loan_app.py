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
        st.title("🔒 전박사의 VIP 부동산 계산기")
        st.markdown("### 부동산학(Real Estate) 데이터 분석 도구")
        st.info("비밀번호를 입력해야 사용할 수 있습니다.")

        # 오픈채팅방 유도 버튼 (입장코드 확인용)
        st.markdown(
            """
            <a href="https://open.kakao.com/o/your_link_here" target="_blank">
                <button style="width: 100%; background-color: #FEE500; color: #000000; padding: 15px; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; margin-bottom: 20px;">
                    💬 입장 코드(비밀번호) 확인하기
                </button>
            </a>
            """, unsafe_allow_html=True
        )

        password = st.text_input("비밀번호(Access Code) 입력", type="password")
        if st.button("로그인"):
            if password == "rich2026":  # [설정] 비밀번호
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("비밀번호가 틀렸습니다.")
        return False
    return True

# ==========================================
# [기능 2] 메인 프로그램
# ==========================================
if check_password():
    st.title("🎓 전박사의 부동산 슈퍼 앱")
    st.markdown("### 2026년형 차세대 부동산 분석 알고리즘")
    
    tab1, tab2 = st.tabs(["💰 대출 한도 분석", "🏆 청약 가점 진단"])

    # [탭 1] 대출 한도 계산기 (여기에 영업 기능 추가!)
    with tab1:
        st.header("대출 한도 정밀 분석 (DSR 3단계)")
        st.info("💡 소득과 부채 정보를 입력하시면 전박사의 알고리즘이 분석합니다.")
        
        income_input = st.number_input("연소득 (단위: 억)", value=1.0, step=0.1, key="income")
        price_input = st.number_input("매매가 (단위: 억)", value=15.0, step=0.1, key="price")
        
        debt_input = st.number_input("기존대출 연원리금 (단위: 만원)", value=1000, step=100, key="debt")
        with st.expander("🚨 정확한 입력을 위한 가이드 (필독)"):
            st.markdown("""
            **금융권 심사 기준(DSR)에 맞게 입력해야 오차가 없습니다.**
            1. **일반 대출:** (원금 + 이자) × 12개월
            2. **★ 마이너스 통장:** (총 한도금액 ÷ 5년)
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

            # --- [결과 화면] ---
            st.divider()
            st.success(f"전박사 분석 결과: 예상 대출 한도는 **{int(final_limit // 1000000):,} 백만 원** 입니다.")
            st.caption(f"제약 요인: {constraint} 규제 적용됨")

            # --- [핵심 추가 기능] 추가 대출 영업 버튼 (Call to Action) ---
            st.markdown("---") # 구분선
            st.error("📉 **원하시는 만큼 한도가 안 나오셨나요?**")
            st.markdown("""
            DSR 규제 때문에 1금융권 한도는 여기까지입니다.
            하지만, **사업자 담보 / 2금융권 / 후순위** 등을 활용하면 **추가 한도**를 만들 수 있습니다.
            
            **"전박사님, 저는 얼마까지 더 나올까요?"**
            궁금하시다면 아래 버튼을 눌러 **히든 솔루션**을 상담받으세요.
            """)
            
            # 상담 오픈채팅방 연결 버튼
            st.markdown(
                """
                <a href="https://open.kakao.com/o/your_link_here" target="_blank">
                    <button style="
                        width: 100%;
                        background-color: #381E1F; 
                        color: #FFFFFF;
                        padding: 15px;
                        border: none;
                        border-radius: 10px;
                        font-size: 18px;
                        font-weight: bold;
                        cursor: pointer;
                        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
                        ">
                        🚀 추가 한도(히든 솔루션) 상담하기
                    </button>
                </a>
                <p style="text-align:center; font-size:12px; margin-top:5px; color:grey;">
                ※ 전박사가 직접 검토한 안전한 금융사만 안내합니다.
                </p>
                """,
                unsafe_allow_html=True
            )
            # -----------------------------------------------------------

    # [탭 2] 청약 가점 계산기 (기존 동일)
    with tab2:
        st.header("청약 가점 정밀 진단")
        no_house_years = st.slider("무주택 기간", 0, 15, 0)
        score_1 = 32 if no_house_years >= 15 else (no_house_years * 2) + 2 if no_house_years > 0 else 0
        
        dependents = st.number_input("부양가족 수", 0, 6, 0)
        score_2 = (dependents * 5) + 5
        
        bank_years = st.slider("통장 가입 기간", 0, 15, 0)
        score_3 = 17 if bank_years >= 15 else bank_years + 2 if bank_years > 0 else 1
        
        total_score = score_1 + score_2 + score_3
        st.divider()
        st.metric("🏆 청약 가점", f"{total_score}점", "/ 84점")
        if total_score >= 60: st.success("👍 당첨 가능성이 높습니다.")
        else: st.warning("🤔 전략 수정이 필요합니다.")

    st.divider()
    st.markdown("<div style='text-align: center; color: grey;'>ⓒ 2026 Developed by <b>전박사 (Dr. Jeon)</b></div>", unsafe_allow_html=True)
