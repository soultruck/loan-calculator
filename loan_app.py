import streamlit as st

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="전프로의 부동산 계산기", layout="centered", page_icon="🏢")

# --- 헤더(타이틀) ---
st.title("🏢 전프로의 부동산 슈퍼 앱")
st.markdown("### 데이터로 분석하는 부동산 의사결정 도구")
st.write("2026년 최신 정책(DSR 3단계, 청약 가점)이 반영된 버전입니다.")

# --- 탭(Tab) 생성 ---
tab1, tab2 = st.tabs(["💰 대출 한도 계산기", "🏆 청약 가점 계산기"])

# ==========================================
# [탭 1] 대출 한도 계산기 로직
# ==========================================
with tab1:
    st.header("대출 한도 예측 (DSR 3단계)")
    
    # 입력 구간
    st.info("💡 소득과 부채 정보를 입력하시면 전프로의 알고리즘이 분석합니다.")
    
    income_input = st.number_input("연소득 (단위: 억)", value=1.0, step=0.1, key="income")
    price_input = st.number_input("매매가 (단위: 억)", value=15.0, step=0.1, key="price")
    
    # --- [수정된 부분] 기존대출 입력 & 주의사항 가이드 ---
    debt_input = st.number_input("기존대출 연원리금 (단위: 만원)", value=1000, step=100, key="debt")
    
    # 여기가 요청하신 '주의사항 버튼'입니다 (클릭하면 열립니다)
    with st.expander("🚨 주의사항: 정확한 계산을 위해 클릭해서 확인하세요!"):
        st.markdown("""
        **"내가 실제로 내는 돈"과 "은행이 계산하는 돈"은 다릅니다!**
        
        1. **일반 대출 (할부 등)**
           - 매달 내는 (원금 + 이자) × 12개월
           
        2. **★ 신용대출 / 마이너스 통장 (중요!)**
           - 실제 이자만 넣으시면 안 됩니다.
           - **(대출 총 한도금액 ÷ 5년)** 으로 계산해서 더해야 합니다.
           - *예시: 마통 1억을 뚫어놨다면? (실제 쓴 돈이 적어도)*
           - 1억 ÷ 5 = **연 2,000만 원**으로 입력해야 정확합니다.
        
        3. **전세자금대출**
           - 보통 '이자' 부분만 계산에 포함됩니다.
        """)
    # -----------------------------------------------------

    rate_input = st.number_input("예상 금리 (%)", value=4.0, step=0.1, key="rate")
    
    col1, col2 = st.columns(2)
    with col1:
        region = st.radio("지역 선택", ["규제지역(서울 등)", "비규제지역(지방/경기일부)"])
    with col2:
        is_first = st.checkbox("생애최초 구입")

    if st.button("💰 대출 한도 확인하기", type="primary"):
        # 계산 로직
        income = income_input * 100000000
        price = price_input * 100000000
        debt_year = debt_input * 10000
        rate = rate_input
        stress_rate = 1.5 
        
        # LTV
        if region == "규제지역(서울 등)":
            ltv_ratio = 0.8 if is_first else 0.4
        else:
            ltv_ratio = 0.8 if is_first else 0.7
        ltv_limit = price * ltv_ratio

        # DSR
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
        st.success(f"전프로 분석 결과: 예상 대출 한도는 **{int(final_limit // 1000000):,} 백만 원** 입니다.")
        st.caption(f"제약 요인: {constraint} 규제 적용됨")

# ==========================================
# [탭 2] 청약 가점 계산기 로직
# ==========================================
with tab2:
    st.header("청약 가점 계산 (만점 84점)")
    st.info("💡 정확한 가점 계산을 위해 항목을 선택해주세요.")

    # 1. 무주택 기간
    st.subheader("1. 무주택 기간 (32점 만점)")
    no_house_years = st.slider("무주택 기간 선택", 0, 15, 0, format="%d년 이상")
    if no_house_years >= 15:
        score_1 = 32
    elif no_house_years == 0:
        score_1 = 0 
    else:
        score_1 = (no_house_years * 2) + 2
    
    st.write(f"👉 점수: **{score_1}점**")

    # 2. 부양가족 수
    st.subheader("2. 부양가족 수 (35점 만점)")
    dependents = st.number_input("본인 제외 부양가족 수 (명)", 0, 6, 0)
    score_2 = (dependents * 5) + 5
    st.write(f"👉 점수: **{score_2}점**")

    # 3. 통장 가입 기간
    st.subheader("3. 청약통장 가입 기간 (17점 만점)")
    bank_years = st.slider("통장 가입 기간 선택", 0, 15, 0, format="%d년 이상")
    if bank_years >= 15:
        score_3 = 17
    elif bank_years == 0:
        score_3 = 1 
    else:
        score_3 = bank_years + 2
    
    st.write(f"👉 점수: **{score_3}점**")

    # 총점 계산 및 결과
    total_score = score_1 + score_2 + score_3
    
    st.divider()
    st.metric(label="🏆 전프로가 계산한 청약 가점", value=f"{total_score}점", delta="/ 84점 만점")
    
    # 점수별 조언
    if total_score >= 70:
        st.balloons()
        st.success("🎉 축하합니다! 당첨 안정권입니다.")
    elif total_score >= 60:
        st.success("👍 서울 주요 단지 당첨 가능성이 높습니다.")
    elif total_score >= 50:
        st.warning("🤔 전략적인 접근이 필요합니다.")
    else:
        st.error("😭 추첨제를 노려보시는 것을 추천합니다.")

# ==========================================
# [하단부] 개발자 크레딧 (Footer)
# ==========================================
st.divider()
st.markdown(
    """
    <style>
    .footer {
        text-align: center;
        color: grey;
        font-size: 14px;
        margin-top: 50px;
    }
    </style>
    <div class="footer">
        <p>ⓒ 2026 Developed by <b>전프로 (Jeon Pro)</b></p>
        <p>Real Estate Investment & Data Analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)
