"""
DASHBOARD - MOVIMIENTO DE INVENTARIO 2025
Análisis de ventas por zona, canal y clasificación
Para: Gerencia General
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Movimiento de Inventario 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de colores profesional
COLORS = {
    'primary': '#1a1a2e',
    'secondary': '#16213e',
    'accent': '#0f3460',
    'highlight': '#e94560',
    'success': '#00bf63',
    'warning': '#ff6b35',
    'info': '#4361ee',
    'light': '#f8f9fa',
    'muted': '#6c757d'
}

# Colores por canal
CANAL_COLORS = {
    'MINORISTA': '#4361ee',
    'INTEGRADOR': '#7209b7',
    'OPERADORES': '#f72585',
    'RETAIL': '#4cc9f0'
}

# Estilos CSS profesionales mejorados
st.markdown(f"""
<style>
    .main {{ background-color: #FAFBFC; }}
    
    .main-header {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['primary']};
        padding: 0.5rem 0;
        margin-bottom: 0.5rem;
    }}
    
    .subtitle {{
        font-size: 1.1rem;
        color: {COLORS['muted']};
        margin-bottom: 2rem;
    }}
    
    .insight-box {{
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        border-left: 5px solid {COLORS['accent']};
        margin: 1.5rem 0;
        font-size: 0.95rem;
        color: #495057;
        line-height: 1.7;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .insight-box-highlight {{
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        border-left: 5px solid {COLORS['warning']};
        margin: 1.5rem 0;
        font-size: 0.95rem;
        color: #495057;
        line-height: 1.7;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .insight-box-success {{
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        border-left: 5px solid {COLORS['success']};
        margin: 1.5rem 0;
        font-size: 0.95rem;
        color: #495057;
        line-height: 1.7;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .metric-box {{
        background-color: #fff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .section-title {{
        font-size: 1.4rem;
        font-weight: 600;
        color: {COLORS['primary']};
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid {COLORS['accent']};
    }}
    
    .story-number {{
        font-size: 3rem;
        font-weight: 700;
        color: {COLORS['highlight']};
        line-height: 1;
    }}
    
    .story-label {{
        font-size: 0.9rem;
        color: {COLORS['muted']};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .callout {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }}
    
    .callout h4 {{
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARGA Y PROCESAMIENTO DE DATOS
# ============================================================================
@st.cache_data
def cargar_datos():
    df = pd.read_csv('sku_canal_zonas_usd.csv', sep=';', encoding='utf-8-sig')
    
    # Solo meses de 2025 (sin enero 2026)
    meses = ['Ene-25', 'Feb-25', 'Mar-25', 'Abr-25', 'May-25', 'Jun-25', 
             'Jul-25', 'Ago-25', 'Set-25', 'Oct-25', 'Nov-25', 'Dic-25']
    
    for mes in meses:
        df[mes] = df[mes].astype(str).str.replace(',', '').astype(float)
    
    df['TOTAL_2025'] = df[meses].sum(axis=1)
    
    # Calcular meses antes y después del cambio de almacén (Agosto 2025)
    meses_antes = ['Ene-25', 'Feb-25', 'Mar-25', 'Abr-25', 'May-25', 'Jun-25', 'Jul-25']
    meses_despues = ['Ago-25', 'Set-25', 'Oct-25', 'Nov-25', 'Dic-25']
    
    df['VENTA_ANTES_CAMBIO'] = df[meses_antes].sum(axis=1)
    df['VENTA_DESPUES_CAMBIO'] = df[meses_despues].sum(axis=1)
    
    return df, meses

df, meses = cargar_datos()

# ============================================================================
# HEADER CON CONTEXTO
# ============================================================================
st.markdown('<p class="main-header">📊 Movimiento de Inventario 2025</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Análisis estratégico de ventas por zona geográfica, canal de distribución y clasificación de productos</p>', unsafe_allow_html=True)

# Contexto inicial - Story hook
st.markdown(f"""
<div class="callout">
<h4>🔍 Contexto del Análisis</h4>
En <b>Agosto 2025</b>, el centro de distribución se trasladó de <b>San Luis</b> (cerca al centro de Lima) a <b>Lurín</b> (extremo sur). 
Este cambio impacta directamente los tiempos de entrega y la capacidad operativa hacia las zonas comerciales del centro de Lima.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# COMPOSICIÓN DEL PORTAFOLIO
# ============================================================================
st.markdown('<p class="section-title">📦 Composición del Portafolio</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="metric-box" style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
        <tr style="border-bottom: 2px solid #1a1a2e;">
            <th style="text-align: left; padding: 8px 0; color: #1a1a2e;">Clasificación</th>
            <th style="text-align: right; padding: 8px 0; color: #1a1a2e;">SKUs</th>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #e94560;">●</span> <b>S</b> — Alta contribución (50%)</td>
            <td style="text-align: right; padding: 6px 0;">121</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #f72585;">●</span> <b>A</b> — Contribución significativa (30%)</td>
            <td style="text-align: right; padding: 6px 0;">273</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #7209b7;">●</span> <b>B</b> — Contribución moderada (15%)</td>
            <td style="text-align: right; padding: 6px 0;">430</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #4361ee;">●</span> <b>C</b> — Baja contribución (4%)</td>
            <td style="text-align: right; padding: 6px 0;">334</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #4cc9f0;">●</span> <b>T</b> — Cola larga (1%)</td>
            <td style="text-align: right; padding: 6px 0;">815</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #00bf63;">●</span> <b>Nuevo</b> — Menos de 6 meses</td>
            <td style="text-align: right; padding: 6px 0;">305</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #ff6b35;">●</span> <b>Gestión</b> — Seguimiento especial</td>
            <td style="text-align: right; padding: 6px 0;">271</td>
        </tr>
        <tr style="border-bottom: 1px solid #e9ecef;">
            <td style="padding: 6px 0;"><span style="color: #6c757d;">●</span> <b>Obsoleto</b> — Baja rotación</td>
            <td style="text-align: right; padding: 6px 0;">6,296</td>
        </tr>
        <tr style="background-color: #1a1a2e; color: white;">
            <td style="padding: 8px 0; font-weight: 600;">Total Portafolio</td>
            <td style="text-align: right; padding: 8px 0; font-weight: 600;">8,850</td>
        </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box">
    <strong>📐 Metodología de Clasificación SABCT</strong><br><br>
    La clasificación SABCT segmenta el portafolio según su contribución al negocio:
    <br><br>
    <b>🎯 Productos Estratégicos (S+A+B):</b> Representan el 95% de la facturación con solo 824 SKUs (9.3% del portafolio). Son el foco principal de disponibilidad y servicio.
    <br><br>
    <b>📊 Cola Larga (C+T):</b> 1,149 SKUs que complementan la oferta y atienden necesidades específicas de nicho.
    <br><br>
    <b>⚙️ Gestión Especial:</b> Productos nuevos en evaluación, artículos en seguimiento comercial y obsoletos pendientes de liquidación.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box-highlight">
    <strong>⚠️ Oportunidad Identificada:</strong> El alto volumen de productos obsoletos (<b>6,296 SKUs</b> = 71% del portafolio) representa capital inmovilizado y espacio de almacenamiento que podría liberarse para productos de mayor rotación.
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# COBERTURA GEOGRÁFICA - COMPARATIVA SAN LUIS vs LURÍN
# ============================================================================
st.markdown('<p class="section-title">🗺️ Impacto del Cambio de Almacén en Tiempos de Entrega</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<strong>📍 Contexto del cambio:</strong> En Agosto 2025, el centro de distribución se trasladó de <b>San Luis</b> (centro-este de Lima) 
a <b>Lurín</b> (extremo sur). Esta comparativa muestra el impacto en los tiempos de entrega hacia las principales zonas comerciales.
</div>
""", unsafe_allow_html=True)

# Coordenadas de ambos almacenes
san_luis = {"lat": -12.070136596787389, "lon": -76.99200082864617, "nombre": "CD San Luis"}
lurin = {"lat": -12.269444, "lon": -76.890889, "nombre": "CD Lurín"}

# Zonas de destino con tiempos desde ambos almacenes
zonas = {
    "Wilson": {"lat": -12.054828666634194, "lon": -77.03806428818251, 
               "tiempo_sanluis": "20min", "km_sanluis": "5",
               "tiempo_lurin": "1h 20min", "km_lurin": "32"},
    "Paruro": {"lat": -12.05042038678001, "lon": -77.02406775564982, 
               "tiempo_sanluis": "18min", "km_sanluis": "4",
               "tiempo_lurin": "1h 25min", "km_lurin": "33"},
    "Malvinas": {"lat": -12.043337534371508, "lon": -77.04817089428148, 
                 "tiempo_sanluis": "25min", "km_sanluis": "6",
                 "tiempo_lurin": "1h 30min", "km_lurin": "35"},
    "Azángaro": {"lat": -12.051654779770855, "lon": -77.03062129243266, 
                 "tiempo_sanluis": "18min", "km_sanluis": "4",
                 "tiempo_lurin": "1h 25min", "km_lurin": "33"},
    "CompuPalace": {"lat": -12.116443820363907, "lon": -77.02803893901076, 
                    "tiempo_sanluis": "15min", "km_sanluis": "6",
                    "tiempo_lurin": "50min", "km_lurin": "22"},
    "Marsano": {"lat": -12.117517551566221, "lon": -77.00740718503695, 
                "tiempo_sanluis": "12min", "km_sanluis": "5",
                "tiempo_lurin": "45min", "km_lurin": "20"}
}

# Colores por zona
colores_zona = {
    "Wilson": "#e94560",
    "Paruro": "#4361ee", 
    "Malvinas": "#00bf63",
    "Azángaro": "#7209b7",
    "CompuPalace": "#ff6b35",
    "Marsano": "#4cc9f0"
}

# Crear dos mapas lado a lado
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #00bf63 0%, #2ecc71 100%); color: white; border-radius: 8px 8px 0 0; font-weight: 600;">
    ✅ ANTES: San Luis (Ene-Jul 2025)
    </div>
    """, unsafe_allow_html=True)
    
    fig_sanluis = go.Figure()
    
    # Rutas desde San Luis
    for zona, coords in zonas.items():
        fig_sanluis.add_trace(go.Scattermapbox(
            lat=[san_luis["lat"], coords["lat"]],
            lon=[san_luis["lon"], coords["lon"]],
            mode='lines',
            line=dict(width=3, color=colores_zona[zona]),
            name=f'{zona} ({coords["tiempo_sanluis"]})',
            hoverinfo='text',
            hovertext=f'Ruta a {zona}<br>Distancia: {coords["km_sanluis"]} km<br>Tiempo: {coords["tiempo_sanluis"]}'
        ))
    
    # Marcador San Luis
    fig_sanluis.add_trace(go.Scattermapbox(
        lat=[san_luis["lat"]],
        lon=[san_luis["lon"]],
        mode='markers',
        marker=dict(size=20, color='#00bf63', symbol='circle'),
        name='CD San Luis',
        hoverinfo='text',
        hovertext='<b>CD San Luis</b><br>Jr. Salaverry 161<br><i>Operó hasta Jul 2025</i>'
    ))
    
    # Marcadores de zonas
    for zona, coords in zonas.items():
        fig_sanluis.add_trace(go.Scattermapbox(
            lat=[coords["lat"]],
            lon=[coords["lon"]],
            mode='markers',
            marker=dict(size=12, color=colores_zona[zona]),
            hoverinfo='text',
            hovertext=f'<b>{zona}</b><br>Tiempo: {coords["tiempo_sanluis"]}',
            showlegend=False
        ))
    
    fig_sanluis.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=-12.08, lon=-77.01), zoom=11.5),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=9)),
        showlegend=True
    )
    
    st.plotly_chart(fig_sanluis, use_container_width=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%); color: white; border-radius: 8px 8px 0 0; font-weight: 600;">
    ⚠️ AHORA: Lurín (Ago-Dic 2025)
    </div>
    """, unsafe_allow_html=True)
    
    fig_lurin = go.Figure()
    
    # Rutas desde Lurín
    for zona, coords in zonas.items():
        fig_lurin.add_trace(go.Scattermapbox(
            lat=[lurin["lat"], coords["lat"]],
            lon=[lurin["lon"], coords["lon"]],
            mode='lines',
            line=dict(width=3, color=colores_zona[zona]),
            name=f'{zona} ({coords["tiempo_lurin"]})',
            hoverinfo='text',
            hovertext=f'Ruta a {zona}<br>Distancia: {coords["km_lurin"]} km<br>Tiempo: {coords["tiempo_lurin"]}'
        ))
    
    # Marcador Lurín
    fig_lurin.add_trace(go.Scattermapbox(
        lat=[lurin["lat"]],
        lon=[lurin["lon"]],
        mode='markers',
        marker=dict(size=20, color='#e94560', symbol='circle'),
        name='CD Lurín',
        hoverinfo='text',
        hovertext='<b>CD Lurín</b><br>Km 29.5 Panamericana Sur<br><i>Opera desde Ago 2025</i>'
    ))
    
    # Marcadores de zonas
    for zona, coords in zonas.items():
        fig_lurin.add_trace(go.Scattermapbox(
            lat=[coords["lat"]],
            lon=[coords["lon"]],
            mode='markers',
            marker=dict(size=12, color=colores_zona[zona]),
            hoverinfo='text',
            hovertext=f'<b>{zona}</b><br>Tiempo: {coords["tiempo_lurin"]}',
            showlegend=False
        ))
    
    fig_lurin.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=-12.15, lon=-76.97), zoom=10.2),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=9)),
        showlegend=True
    )
    
    st.plotly_chart(fig_lurin, use_container_width=True)

# Tabla comparativa de tiempos
st.markdown("#### ⏱️ Comparativa de Tiempos de Entrega")

col1, col2, col3 = st.columns([1.2, 1.2, 0.8])

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['success']} 0%, #2ecc71 100%); color: white; padding: 1.2rem; border-radius: 10px;">
        <h4 style="margin: 0 0 0.8rem 0; font-size: 0.95rem; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 0.5rem;">✅ Desde San Luis</h4>
        <div style="font-size: 0.85rem; line-height: 2;">
            <div style="display: flex; justify-content: space-between;"><span>🔴 Wilson</span><span><b>20 min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🔵 Paruro</span><span><b>18 min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🟢 Malvinas</span><span><b>25 min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🟣 Azángaro</span><span><b>18 min</b></span></div>
            <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 6px; margin-top: 6px;"><span>🟠 CompuPalace</span><span><b>15 min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🔵 Marsano</span><span><b>12 min</b></span></div>
        </div>
        <div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.3); font-size: 0.9rem;">
            <b>Promedio: ~18 min</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['highlight']} 0%, #ff6b6b 100%); color: white; padding: 1.2rem; border-radius: 10px;">
        <h4 style="margin: 0 0 0.8rem 0; font-size: 0.95rem; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 0.5rem;">⚠️ Desde Lurín</h4>
        <div style="font-size: 0.85rem; line-height: 2;">
            <div style="display: flex; justify-content: space-between;"><span>🔴 Wilson</span><span><b>1h 20min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🔵 Paruro</span><span><b>1h 25min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🟢 Malvinas</span><span><b>1h 30min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🟣 Azángaro</span><span><b>1h 25min</b></span></div>
            <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 6px; margin-top: 6px;"><span>🟠 CompuPalace</span><span><b>50 min</b></span></div>
            <div style="display: flex; justify-content: space-between;"><span>🔵 Marsano</span><span><b>45 min</b></span></div>
        </div>
        <div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.3); font-size: 0.9rem;">
            <b>Promedio: ~1h 06min</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); color: white; padding: 1.2rem; border-radius: 10px; text-align: center;">
        <h4 style="margin: 0 0 1rem 0; font-size: 0.95rem;">📊 Incremento</h4>
        <div style="font-size: 2.5rem; font-weight: 700; color: #ffd93d;">+267%</div>
        <div style="font-size: 0.85rem; opacity: 0.9; margin-top: 0.5rem;">en tiempo<br>promedio</div>
        <div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid rgba(255,255,255,0.3); font-size: 0.8rem;">
            De <b>18 min</b><br>a <b>1h 06min</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Calcular métricas por zona del mapa para el insight
