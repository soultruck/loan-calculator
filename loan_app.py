import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="부동산 대출 계산기", layout="centered")

st.title("🏠 2026 부동산 대출 계산기")
st.write("이사님, 본부장입니다. 강화된 규제(DSR 3단계)를 반영한 예상 한도입니다.")

# --- 입력 구간 (모바일 터치 친화적) ---
st.subheader("1. 정보 입력")

income_input = st.number_input("연소득 (단위: 억)", value=1.0, step=0.1)
price_input = st.number_input("매매가 (단위: 억)", value=15.0, step=0.1)
debt_input = st.number_input("기존대출 연원리금 (단위: 만원)", value=1000, step=100, help="마통은 한도/5로 계산하세요!")
rate_input = st.number_input("예상 금리 (%)", value=4.0, step=0.1)

region = st.radio("지역 선택", ["규제지역(서울 등)", "비규제지역(지방/경기일부)"])
is_first = st.checkbox("생애최초 구입인가요?")

# --- 계산 로직 (기존과 동일) ---
if st.button("💰 대출 한도 확인하기", type="primary"):
    # 단위 변환
    income = income_input * 100000000
    price = price_input * 100000000
    debt_year = debt_input * 10000
    rate = rate_input
    stress_rate = 1.5 # 스트레스 금리
    
    # LTV 계산
    if region == "규제지역(서울 등)":
        ltv_ratio = 0.8 if is_first else 0.4
    else:
        ltv_ratio = 0.8 if is_first else 0.7
    
    ltv_limit = price * ltv_ratio

    # DSR 계산
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
    constraint = "LTV(집값) 규제" if final_limit == ltv_limit else "DSR(소득) 규제"

    # --- 결과 출력 ---
    st.divider()
    st.success(f"예상 대출 한도는 **{int(final_limit // 1000000):,} 백만 원** 입니다.")
    
    if constraint == "DSR(소득) 규제":
        st.error(f"⛔ 제약 요인: {constraint}\n\n소득 대비 부채가 많아 한도가 줄었습니다.")
    else:
        st.info(f"✅ 제약 요인: {constraint}\n\nLTV 한도까지만 대출이 가능합니다.")
        
    st.caption("※ 본 계산은 2026년 정책 기준 단순 참고용이며, 정확한 한도는 은행 심사를 따릅니다.")
