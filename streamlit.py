import streamlit as st
import pandas as pd
import os

def load_excel(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        st.error("파일을 찾을 수 없습니다.")
        return None

def save_excel(df, file_path):
    df.to_excel(file_path, index=False)
    st.success("엑셀 파일이 성공적으로 저장되었습니다!")

def main():
    st.title("투자잔액 입력 시스템")
    file_path = "C:\\Users\\skim590\\Downloads\\dataset.xlsx"
    df = load_excel(file_path)
    
    if df is not None:
        # 컬럼명 확인 및 출력
        st.write("엑셀 컬럼명:", df.columns.tolist())

        # 컬럼명의 공백 제거
        df.columns = df.columns.str.strip()

        # 컬럼명이 존재하는지 확인
        if "보수기준" in df.columns and "추가정보" in df.columns:
            filtered_indices = df[df["보수기준"].astype(str).str.contains("투자잔액", na=False)].index
            
            if not filtered_indices.empty:
                user_input = st.text_input("추가정보(D열)에 입력할 값을 입력하세요:")
                if st.button("입력 저장"):
                    df.loc[filtered_indices, "추가정보"] = user_input
                    save_excel(df, file_path)
                    st.dataframe(df)
            else:
                st.warning("'투자잔액'을 포함하는 B열의 데이터가 없습니다.")
        else:
            st.error("보수기준(B열) 또는 추가정보(D열) 컬럼이 존재하지 않습니다.")

if __name__ == "__main__":
    main()