zonas_mapa = ['WILSON', 'PARURO', 'MALVINAS', 'AZANGARO', 'COMPUPALACE', 'MARSANO']
zonas_data = []
total_ventas_zonas = df[df['ZONA_CONSOLIDADO'].isin(zonas_mapa)]['TOTAL_2025'].sum()

for zona in zonas_mapa:
    df_zona = df[df['ZONA_CONSOLIDADO'] == zona]
    skus = df_zona['ARTICULO'].nunique()
    venta = df_zona['TOTAL_2025'].sum()
    pct_contribucion = (venta / total_ventas_zonas * 100) if total_ventas_zonas > 0 else 0
    zonas_data.append({'skus': skus, 'venta': venta, 'pct': pct_contribucion})

# Calcular total de las 4 zonas críticas del centro
venta_centro = sum([zonas_data[i]['venta'] for i in range(4)])
pct_centro = sum([zonas_data[i]['pct'] for i in range(4)])

st.markdown(f"""
<div class="insight-box-highlight">
<strong>🚨 Impacto Operativo del Cambio:</strong><br><br>
• <b>Tiempo promedio de entrega aumentó 267%</b> (de 18 min a 1h 06min en promedio)<br><br>
• Las zonas del <b>centro de Lima</b> (Wilson, Paruro, Malvinas, Azángaro) pasaron de <b>~20 min</b> a <b>+1h 20min</b><br><br>
• Estas 4 zonas concentran <b>{pct_centro:.1f}%</b> de las ventas (${venta_centro/1000:,.0f}K) y operan <b>100% canal MINORISTA</b><br><br>
• <b>Capacidad de entrega reducida:</b> Antes se podían hacer 6-8 ciclos/día, ahora máximo 2-3 ciclos/día hacia el centro
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INDICADORES PRINCIPALES 2025
# ============================================================================
st.markdown('<p class="section-title">📈 Indicadores de Venta 2025</p>', unsafe_allow_html=True)

# Cálculos
total_2025 = df['TOTAL_2025'].sum()
promedio_mensual = total_2025 / 12
skus_con_venta = df[df['TOTAL_2025'] > 0]['ARTICULO'].nunique()
skus_totales = df['ARTICULO'].nunique()

# Métricas principales con diseño mejorado
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box" style="text-align: center; padding: 1.5rem;">
        <p class="story-label">Venta Total 2025</p>
        <p class="story-number">${total_2025/1000000:.1f}M</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box" style="text-align: center; padding: 1.5rem;">
        <p class="story-label">Promedio Mensual</p>
        <p class="story-number">${promedio_mensual/1000:.0f}K</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box" style="text-align: center; padding: 1.5rem;">
        <p class="story-label">SKUs con Movimiento</p>
        <p class="story-number">{skus_con_venta:,}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pct_activos = (skus_con_venta / skus_totales) * 100
    st.markdown(f"""
    <div class="metric-box" style="text-align: center; padding: 1.5rem;">
        <p class="story-label">% SKUs Activos</p>
        <p class="story-number">{pct_activos:.0f}%</p>
    </div>
    """, unsafe_allow_html=True)

# Evolución mensual con anotaciones
st.markdown("#### 📊 Evolución Mensual de Ventas")

ventas_mensuales = df[meses].sum()
df_mensual = pd.DataFrame({
    'Mes': meses,
    'Ventas': ventas_mensuales.values
})

fig_linea = go.Figure()

# Área de fondo para período pre-cambio
fig_linea.add_vrect(
    x0=-0.5, x1=6.5,
    fillcolor="rgba(0, 191, 99, 0.1)",
    layer="below",
    line_width=0,
)

# Área de fondo para período post-cambio
fig_linea.add_vrect(
    x0=6.5, x1=11.5,
    fillcolor="rgba(233, 69, 96, 0.1)",
    layer="below",
    line_width=0,
)

fig_linea.add_trace(go.Scatter(
    x=df_mensual['Mes'], 
    y=df_mensual['Ventas'],
    mode='lines+markers',
    name='Ventas 2025',
    line=dict(color=COLORS['primary'], width=3, shape='spline', smoothing=1.3),
    marker=dict(size=10, color=COLORS['primary'], line=dict(width=2, color='white')),
    fill='tozeroy',
    fillcolor='rgba(26, 26, 46, 0.1)'
))

# Línea vertical para el cambio de almacén
fig_linea.add_vline(x=7, line_dash="dash", line_color=COLORS['highlight'], line_width=2,
                     annotation_text="📦 Cambio a Lurín", annotation_position="top",
                     annotation_font=dict(size=11, color=COLORS['highlight']))

fig_linea.add_hline(y=promedio_mensual, line_dash="dot", line_color=COLORS['muted'], line_width=1,
                     annotation_text=f"Promedio: ${promedio_mensual:,.0f}", annotation_position="right")

# Anotaciones para meses clave
mes_max_idx = df_mensual['Ventas'].idxmax()
mes_min_idx = df_mensual['Ventas'].idxmin()

fig_linea.add_annotation(
    x=meses[mes_max_idx], y=df_mensual['Ventas'].max(),
    text=f"🏆 Máximo<br>${df_mensual['Ventas'].max()/1000:,.0f}K",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
    arrowcolor=COLORS['success'], font=dict(size=10, color=COLORS['success']),
    ax=0, ay=-40
)

fig_linea.add_annotation(
    x=meses[mes_min_idx], y=df_mensual['Ventas'].min(),
    text=f"📉 Mínimo<br>${df_mensual['Ventas'].min()/1000:,.0f}K",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
    arrowcolor=COLORS['highlight'], font=dict(size=10, color=COLORS['highlight']),
    ax=0, ay=40
)

fig_linea.update_layout(
    height=400,
    yaxis_title="Ventas (USD)",
    xaxis_title="",
    yaxis_tickformat="$,.0f",
    margin=dict(l=60, r=20, t=40, b=40),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False
)
fig_linea.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
fig_linea.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

st.plotly_chart(fig_linea, use_container_width=True)

# Insight sobre el cambio
venta_antes = df['VENTA_ANTES_CAMBIO'].sum()
venta_despues = df['VENTA_DESPUES_CAMBIO'].sum()
promedio_antes = venta_antes / 7
promedio_despues = venta_despues / 5
variacion = ((promedio_despues / promedio_antes) - 1) * 100

if variacion < 0:
    st.markdown(f"""
    <div class="insight-box-highlight">
    <strong>📊 Impacto del Cambio de Almacén:</strong> El promedio mensual <b>antes del cambio</b> (Ene-Jul) fue de <b>${promedio_antes:,.0f}</b>, mientras que <b>después del cambio</b> (Ago-Dic) bajó a <b>${promedio_despues:,.0f}</b>. Esto representa una <b>reducción del {abs(variacion):.1f}%</b> que podría estar relacionada con la mayor distancia a las zonas comerciales del centro.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="insight-box-success">
    <strong>📊 Impacto del Cambio de Almacén:</strong> A pesar del cambio de ubicación, el promedio mensual se mantuvo estable. Antes: <b>${promedio_antes:,.0f}</b> vs Después: <b>${promedio_despues:,.0f}</b> ({variacion:+.1f}%).
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ANÁLISIS POR CANAL
# ============================================================================
st.markdown('<p class="section-title">🏪 Distribución por Canal de Venta</p>', unsafe_allow_html=True)

canal_analysis = df.groupby('CANAL').agg({
    'TOTAL_2025': 'sum',
    'ARTICULO': 'nunique'
}).reset_index()

canal_analysis.columns = ['CANAL', 'VENTA_2025', 'SKUs']
canal_analysis['PROMEDIO_MENSUAL'] = canal_analysis['VENTA_2025'] / 12
canal_analysis['PARTICIPACION'] = (canal_analysis['VENTA_2025'] / canal_analysis['VENTA_2025'].sum()) * 100
canal_analysis = canal_analysis.sort_values('VENTA_2025', ascending=False)

col1, col2 = st.columns([1.2, 0.8])

with col1:
    # Donut chart más visual
    fig_donut = go.Figure(data=[go.Pie(
        labels=canal_analysis['CANAL'],
        values=canal_analysis['VENTA_2025'],
        hole=0.6,
        marker=dict(colors=[CANAL_COLORS.get(c, '#999') for c in canal_analysis['CANAL']]),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>Venta: $%{value:,.0f}<br>Participación: %{percent}<extra></extra>"
    )])
    
    fig_donut.add_annotation(
        text=f"<b>${total_2025/1000000:.1f}M</b><br><span style='font-size:12px'>Total 2025</span>",
        x=0.5, y=0.5, font=dict(size=20, color=COLORS['primary']), showarrow=False
    )
    
    fig_donut.update_layout(
        height=350,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=20, b=60)
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    st.markdown("#### Detalle por Canal")
    for _, row in canal_analysis.iterrows():
        color = CANAL_COLORS.get(row['CANAL'], '#999')
        st.markdown(f"""
        <div style="background: white; padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {color}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: {color};">{row['CANAL']}</span>
                <span style="font-size: 0.85rem; color: #6c757d;">{row['PARTICIPACION']:.1f}%</span>
            </div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #1a1a2e;">${row['VENTA_2025']/1000:,.0f}K</div>
            <div style="font-size: 0.8rem; color: #6c757d;">{row['SKUs']} SKUs activos</div>
        </div>
        """, unsafe_allow_html=True)

participacion_minorista = canal_analysis[canal_analysis['CANAL'] == 'MINORISTA']['PARTICIPACION'].values[0]
st.markdown(f"""
<div class="insight-box">
<strong>🎯 Concentración de ventas:</strong> El canal <b>MINORISTA</b> representa el <b>{participacion_minorista:.1f}%</b> de las ventas totales, lo que indica alta dependencia de este segmento. Los canales <b>INTEGRADOR</b> y <b>OPERADORES</b> ofrecen oportunidades de diversificación con potencial de mayor margen en proyectos especializados.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# ANÁLISIS SABCT POR CANAL - NUEVO DISEÑO DIDÁCTICO
# ============================================================================
st.markdown('<p class="section-title">🧩 Composición SABCT por Canal de Venta</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<strong>📖 ¿Qué nos dice este análisis?</strong> Cada canal de venta tiene una "personalidad" diferente según el tipo de productos que mueve. 
Entender esta composición ayuda a definir estrategias de inventario y servicio diferenciadas.
</div>
""", unsafe_allow_html=True)

# Filtrar solo clasificaciones activas (excluir Obsoleto y Gestión)
sabct_activos = ['S', 'A', 'B', 'C', 'T', 'Nuevo']
df_sabct_canal = df[df['SABCT'].isin(sabct_activos)]

# Colores SABCT
SABCT_COLORS = {
    'S': '#e94560',
    'A': '#f72585', 
    'B': '#7209b7',
    'C': '#4361ee',
    'T': '#4cc9f0',
    'Nuevo': '#00bf63'
}

# Tabla 1: Recuento de SKUs por Canal y SABCT
pivot_skus = df_sabct_canal.groupby(['CANAL', 'SABCT'])['ARTICULO'].nunique().unstack(fill_value=0)
pivot_skus = pivot_skus.reindex(columns=['S', 'A', 'B', 'C', 'T', 'Nuevo'], fill_value=0)
pivot_skus['Total'] = pivot_skus.sum(axis=1)

# Tabla 2: Participación de cada canal en cada clasificación SABCT
totales_sabct = df_sabct_canal.groupby('SABCT')['ARTICULO'].nunique()
pivot_participacion = pivot_skus.copy()
for col in ['S', 'A', 'B', 'C', 'T', 'Nuevo']:
    if col in totales_sabct.index and totales_sabct[col] > 0:
        pivot_participacion[col] = (pivot_skus[col] / totales_sabct[col] * 100).round(0).astype(int)
    else:
        pivot_participacion[col] = 0

# Gráfico de Treemap - Más didáctico que barras apiladas
st.markdown("#### 🗺️ Mapa de Composición: ¿Dónde están los productos?")

# Preparar datos para treemap
treemap_data = []
for canal in ['MINORISTA', 'INTEGRADOR', 'OPERADORES', 'RETAIL']:
    if canal in pivot_skus.index:
        for sabct in ['S', 'A', 'B', 'C', 'T', 'Nuevo']:
            if pivot_skus.loc[canal, sabct] > 0:
                treemap_data.append({
                    'Canal': canal,
                    'SABCT': sabct,
                    'SKUs': pivot_skus.loc[canal, sabct],
                    'Label': f"{sabct}"
                })

df_treemap = pd.DataFrame(treemap_data)

fig_treemap = px.treemap(
    df_treemap,
    path=['Canal', 'SABCT'],
    values='SKUs',
    color='Canal',
    color_discrete_map=CANAL_COLORS,
    hover_data={'SKUs': True}
)

fig_treemap.update_traces(
    textinfo="label+value",
    textfont=dict(size=14),
    hovertemplate="<b>%{label}</b><br>SKUs: %{value}<extra></extra>"
)

fig_treemap.update_layout(
    height=450,
    margin=dict(l=10, r=10, t=30, b=10)
)

st.plotly_chart(fig_treemap, use_container_width=True)

# Tablas lado a lado
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Cantidad de SKUs")
    # Estilizar tabla
    styled_skus = pivot_skus.style.background_gradient(cmap='Blues', subset=['S', 'A', 'B', 'C', 'T', 'Nuevo'])
    st.dataframe(pivot_skus, use_container_width=True)

with col2:
    st.markdown("#### 📈 Participación del Canal en cada SABCT")
    pivot_part_display = pivot_participacion[['S', 'A', 'B', 'C', 'T', 'Nuevo']].copy()
    pivot_part_display = pivot_part_display.applymap(lambda x: f"{x}%")
    st.dataframe(pivot_part_display, use_container_width=True)

# Gráfico radar para comparar perfiles
st.markdown("#### 🎯 Perfil de cada Canal")

canales_order = ['MINORISTA', 'INTEGRADOR', 'OPERADORES', 'RETAIL']
fig_radar = go.Figure()

for canal in canales_order:
    if canal in pivot_participacion.index:
        valores = [pivot_participacion.loc[canal, col] for col in ['S', 'A', 'B', 'C', 'T', 'Nuevo']]
        valores.append(valores[0])  # Cerrar el polígono
        
        fig_radar.add_trace(go.Scatterpolar(
            r=valores,
            theta=['S', 'A', 'B', 'C', 'T', 'Nuevo', 'S'],
            fill='toself',
            fillcolor=f"rgba{tuple(list(int(CANAL_COLORS[canal].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}",
            line=dict(color=CANAL_COLORS[canal], width=2),
            name=canal
        ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 70]),
        angularaxis=dict(tickfont=dict(size=12))
    ),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    height=400,
    margin=dict(l=60, r=60, t=40, b=60)
)

