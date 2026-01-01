import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 深度补全的 GA DDS 站点数据库
# 整合了城市 (DAI)、站点代码 (ZGH) 和县 (County)
site_data = [
    {"ZGH": "001", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.744, "Lon": -84.394, "Note": "Whitehall St"},
    {"ZGH": "003", "DAI": "CARTERSVILLE", "County": "BARTOW", "Lat": 34.165, "Lon": -84.796, "Note": ""},
    {"ZGH": "004", "DAI": "CARROLLTON", "County": "CARROLL", "Lat": 33.580, "Lon": -85.076, "Note": ""},
    {"ZGH": "005", "DAI": "ATHENS", "County": "CLARKE", "Lat": 33.951, "Lon": -83.357, "Note": ""},
    {"ZGH": "007", "DAI": "COLUMBUS", "County": "MUSCOGEE", "Lat": 32.460, "Lon": -84.987, "Note": "Main Office"},
    {"ZGH": "010", "DAI": "AMERICUS", "County": "SUMTER", "Lat": 32.072, "Lon": -84.232, "Note": ""},
    {"ZGH": "012", "DAI": "MACON", "County": "BIBB", "Lat": 32.840, "Lon": -83.632, "Note": ""},
    {"ZGH": "015", "DAI": "DECATUR", "County": "DEKALB", "Lat": 33.774, "Lon": -84.296, "Note": ""},
    {"ZGH": "018", "DAI": "SAVANNAH", "County": "CHATHAM", "Lat": 32.083, "Lon": -81.099, "Note": "Main Site"},
    {"ZGH": "019", "DAI": "VALDOSTA", "County": "LOWNDES", "Lat": 30.832, "Lon": -83.278, "Note": ""},
    {"ZGH": "021", "DAI": "GAINESVILLE", "County": "HALL", "Lat": 34.297, "Lon": -83.824, "Note": ""},
    {"ZGH": "022", "DAI": "MARIETTA", "County": "COBB", "Lat": 33.952, "Lon": -84.549, "Note": "Cobb County Hub"},
    {"ZGH": "023", "DAI": "BRUNSWICK", "County": "GLYNN", "Lat": 31.149, "Lon": -81.491, "Note": ""},
    {"ZGH": "024", "DAI": "AUGUSTA", "County": "RICHMOND", "Lat": 33.470, "Lon": -81.974, "Note": "Main Site"},
    {"ZGH": "027", "DAI": "DALTON", "County": "WHITFIELD", "Lat": 34.769, "Lon": -84.970, "Note": ""},
    {"ZGH": "028", "DAI": "CANTON", "County": "CHEROKEE", "Lat": 34.237, "Lon": -84.494, "Note": ""},
    {"ZGH": "029", "DAI": "CEDARTOWN", "County": "POLK", "Lat": 34.053, "Lon": -85.255, "Note": ""},
    {"ZGH": "031", "DAI": "NORCROSS", "County": "GWINNETT", "Lat": 33.941, "Lon": -84.213, "Note": ""},
    {"ZGH": "033", "DAI": "LAWRENCEVILLE", "County": "GWINNETT", "Lat": 33.956, "Lon": -83.988, "Note": "Main Hub"},
    {"ZGH": "040", "DAI": "ALBANY", "County": "DOUGHERTY", "Lat": 31.578, "Lon": -84.155, "Note": ""},
    {"ZGH": "043", "DAI": "CALHOUN", "County": "GORDON", "Lat": 34.502, "Lon": -84.951, "Note": ""},
    {"ZGH": "044", "DAI": "CONYERS", "County": "ROCKDALE", "Lat": 33.667, "Lon": -84.017, "Note": ""},
    {"ZGH": "048", "DAI": "NORCROSS", "County": "GWINNETT", "Lat": 33.930, "Lon": -84.120, "Note": "Beaver Ruin Rd"},
    {"ZGH": "050", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.753, "Lon": -84.385, "Note": "Downtown"},
    {"ZGH": "054", "DAI": "SUWANEE", "County": "GWINNETT", "Lat": 34.051, "Lon": -84.062, "Note": ""},
    {"ZGH": "067", "DAI": "CONYERS", "County": "ROCKDALE", "Lat": 33.650, "Lon": -84.030, "Note": "Auxiliary"},
    {"ZGH": "068", "DAI": "DOUGLASVILLE", "County": "DOUGLAS", "Lat": 33.751, "Lon": -84.747, "Note": ""},
    {"ZGH": "081", "DAI": "FAYETTEVILLE", "County": "FAYETTE", "Lat": 33.447, "Lon": -84.455, "Note": ""},
    {"ZGH": "085", "DAI": "ALPHARETTA", "County": "FULTON", "Lat": 34.075, "Lon": -84.294, "Note": "North Fulton"},
    {"ZGH": "095", "DAI": "BLAIRSVILLE", "County": "UNION", "Lat": 34.876, "Lon": -83.958, "Note": ""},
    {"ZGH": "096", "DAI": "NEWNAN", "County": "COWETA", "Lat": 33.376, "Lon": -84.799, "Note": "Newnan CSC"},
    {"ZGH": "105", "DAI": "CANTON", "County": "CHEROKEE", "Lat": 34.220, "Lon": -84.480, "Note": "Auxiliary"},
    {"ZGH": "108", "DAI": "CUMMING", "County": "FORSYTH", "Lat": 34.207, "Lon": -84.140, "Note": ""},
    {"ZGH": "137", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.716, "Lon": -84.350, "Note": "Moreland Ave"},
]

df = pd.DataFrame(site_data)

# Streamlit 页面配置
st.set_page_config(page_title="GA DDS 站点查询全集", layout="wide")

st.title("🍑 佐治亚州 (GA) DDS 站点代码 (ZGH) 汇总大全")
st.markdown("该工具集成了 GA 州所有 DDS 办公地点、对应城市 (DAI) 及所属县 (County)。")

# --- 侧边栏：多维度查询 ---
st.sidebar.header("🔍 站点筛选")
query = st.sidebar.text_input("输入 城市、县 或 站点代码:").upper()

if query:
    mask = df.apply(lambda row: query in row.astype(str).values, axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

# --- 主界面：地图与表格 ---
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("📍 站点地理分布")
    # 初始化地图
    m = folium.Map(location=[32.8, -83.6], zoom_start=7, tiles="OpenStreetMap")
    
    # 在地图上标记筛选后的点
    for _, row in filtered_df.iterrows():
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"ID: {row['ZGH']}<br>DAI: {row['DAI']}<br>County: {row['County']}",
            tooltip=f"{row['DAI']} ({row['ZGH']})",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    
    st_folium(m, width=600, height=500)

with col_right:
    st.subheader("📋 站点对照表")
    # 动态显示过滤后的表格
    st.dataframe(filtered_df[['ZGH', 'DAI', 'County', 'Note']], height=450, use_container_width=True)
    
    # 导出功能
    csv = df[['ZGH', 'DAI', 'County', 'Note']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 下载完整对照表 (CSV/XLS 兼容)",
        data=csv,
        file_name='GA_DDS_Station_Full_List.csv',
        mime='text/csv',
    )

st.divider()
st.caption("提示：在条码生成中，请确保 ZGH 字段为 3 位数字（如 018），DAI 字段与上述城市名完全一致。")
