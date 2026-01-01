import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# 1. 完整 GA DDS 站点数据库
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
geolocator = Nominatim(user_agent="ga_dds_locator")

st.set_page_config(page_title="GA DDS 智能站点助手", layout="wide")
st.title("🍑 佐治亚州 (GA) DDS 站点智能查询系统")

# --- 侧边栏搜索逻辑 ---
st.sidebar.header("🔍 搜索与推荐")
query = st.sidebar.text_input("输入城市、县或站点代码:").upper()

search_lat, search_lon = None, None
is_recommendation = False

if query:
    # 1. 尝试直接匹配
    filtered_df = df[
        (df['DAI'].str.contains(query, na=False)) | 
        (df['County'].str.contains(query, na=False)) | 
        (df['ZGH'].str.contains(query, na=False))
    ]
    
    # 2. 如果没有直接匹配，尝试寻找最近站点
    if filtered_df.empty:
        try:
            # 搜索地理坐标，限定在 GA 州
            location = geolocator.geocode(f"{query}, Georgia, USA")
            if location:
                search_lat, search_lon = location.latitude, location.longitude
                # 计算所有站点到搜索点的距离
                df['distance'] = df.apply(
                    lambda row: geodesic((search_lat, search_lon), (row['Lat'], row['Lon'])).miles, axis=1
                )
                # 取最近的 3 个站点
                filtered_df = df.sort_values('distance').head(3)
                is_recommendation = True
                st.sidebar.warning(f"未找到直接匹配。已为您推荐距离 {query} 最近的 3 个站点。")
        except Exception:
            st.sidebar.error("无法定位该位置，请尝试其他关键词。")
else:
    filtered_df = df

# --- 布局：地图与表格 ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📍 站点分布图")
    # 初始化地图中心
    center_lat = search_lat if search_lat else 32.8
    center_lon = search_lon if search_lon else -83.6
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    
    # 如果是搜索定位，标记搜索点
    if search_lat and search_lon:
        folium.Marker(
            [search_lat, search_lon],
            popup="搜索点",
            icon=folium.Icon(color="red", icon="search")
        ).add_to(m)

    # 标记站点
    for _, row in filtered_df.iterrows():
        color = "green" if is_recommendation else "blue"
        dist_info = f"<br>距离: {row['distance']:.1f} miles" if 'distance' in row else ""
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"ID: {row['ZGH']}<br>DAI: {row['DAI']}{dist_info}",
            tooltip=f"{row['DAI']} ({row['ZGH']})",
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    st_folium(m, width=700, height=500)

with col_right:
    st.subheader("📋 站点信息清单")
    display_cols = ['ZGH', 'DAI', 'County', 'Note']
    if 'distance' in filtered_df.columns:
        display_cols.append('distance')
    
    st.dataframe(filtered_df[display_cols], use_container_width=True)
    
    if is_recommendation:
        st.info("提示：绿色图标表示推荐的临近站点。")

    # 下载功能
    csv = df[['ZGH', 'DAI', 'County', 'Note']].to_csv(index=False).encode('utf-8')
    st.download_button("📥 下载完整站点表 (CSV)", data=csv, file_name='GA_DDS_Station_List.csv', mime='text/csv')
