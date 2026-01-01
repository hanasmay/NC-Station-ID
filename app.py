import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 完善后的 GA DDS 站点数据库
# 包含你之前确认的所有站点及其对应关系
site_dict = [
    {"ID": "096", "City": "NEWNAN", "County": "Coweta", "Lat": 33.376, "Lon": -84.799},
    {"ID": "054", "City": "SUWANEE", "County": "Gwinnett", "Lat": 34.051, "Lon": -84.062},
    {"ID": "018", "City": "SAVANNAH", "County": "Chatham", "Lat": 32.080, "Lon": -81.091},
    {"ID": "022", "City": "MARIETTA", "County": "Cobb", "Lat": 33.952, "Lon": -84.549},
    {"ID": "048", "City": "NORCROSS", "County": "Gwinnett", "Lat": 33.941, "Lon": -84.132},
    {"ID": "067", "City": "CONYERS", "County": "Rockdale", "Lat": 33.667, "Lon": -84.017},
    {"ID": "050", "City": "ATLANTA", "County": "Fulton", "Lat": 33.749, "Lon": -84.388},
    {"ID": "051", "City": "AUGUSTA", "County": "Richmond", "Lat": 33.470, "Lon": -81.974},
    {"ID": "081", "City": "FAYETTEVILLE", "County": "Fayette", "Lat": 33.447, "Lon": -84.455},
    {"ID": "033", "City": "LAWRENCEVILLE", "County": "Gwinnett", "Lat": 33.956, "Lon": -83.988},
    {"ID": "105", "City": "CANTON", "County": "Cherokee", "Lat": 34.237, "Lon": -84.494},
    {"ID": "108", "City": "CUMMING", "County": "Forsyth", "Lat": 34.207, "Lon": -84.140},
]

df = pd.DataFrame(site_dict)

# 页面设置
st.set_page_config(page_title="GA DDS 条码助手", layout="wide", initial_sidebar_state="expanded")

# 自定义 CSS 样式
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🍑 GA 州 DDS 站点地理辅助工具")
st.caption("版本：v1.2 | 专为 AAMVA 387-Byte Bit-for-bit 复刻优化")

# --- 侧边栏：交互查询 ---
st.sidebar.header("🔍 城市/县查询")
search_query = st.sidebar.text_input("输入城市或县名称:").upper()

if search_query:
    # 同时搜索城市和县
    filtered_df = df[(df['City'].str.contains(search_query)) | (df['County'].str.upper().contains(search_query))]
    
    if not filtered_df.empty:
        for idx, row in filtered_df.iterrows():
            with st.sidebar.expander(f"📍 {row['City']} (ID: {row['ID']})", expanded=True):
                st.write(f"**县**: {row['County']}")
                st.write(f"**站点 ID**: `{row['ID']}`")
                # 字节对齐预警
                city_len = len(row['City'])
                st.info(f"📏 DAI 长度: {city_len} 字节")
                if city_len != 6: # 假设你的模板是以 NEWNAN (6位) 为准
                    st.warning(f"注意：该城市长度与 NEWNAN 不符，偏移量将漂移 {city_len - 6} 字节！")
    else:
        st.sidebar.error("未找到对应站点。")

# --- 主界面布局 ---
col_map, col_data = st.columns([3, 2])

with col_map:
    st.subheader("🗺️ 站点分布图")
    # 设置地图中心为佐治亚州中心
    m = folium.Map(location=[32.8, -83.6], zoom_start=7, tiles="CartoDB positron")
    
    for i, row in df.iterrows():
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"ID: {row['ID']}<br>City: {row['City']}<br>County: {row['County']}",
            tooltip=f"{row['City']} ({row['ID']})",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    
    st_folium(m, width=700, height=500)

with col_data:
    st.subheader("📊 站点对照表")
    # 显示表格并允许下载
    st.dataframe(df[['ID', 'City', 'County']], height=400, use_container_width=True)
    
    csv = df[['ID', 'City', 'County']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 下载完整站点 XLS (CSV 格式)",
        data=csv,
        file_name='GA_DDS_Station_Full_List.csv',
        mime='text/csv',
    )

st.divider()

# --- 底部：复刻知识库 ---
with st.expander("🛠️ 针对 387 字节 GA 样本的复刻提示"):
    st.markdown("""
    1. **DAI 长度对齐**：`NEWNAN`(6) vs `SAVANNAH`(8)。如果 DAI 长度改变，必须手动调整 `DL` 子文件设计器的 Length 位。
    2. **ZGH 格式**：GA 州固定为 3 位数字（补 0），例如 `018` 而非 `18`。
    3. **县名同步**：确保条码中的 `ZGD` 字段与此处查询到的县名一致。
    4. **DAK 空格**：邮编后方必须跟两个 Hex 空格 `20 20`。
    """)