st.plotly_chart(fig_radar, use_container_width=True)

# Insights
part_minorista_nuevos = pivot_participacion.loc['MINORISTA', 'Nuevo'] if 'MINORISTA' in pivot_participacion.index else 0
part_minorista_a = pivot_participacion.loc['MINORISTA', 'A'] if 'MINORISTA' in pivot_participacion.index else 0

st.markdown(f"""
<div class="insight-box-success">
<strong>💡 Hallazgos Clave:</strong><br><br>
• <b>MINORISTA es el motor de innovación:</b> Concentra el <b>{part_minorista_nuevos}%</b> de productos Nuevos, siendo el canal de prueba para nuevos lanzamientos.<br><br>
• <b>INTEGRADOR apuesta por valor:</b> Mayor participación relativa en productos S (alta contribución), enfocándose en proyectos de alto impacto.<br><br>
• <b>RETAIL es nicho:</b> Participación marginal (1-4%) sugiere ser un canal complementario, no prioritario.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# NUEVA SECCIÓN: ANÁLISIS ZONA vs CANAL
# ============================================================================
st.markdown('<p class="section-title">🌍 Rendimiento por Zona y Canal</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<strong>📖 ¿Por qué es importante?</strong> Este cruce nos permite identificar qué zonas geográficas son más fuertes en cada canal, 
optimizar rutas de distribución y detectar oportunidades de crecimiento territorial.
</div>
""", unsafe_allow_html=True)

