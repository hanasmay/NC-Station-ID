import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 修正后的 GA DDS 站点数据库 (确保列名与搜索逻辑一致)
site_data = [
    {"ZGH": "001", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.744, "Lon": -84.394, "Note": "Whitehall St"},
    {"ZGH": "003", "DAI": "CARTERSVILLE", "County": "BARTOW", "Lat": 34.165, "Lon": -84.796, "Note": ""},
    {"ZGH": "004", "DAI": "CARROLLTON", "County": "CARROLL", "Lat": 33.580, "Lon": -85.076, "Note": ""},
    {"ZGH": "005", "DAI": "ATHENS", "County": "CLARKE", "Lat": 33.951, "Lon": -83.357, "Note": ""},
    {"ZGH": "007", "DAI": "COLUMBUS", "County": "MUSCOGEE", "Lat": 32.460, "Lon": -84.987, "Note": "Main Office"},
    {"ZGH": "012", "DAI": "MACON", "County": "BIBB", "Lat": 32.840, "Lon": -83.632, "Note": ""},
    {"ZGH": "015", "DAI": "DECATUR", "County": "DEKALB", "Lat": 33.774, "Lon": -84.296, "Note": ""},
    {"ZGH": "018", "DAI": "SAVANNAH", "County": "CHATHAM", "Lat": 32.083, "Lon": -81.099, "Note": "Main Site"},
    {"ZGH": "019", "DAI": "VALDOSTA", "County": "LOWNDES", "Lat": 30.832, "Lon": -83.278, "Note": ""},
    {"ZGH": "021", "DAI": "GAINESVILLE", "County": "HALL", "Lat": 34.297, "Lon": -83.824, "Note": ""},
    {"ZGH": "022", "DAI": "MARIETTA", "County": "COBB", "Lat": 33.952, "Lon": -84.549, "Note": "Cobb County Hub"},
    {"ZGH": "024", "DAI": "AUGUSTA", "County": "RICHMOND", "Lat": 33.470, "Lon": -81.974, "Note": "Main Site"},
    {"ZGH": "031", "DAI": "NORCROSS", "County": "GWINNETT", "Lat": 33.941, "Lon": -84.213, "Note": ""},
    {"ZGH": "033", "DAI": "LAWRENCEVILLE", "County": "GWINNETT", "Lat": 33.956, "Lon": -83.988, "Note": "Main Hub"},
    {"ZGH": "044", "DAI": "CONYERS", "County": "ROCKDALE", "Lat": 33.667, "Lon": -84.017, "Note": ""},
    {"ZGH": "054", "DAI": "SUWANEE", "County": "GWINNETT", "Lat": 34.051, "Lon": -84.062, "Note": ""},
    {"ZGH": "081", "DAI": "FAYETTEVILLE", "County": "FAYETTE", "Lat": 33.447, "Lon": -84.455, "Note": ""},
    {"ZGH": "085", "DAI": "ALPHARETTA", "County": "FULTON", "Lat": 34.075, "Lon": -84.294, "Note": "North Fulton"},
    {"ZGH": "096", "DAI": "NEWNAN", "County": "COWETA", "Lat": 33.376, "Lon": -84.799, "Note": "Newnan CSC"},
    {"ZGH": "137", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.716, "Lon": -84.350, "Note": "Moreland Ave"},
]

df = pd.DataFrame(site_data)

# 页面配置
st.set_page_config(page_title="GA DDS 站点查询全集", layout="wide")
st.title("🍑 佐治亚州 (GA) DDS 站点代码 (ZGH) 汇总大全")

# --- 侧边栏查询逻辑 (修正列名错误) ---
st.sidebar.header("🔍 站点筛选")
query = st.sidebar.text_input("输入 城市(DAI)、县 或 站点代码(ZGH):").upper()

if query:
    # 修正：使用正确的列名 'DAI' 和 'County'，并增加对 'ZGH' 的搜索支持
    filtered_df = df[
        (df['DAI'].str.contains(query, na=False)) | 
        (df['County'].str.contains(query, na=False)) | 
        (df['ZGH'].str.contains(query, na=False))
    ]
else:
    filtered_df = df

# --- 布局：地图与表格 ---
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("📍 站点地理分布")
    m = folium.Map(location=[32.8, -83.6], zoom_start=7)
    
    for _, row in filtered_df.iterrows():
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"ID: {row['ZGH']}<br>DAI: {row['DAI']}<br>County: {row['County']}",
            tooltip=f"{row['DAI']} ({row['ZGH']})"
        ).add_to(m)
    
    st_folium(m, width=600, height=500)

with col_right:
    st.subheader("📋 站点对照表")
    # 只显示业务需要的列
    st.dataframe(filtered_df[['ZGH', 'DAI', 'County', 'Note']], height=450, use_container_width=True)
    
    # 导出功能
    csv = df[['ZGH', 'DAI', 'County', 'Note']].to_csv(index=False).encode('utf-8')
    st.download_button("📥 下载完整对照表 (CSV)", data=csv, file_name='GA_DDS_Station_List.csv', mime='text/csv')
