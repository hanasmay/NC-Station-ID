import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# --- 1. 彻底更新的完整站点数据库 ---
# 确保这里包含 086 等全省 60 多个站点
full_site_data = [
    {"ZGH": "001", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.744, "Lon": -84.394, "Note": "Whitehall St"},
    {"ZGH": "002", "DAI": "ALBANY", "County": "DOUGHERTY", "Lat": 31.578, "Lon": -84.155, "Note": ""},
    {"ZGH": "003", "DAI": "CARTERSVILLE", "County": "BARTOW", "Lat": 34.165, "Lon": -84.796, "Note": ""},
    {"ZGH": "004", "DAI": "CARROLLTON", "County": "CARROLL", "Lat": 33.580, "Lon": -85.076, "Note": ""},
    {"ZGH": "005", "DAI": "ATHENS", "County": "CLARKE", "Lat": 33.951, "Lon": -83.357, "Note": ""},
    {"ZGH": "006", "DAI": "BLUE RIDGE", "County": "FANNIN", "Lat": 34.864, "Lon": -84.322, "Note": ""},
    {"ZGH": "007", "DAI": "COLUMBUS", "County": "MUSCOGEE", "Lat": 32.460, "Lon": -84.987, "Note": ""},
    {"ZGH": "008", "DAI": "BLAIRSVILLE", "County": "UNION", "Lat": 34.876, "Lon": -83.958, "Note": ""},
    {"ZGH": "010", "DAI": "BAINBRIDGE", "County": "DECATUR", "Lat": 30.903, "Lon": -84.575, "Note": ""},
    {"ZGH": "012", "DAI": "MACON", "County": "BIBB", "Lat": 32.840, "Lon": -83.632, "Note": ""},
    {"ZGH": "013", "DAI": "AMERICUS", "County": "SUMTER", "Lat": 32.072, "Lon": -84.232, "Note": ""},
    {"ZGH": "015", "DAI": "DECATUR", "County": "DEKALB", "Lat": 33.774, "Lon": -84.296, "Note": ""},
    {"ZGH": "016", "DAI": "BRUNSWICK", "County": "GLYNN", "Lat": 31.149, "Lon": -81.491, "Note": ""},
    {"ZGH": "017", "DAI": "CALHOUN", "County": "GORDON", "Lat": 34.502, "Lon": -84.951, "Note": ""},
    {"ZGH": "018", "DAI": "SAVANNAH", "County": "CHATHAM", "Lat": 32.083, "Lon": -81.099, "Note": ""},
    {"ZGH": "019", "DAI": "VALDOSTA", "County": "LOWNDES", "Lat": 30.832, "Lon": -83.278, "Note": ""},
    {"ZGH": "020", "DAI": "DOUGLAS", "County": "COFFEE", "Lat": 31.508, "Lon": -82.850, "Note": ""},
    {"ZGH": "021", "DAI": "GAINESVILLE", "County": "HALL", "Lat": 34.297, "Lon": -83.824, "Note": ""},
    {"ZGH": "022", "DAI": "MARIETTA", "County": "COBB", "Lat": 33.952, "Lon": -84.549, "Note": "Cobb Hub"},
    {"ZGH": "023", "DAI": "DALTON", "County": "WHITFIELD", "Lat": 34.769, "Lon": -84.970, "Note": ""},
    {"ZGH": "024", "DAI": "AUGUSTA", "County": "RICHMOND", "Lat": 33.470, "Lon": -81.974, "Note": ""},
    {"ZGH": "026", "DAI": "DUBLIN", "County": "LAURENS", "Lat": 32.540, "Lon": -82.903, "Note": ""},
    {"ZGH": "031", "DAI": "NORCROSS", "County": "GWINNETT", "Lat": 33.941, "Lon": -84.213, "Note": ""},
    {"ZGH": "033", "DAI": "LAWRENCEVILLE", "County": "GWINNETT", "Lat": 33.956, "Lon": -83.988, "Note": ""},
    {"ZGH": "037", "DAI": "CANTON", "County": "CHEROKEE", "Lat": 34.237, "Lon": -84.494, "Note": ""},
    {"ZGH": "041", "DAI": "CORDELE", "County": "CRISP", "Lat": 31.968, "Lon": -83.782, "Note": ""},
    {"ZGH": "043", "DAI": "CUMMING", "County": "FORSYTH", "Lat": 34.207, "Lon": -84.140, "Note": ""},
    {"ZGH": "044", "DAI": "CONYERS", "County": "ROCKDALE", "Lat": 33.667, "Lon": -84.017, "Note": ""},
    {"ZGH": "046", "DAI": "COVINGTON", "County": "NEWTON", "Lat": 33.596, "Lon": -83.860, "Note": ""},
    {"ZGH": "053", "DAI": "DALLAS", "County": "PAULDING", "Lat": 33.923, "Lon": -84.840, "Note": ""},
    {"ZGH": "054", "DAI": "SUWANEE", "County": "GWINNETT", "Lat": 34.051, "Lon": -84.062, "Note": ""},
    {"ZGH": "057", "DAI": "DOUGLASVILLE", "County": "DOUGLAS", "Lat": 33.751, "Lon": -84.747, "Note": ""},
    {"ZGH": "060", "DAI": "ELBERTON", "County": "ELBERT", "Lat": 34.111, "Lon": -82.867, "Note": ""},
    {"ZGH": "063", "DAI": "FOREST PARK", "County": "CLAYTON", "Lat": 33.622, "Lon": -84.368, "Note": ""},
    {"ZGH": "065", "DAI": "FITZGERALD", "County": "BEN HILL", "Lat": 31.714, "Lon": -83.254, "Note": ""},
    {"ZGH": "069", "DAI": "GRIFFIN", "County": "SPALDING", "Lat": 33.246, "Lon": -84.264, "Note": ""},
    {"ZGH": "073", "DAI": "GREENSBORO", "County": "GREENE", "Lat": 33.575, "Lon": -83.182, "Note": ""},
    {"ZGH": "074", "DAI": "HINESVILLE", "County": "LIBERTY", "Lat": 31.846, "Lon": -81.595, "Note": ""},
    {"ZGH": "077", "DAI": "JACKSON", "County": "BUTTS", "Lat": 33.294, "Lon": -83.966, "Note": ""},
    {"ZGH": "078", "DAI": "JESUP", "County": "WAYNE", "Lat": 31.607, "Lon": -81.885, "Note": ""},
    {"ZGH": "081", "DAI": "FAYETTEVILLE", "County": "FAYETTE", "Lat": 33.447, "Lon": -84.455, "Note": ""},
    {"ZGH": "082", "DAI": "LAGRANGE", "County": "TROUP", "Lat": 33.039, "Lon": -85.031, "Note": ""},
    {"ZGH": "083", "DAI": "LAFAYETTE", "County": "WALKER", "Lat": 34.704, "Lon": -85.289, "Note": ""},
    {"ZGH": "085", "DAI": "ALPHARETTA", "County": "FULTON", "Lat": 34.075, "Lon": -84.294, "Note": ""},
    # 核心修正点：确保 086 在这里
    {"ZGH": "086", "DAI": "ACWORTH", "County": "COBB", "Lat": 34.043, "Lon": -84.664, "Note": "Kennesaw Site"},
    {"ZGH": "087", "DAI": "KINGS BAY", "County": "CAMDEN", "Lat": 30.796, "Lon": -81.547, "Note": ""},
    {"ZGH": "089", "DAI": "LOUISVILLE", "County": "JEFFERSON", "Lat": 33.001, "Lon": -82.411, "Note": ""},
    {"ZGH": "091", "DAI": "LOCUST GROVE", "County": "HENRY", "Lat": 33.345, "Lon": -84.110, "Note": ""},
    {"ZGH": "093", "DAI": "MILLEDGEVILLE", "County": "BALDWIN", "Lat": 33.080, "Lon": -83.232, "Note": ""},
    {"ZGH": "094", "DAI": "MOULTRIE", "County": "COLQUITT", "Lat": 31.179, "Lon": -83.789, "Note": ""},
    {"ZGH": "095", "DAI": "METTER", "County": "CANDLER", "Lat": 32.397, "Lon": -82.062, "Note": ""},
    {"ZGH": "096", "DAI": "NEWNAN", "County": "COWETA", "Lat": 33.376, "Lon": -84.799, "Note": ""},
    {"ZGH": "100", "DAI": "ROME", "County": "FLOYD", "Lat": 34.257, "Lon": -85.164, "Note": ""},
    {"ZGH": "103", "DAI": "REIDSVILLE", "County": "TATTNALL", "Lat": 32.083, "Lon": -82.119, "Note": ""},
    {"ZGH": "105", "DAI": "ROCKMART", "County": "POLK", "Lat": 34.003, "Lon": -85.048, "Note": ""},
    {"ZGH": "109", "DAI": "SANDERSVILLE", "County": "WASHINGTON", "Lat": 32.981, "Lon": -82.810, "Note": ""},
    {"ZGH": "112", "DAI": "STATESBORO", "County": "BULLOCH", "Lat": 32.448, "Lon": -81.783, "Note": ""},
    {"ZGH": "114", "DAI": "SWAINSBORO", "County": "EMANUEL", "Lat": 32.597, "Lon": -82.333, "Note": ""},
    {"ZGH": "117", "DAI": "THOMASTON", "County": "UPSON", "Lat": 32.891, "Lon": -84.326, "Note": ""},
    {"ZGH": "118", "DAI": "THOMASVILLE", "County": "THOMAS", "Lat": 30.836, "Lon": -83.978, "Note": ""},
    {"ZGH": "119", "DAI": "TIFTON", "County": "TIFT", "Lat": 31.450, "Lon": -83.508, "Note": ""},
    {"ZGH": "120", "DAI": "TOCCOA", "County": "STEPHENS", "Lat": 34.577, "Lon": -83.332, "Note": ""},
    {"ZGH": "121", "DAI": "THOMSON", "County": "MCDUFFIE", "Lat": 33.470, "Lon": -82.504, "Note": ""},
    {"ZGH": "125", "DAI": "WAYCROSS", "County": "WARE", "Lat": 31.213, "Lon": -82.354, "Note": ""},
    {"ZGH": "126", "DAI": "WARNER ROBINS", "County": "HOUSTON", "Lat": 32.617, "Lon": -83.603, "Note": ""},
    {"ZGH": "127", "DAI": "WASHINGTON", "County": "WILKES", "Lat": 33.736, "Lon": -82.740, "Note": ""},
    {"ZGH": "130", "DAI": "WAYNESBORO", "County": "BURKE", "Lat": 33.090, "Lon": -82.015, "Note": ""},
    {"ZGH": "132", "DAI": "WINDER", "County": "BARROW", "Lat": 33.992, "Lon": -83.720, "Note": ""},
    {"ZGH": "137", "DAI": "ATLANTA", "County": "FULTON", "Lat": 33.716, "Lon": -84.350, "Note": "Moreland Ave"},
    {"ZGH": "143", "DAI": "SUGAR HILL", "County": "GWINNETT", "Lat": 34.120, "Lon": -84.040, "Note": "Latest Hub"},
]