# Calcular métricas por zona y canal
zona_canal = df.groupby(['ZONA_CONSOLIDADO', 'CANAL']).agg({
    'ARTICULO': 'nunique',  # Pedidos promedio (aproximación por SKUs únicos)
    'TOTAL_2025': 'sum'     # Venta total
}).reset_index()

zona_canal.columns = ['ZONA', 'CANAL', 'PEDIDOS_PROMEDIO', 'VENTA_2025']

# Crear tabla pivote
pivot_pedidos = zona_canal.pivot_table(index='ZONA', columns='CANAL', values='PEDIDOS_PROMEDIO', aggfunc='sum', fill_value=0)
pivot_ventas = zona_canal.pivot_table(index='ZONA', columns='CANAL', values='VENTA_2025', aggfunc='sum', fill_value=0)

# Agregar totales
pivot_pedidos['Total'] = pivot_pedidos.sum(axis=1)
pivot_ventas['Total'] = pivot_ventas.sum(axis=1)

# Ordenar por venta total
pivot_ventas = pivot_ventas.sort_values('Total', ascending=False)
pivot_pedidos = pivot_pedidos.loc[pivot_ventas.index]

# Visualización: Heatmap de ventas por zona y canal
st.markdown("#### 🔥 Mapa de Calor: Ventas por Zona y Canal")

