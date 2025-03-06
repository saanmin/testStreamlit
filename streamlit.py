import streamlit as st
import pandas as pd
import os

def load_excel(file_path):
    """엑셀 파일 로드 함수"""
    if os.path.exists(file_path):
        return pd.read_excel(file_path, dtype=str)  # 모든 컬럼을 문자열로 변환
    else:
        st.error("파일을 찾을 수 없습니다.")
        return None

def save_excel(df, file_path):
    """엑셀 파일 저장 함수"""
    df.to_excel(file_path, index=False)
    st.success(f"엑셀 파일이 성공적으로 저장되었습니다! → {file_path}")

def main():
    st.title("투자잔액 입력 시스템")
    
    # 사용자로부터 파일 업로드 받기
    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
    
    if uploaded_file is not None:
        temp_file_path = "temp_uploaded_file.xlsx"

        # 업로드된 파일을 로컬에 저장
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        df = pd.read_excel(temp_file_path, dtype=str)  # 문자열 변환

        # 컬럼명 확인 및 출력
        st.write("엑셀 컬럼명:", df.columns.tolist())

        # 컬럼명의 공백 제거
        df.columns = df.columns.str.strip()

        # "추가정보" 컬럼을 문자열 타입으로 변환하여 데이터 추가 가능하게 설정
        if "추가정보" in df.columns:
            df["추가정보"] = df["추가정보"].astype(str)

        # 컬럼명이 존재하는지 확인
        if "보수기준" in df.columns and "추가정보" in df.columns:
            for index, row in df.iterrows():
                st.write(f"### 행 {index + 1}")
                st.write(row)

                if "투자총액" in str(row["보수기준"]):
                    df.at[index, "추가정보"] = "추가적인 정보입력이 불필요합니다"
                    st.write("✅ 추가적인 정보입력이 불필요합니다.")
                elif "투자잔액" in str(row["보수기준"]):
                    user_input = st.text_input(f"추가정보(D열)에 입력할 값을 입력하세요 (행 {index + 1}):", key=f"input_{index}")
                    reason_input = st.text_input(f"판단한 사유를 입력하세요 (행 {index + 1}):", key=f"reason_{index}")
                    if st.button(f"입력 저장 (행 {index + 1})", key=f"save_{index}"):
                        df.at[index, "추가정보"] = f"{user_input} (사유: {reason_input})"
                        st.success(f"행 {index + 1}이 업데이트되었습니다.")
            
            st.dataframe(df.astype(str))  # 문자열 변환하여 Streamlit에서 처리 가능하도록 함
            
            # 새로운 엑셀 파일 경로 설정
            updated_file_path = "updated_dataset.xlsx"

            if st.button("엑셀 저장"):
                save_excel(df, updated_file_path)

                # 다운로드 버튼 추가
                with open(updated_file_path, "rb") as f:
                    st.download_button(
                        label="📥 업데이트된 엑셀 다운로드",
                        data=f,
                        file_name="updated_dataset.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.error("보수기준(B열) 또는 추가정보(D열) 컬럼이 존재하지 않습니다.")

if __name__ == "__main__":
    main()