# --- 2. 应用设置 ---
st.set_page_config(page_title="GA DDS 站点大全", layout="wide")

# 强制刷新 DataFrame
df = pd.DataFrame(full_site_data)
# 按代码排序，确保列表整齐
df = df.sort_values('ZGH').reset_index(drop=True)

st.title("🍑 佐治亚州 (GA) DDS 站点智能查询系统 (全省版)")
st.info(f"系统已加载全省共 {len(df)} 个官方站点数据。")

# --- 3. 搜索逻辑 ---
st.sidebar.header("🔍 站点搜索")
query = st.sidebar.text_input("搜索 ID、城市或县:").strip().upper()

search_lat, search_lon = None, None
is_recommendation = False

if query:
    # 模糊匹配
    filtered_df = df[
        (df['DAI'].str.contains(query, na=False)) | 
        (df['County'].str.contains(query, na=False)) | 
        (df['ZGH'].str.contains(query, na=False))
    ]
    
    # 如果没匹配到，尝试地理定位
    if filtered_df.empty:
        try:
            geolocator = Nominatim(user_agent="ga_dds_locator_v2")
            location = geolocator.geocode(f"{query}, Georgia, USA")
            if location:
                search_lat, search_lon = location.latitude, location.longitude
                df['distance'] = df.apply(
                    lambda row: geodesic((search_lat, search_lon), (row['Lat'], row['Lon'])).miles, axis=1
                )
                filtered_df = df.sort_values('distance').head(5)
                is_recommendation = True
                st.sidebar.warning(f"坐标定位：已显示距离 {query} 最近的 5 个站点。")
        except:
            st.sidebar.error("未找到相关信息，请检查拼写。")
else:
    filtered_df = df

# --- 4. 界面展示 ---
col_map, col_table = st.columns([1.6, 1])

with col_map:
    st.subheader("📍 站点分布图")
    # 地图中心动态调整
    c_lat = search_lat if search_lat else 32.8
    c_lon = search_lon if search_lon else -83.6
    
    m = folium.Map(location=[c_lat, c_lon], zoom_start=7)
    
    for _, row in filtered_df.iterrows():
        color = "green" if is_recommendation else "blue"
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"ID: {row['ZGH']}<br>City: {row['DAI']}<br>County: {row['County']}",
            tooltip=f"{row['DAI']} ({row['ZGH']})",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)
    
    st_folium(m, width="100%", height=600)

with col_table:
    st.subheader(f"📋 结果详情 ({len(filtered_df)} 条)")
    cols = ['ZGH', 'DAI', 'County', 'Note']
    if 'distance' in filtered_df.columns:
        cols.append('distance')
        
    st.dataframe(filtered_df[cols], use_container_width=True, height=550)

    # 导出
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 导出完整 60+ 站点清单",
        data=csv,
        file_name='GA_Full_DDS_List.csv',
        mime='text/csv',
    )