# Preparar datos para heatmap (sin columna Total para mejor visualización)
canales_heatmap = ['INTEGRADOR', 'MINORISTA', 'OPERADORES', 'RETAIL']
zonas_top = pivot_ventas.head(10).index.tolist()

heatmap_values = pivot_ventas.loc[zonas_top, canales_heatmap].values

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_values,
    x=canales_heatmap,
    y=zonas_top,
    colorscale='Blues',
    text=[[f"${val/1000:,.0f}K" if val > 0 else "-" for val in row] for row in heatmap_values],
    texttemplate="%{text}",
    textfont=dict(size=11),
    hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>Venta: $%{z:,.0f}<extra></extra>",
    colorbar=dict(title="Venta USD", tickformat="$,.0f")
))

# Agregar anotaciones para valores destacados
max_val = heatmap_values.max()
for i, zona in enumerate(zonas_top):
    for j, canal in enumerate(canales_heatmap):
        val = heatmap_values[i][j]
        if val == max_val:
            fig_heatmap.add_annotation(
                x=canal, y=zona,
                text="⭐",
                showarrow=False,
                font=dict(size=16)
            )

fig_heatmap.update_layout(
    height=450,
    xaxis_title="Canal de Venta",
    yaxis_title="",
    margin=dict(l=120, r=20, t=30, b=60),
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# Tablas detalladas
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📦 SKUs Únicos por Zona y Canal")
    pivot_pedidos_display = pivot_pedidos.copy()
    pivot_pedidos_display = pivot_pedidos_display.astype(int)
    st.dataframe(pivot_pedidos_display, use_container_width=True, height=400)

with col2:
    st.markdown("#### 💰 Venta 2025 por Zona y Canal")
    pivot_ventas_display = pivot_ventas.copy()
    pivot_ventas_display = pivot_ventas_display.applymap(lambda x: f"${x:,.0f}" if x > 0 else "-")
    st.dataframe(pivot_ventas_display, use_container_width=True, height=400)

# Gráfico de barras horizontales apiladas - Top zonas
st.markdown("#### 📊 Composición de Ventas: Top 8 Zonas")

top_zonas = pivot_ventas.head(8).index.tolist()

fig_barras_zona = go.Figure()

for canal in ['MINORISTA', 'INTEGRADOR', 'OPERADORES', 'RETAIL']:
    if canal in pivot_ventas.columns:
        valores = [pivot_ventas.loc[zona, canal] for zona in top_zonas]
        fig_barras_zona.add_trace(go.Bar(
            name=canal,
            y=top_zonas,
            x=valores,
            orientation='h',
            marker_color=CANAL_COLORS.get(canal, '#999'),
            text=[f"${v/1000:,.0f}K" if v > 50000 else "" for v in valores],
            textposition='inside',
            textfont=dict(size=10, color='white')
        ))

fig_barras_zona.update_layout(
    barmode='stack',
    height=400,
    xaxis_title="Venta Total 2025 (USD)",
    xaxis_tickformat="$,.0f",
    yaxis_title="",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    margin=dict(l=120, r=20, t=60, b=40),
    plot_bgcolor='white'
)
fig_barras_zona.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
fig_barras_zona.update_yaxes(autorange="reversed")

st.plotly_chart(fig_barras_zona, use_container_width=True)

# Insights de zona-canal
zona_top = pivot_ventas.index[0]
venta_zona_top = pivot_ventas.loc[zona_top, 'Total']
canal_dominante_zona_top = pivot_ventas.loc[zona_top, canales_heatmap].idxmax()

st.markdown(f"""
<div class="insight-box">
<strong>🎯 Hallazgos Territoriales:</strong><br><br>
• <b>{zona_top}</b> es la zona líder con <b>${venta_zona_top:,.0f}</b> en ventas, dominada por el canal <b>{canal_dominante_zona_top}</b>.<br><br>
• Las zonas del <b>centro de Lima</b> (Wilson, Paruro, Malvinas, Azángaro) muestran fuerte concentración en MINORISTA, lo que amplifica el impacto del mayor tiempo de traslado desde Lurín.<br><br>
• <b>Provincias</b> muestra diversificación entre canales, sugiriendo estrategias diferenciadas por región.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RESUMEN EJECUTIVO
# ============================================================================
st.markdown('<p class="section-title">📋 Resumen Ejecutivo</p>', unsafe_allow_html=True)

# Calcular participación Lima vs Provincia
zona_analysis = df.groupby('ZONA_CONSOLIDADO').agg({
    'TOTAL_2025': 'sum'
}).reset_index()
zona_analysis['PARTICIPACION'] = (zona_analysis['TOTAL_2025'] / zona_analysis['TOTAL_2025'].sum()) * 100
zonas_lima = ['LIMA', 'WILSON', 'MALVINAS', 'PARURO', 'AZANGARO', 'COMPUPALACE', 'MARSANO', 'CALLAO', 'RIMAC']
zona_analysis['TIPO'] = zona_analysis['ZONA_CONSOLIDADO'].apply(lambda x: 'Lima' if x in zonas_lima else 'Provincia')
part_lima = zona_analysis[zona_analysis['TIPO'] == 'Lima']['PARTICIPACION'].sum()
part_provincia = zona_analysis[zona_analysis['TIPO'] == 'Provincia']['PARTICIPACION'].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); color: white; padding: 1.5rem; border-radius: 12px; height: 100%;">
    <h4 style="margin: 0 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">📊 Indicadores Clave</h4>
    <div style="font-size: 0.9rem; line-height: 1.8;">
    • Venta total: <b>${total_2025:,.0f}</b><br>
    • Promedio mensual: <b>${promedio_mensual:,.0f}</b><br>
    • SKUs activos: <b>{skus_con_venta:,}</b> de {skus_totales:,}<br>
    • Canal principal: MINORISTA ({participacion_minorista:.1f}%)<br>
    • Concentración Lima: {part_lima:.1f}%
    </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['warning']} 0%, #ff8c42 100%); color: white; padding: 1.5rem; border-radius: 12px; height: 100%;">
    <h4 style="margin: 0 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">⚠️ Riesgos Identificados</h4>
    <div style="font-size: 0.9rem; line-height: 1.8;">
    • Alta dependencia del canal MINORISTA<br>
    • Tiempos de entrega +1h al centro de Lima<br>
    • 6,296 SKUs obsoletos (71% del catálogo)<br>
    • Posible caída post-cambio de almacén<br>
    • Concentración en pocas zonas
    </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {COLORS['success']} 0%, #2ecc71 100%); color: white; padding: 1.5rem; border-radius: 12px; height: 100%;">
    <h4 style="margin: 0 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem;">✅ Oportunidades</h4>
    <div style="font-size: 0.9rem; line-height: 1.8;">
    • Diversificar hacia INTEGRADOR/OPERADORES<br>
    • Depurar inventario obsoleto<br>
    • Optimizar rutas centro de Lima<br>
    • Expandir en Provincias ({part_provincia:.1f}%)<br>
    • Cross-docking o punto intermedio
    </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {COLORS['muted']}; font-size: 0.85rem; padding: 1rem 0;">
📊 Dashboard generado con datos de Enero a Diciembre 2025 | Última actualización: Enero 2026
</div>
""", unsafe_allow_html=True)
