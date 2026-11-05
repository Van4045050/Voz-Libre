import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

# ==================================================
# 1. CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Voz Libre | Tu espacio",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded"
)

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "datos.csv"

COLUMNAS = ["ID", "Categoria", "Contenido", "Color", "Fecha"]

# Imágenes de la página
IMG_NATURALEZA = "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1200"
IMG_FLORES = "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=900"
IMG_ARTE = "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=900"
IMG_BAILE = "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=900"
IMG_COCINA = "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=900"


# ==================================================
# 2. ESTILOS PERSONALIZADOS
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap');

.stApp {
    background: #f8f7fc;
    color: #35445b;
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: #34445c !important;
    font-family: 'Playfair Display', serif !important;
}

p {
    color: #64748b;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e5f5f2, #f0eafd);
    border-right: 1px solid #dce9eb;
}

[data-testid="stSidebar"] h1 {
    color: #355e65 !important;
}

.hero {
    background: linear-gradient(120deg, #d9f3ec, #e9e2fa, #fce5ef);
    padding: 42px;
    border-radius: 25px;
    margin-bottom: 25px;
    border: 1px solid #ffffff;
}

.hero h1 {
    font-size: 42px;
    line-height: 1.2;
    margin-top: 12px;
}

.hero p {
    font-size: 17px;
    color: #52677b;
}

.eyebrow {
    color: #648c89;
    font-weight: 700;
    letter-spacing: 3px;
    font-size: 12px;
    text-transform: uppercase;
}

.card {
    background: white;
    padding: 23px;
    border-radius: 19px;
    border: 1px solid #e8e8f1;
    box-shadow: 0 5px 18px rgba(72, 78, 112, 0.06);
    margin-bottom: 15px;
}

.soft-aqua {
    background: #e1f4ee;
}

.soft-lavender {
    background: #eee8fb;
}

.soft-pink {
    background: #fbe8f0;
}

.soft-blue {
    background: #e5effb;
}

.tag {
    display: inline-block;
    padding: 6px 13px;
    border-radius: 20px;
    background: #e6f3ee;
    color: #477a70;
    font-size: 12px;
    font-weight: 700;
}

.quote {
    background: linear-gradient(120deg, #e8e2fa, #fbe7ef);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin: 15px 0;
}

.quote p {
    font-family: 'Playfair Display', serif;
    font-size: 23px;
    font-style: italic;
    color: #586080;
}

.stButton > button,
.stFormSubmitButton > button,
.stLinkButton > a {
    background: #789b99 !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 9px 20px !important;
    transition: 0.3s;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stLinkButton > a:hover {
    background: #627f91 !important;
    transform: translateY(-2px);
}

.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
}

hr {
    border-color: #e5e6ee;
}

.footer {
    background: #e9f2f0;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-top: 35px;
}

.footer p {
    color: #617c7a;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. FUNCIONES DE DATOS
# ==================================================

def datos_de_ejemplo():

    return pd.DataFrame([
        {
            "ID": 1,
            "Categoria": "Pensamiento",
            "Contenido": "Un respiro también es un comienzo.",
            "Color": "Aqua",
            "Fecha": "2026-10-29"
        },
        {
            "ID": 2,
            "Categoria": "Apoyo",
            "Contenido": "Hablar con alguien de confianza puede ayudarte.",
            "Color": "Azul",
            "Fecha": "2026-10-29"
        },
        {
            "ID": 3,
            "Categoria": "Actividad",
            "Contenido": "Traza líneas y colores sin buscar un resultado perfecto.",
            "Color": "Lavanda",
            "Fecha": "2026-10-28"
        },
        {
            "ID": 4,
            "Categoria": "Pensamiento",
            "Contenido": "No tienes que resolverlo todo hoy.",
            "Color": "Rosa",
            "Fecha": "2026-10-28"
        }
    ], columns=COLUMNAS)


def cargar_datos():

    if not ARCHIVO.exists():
        return datos_de_ejemplo()

    try:
        df = pd.read_csv(ARCHIVO, encoding="utf-8-sig")

        if df.empty:
            return datos_de_ejemplo()

        for columna in COLUMNAS:
            if columna not in df.columns:
                df[columna] = ""

        df = df[COLUMNAS].copy()

        df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
        df["Categoria"] = df["Categoria"].fillna("Pensamiento").astype(str)
        df["Contenido"] = df["Contenido"].fillna("").astype(str)
        df["Color"] = df["Color"].fillna("Aqua").astype(str)
        df["Fecha"] = df["Fecha"].fillna("").astype(str)

        df = df[df["Contenido"].str.strip() != ""]

        return df

    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        st.warning("No se pudieron leer los datos. Se mostrarán ejemplos.")
        return datos_de_ejemplo()


def guardar_datos(df):

    try:
        df.to_csv(ARCHIVO, index=False, encoding="utf-8-sig")
        return True

    except OSError:
        st.error("No se pudieron guardar los datos.")
        return False


def publicar_nota(contenido, color):

    df = cargar_datos()

    ids = pd.to_numeric(df["ID"], errors="coerce")

    nuevo_id = int(ids.max()) + 1 if ids.notna().any() else 1

    nueva_nota = pd.DataFrame([{
        "ID": nuevo_id,
        "Categoria": "Pensamiento",
        "Contenido": contenido,
        "Color": color,
        "Fecha": date.today().isoformat()
    }])

    df = pd.concat([df, nueva_nota], ignore_index=True)

    return guardar_datos(df)


# ==================================================
# 4. BARRA LATERAL
# ==================================================

st.sidebar.image(
    "https://img.icons8.com/fluency/96/butterfly.png",
    width=65
)

st.sidebar.title("Voz Libre")

st.sidebar.markdown(
    "*Un espacio para sentir, crear y compartir.*"
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "EXPLORA",
    [
        "Inicio",
        "Muro de Pensamientos",
        "Apoyo y Recursos",
        "Actividades",
        "Quiénes Somos"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### ✨ Recuerda")

st.sidebar.info(
    "Tus emociones importan. No tienes que tener todo resuelto."
)

st.sidebar.caption("VOZ LIBRE · 2026")


# ==================================================
# 5. INICIO
# ==================================================

if menu == "Inicio":

    st.markdown("""
    <div class="hero">

        <span class="eyebrow">BIENVENIDO A VOZ LIBRE</span>

        <h1>Un lugar para ser tú. 🦋</h1>

        <p>
        Un espacio donde puedes expresarte, descubrir nuevas ideas
        y recordar que cada emoción merece ser escuchada.
        </p>

        <span class="tag">SIENTE · CREA · COMPARTE</span>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9])

    with col1:

        st.image(IMG_NATURALEZA, use_container_width=True)

    with col2:

        st.markdown("""
        <div class="quote">

            <h3>💗 Una frase para ti</h3>

            <p>
            "No tienes que florecer todos los días
            para seguir creciendo."
            </p>

            <span class="tag">UN DÍA A LA VEZ</span>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Explora tu espacio")

    st.write("Cada sección tiene algo diferente para ofrecerte.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card soft-aqua">
        <h2>💬</h2>
        <h3>Exprésate</h3>
        <p>Comparte tus pensamientos en nuestro muro.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card soft-lavender">
        <h2>🤍</h2>
        <h3>Encuentra apoyo</h3>
        <p>Conoce recursos y aprende a pedir orientación.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card soft-pink">
        <h2>🎨</h2>
        <h3>Inspírate</h3>
        <p>Descubre actividades para expresarte.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Un pequeño recordatorio")

    st.image(IMG_FLORES, use_container_width=True)

    st.markdown("""
    <div class="quote">
    <p>
    "Cada persona tiene su propio ritmo.
    Tu proceso también merece paciencia."
    </p>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 6. MURO DE PENSAMIENTOS
# ==================================================

elif menu == "Muro de Pensamientos":

    st.title("💬 Muro de pensamientos")

    st.write(
        "Un espacio para compartir palabras, ideas y reflexiones."
    )

    st.info(
        "Las notas publicadas pueden ser vistas por quienes accedan "
        "a este muro. No compartas información personal o privada."
    )

    col1, col2 = st.columns([0.9, 1.1])

    with col1:

        st.markdown("### Deja tu mensaje")

        with st.form("formulario_nota", clear_on_submit=True):

            contenido = st.text_area(
                "¿Qué te gustaría expresar?",
                placeholder="Escribe aquí tu pensamiento...",
                max_chars=280
            )

            color = st.selectbox(
                "Elige un color",
                ["Aqua", "Azul", "Lavanda", "Rosa"]
            )

            enviar = st.form_submit_button(
                "Publicar mi pensamiento",
                use_container_width=True
            )

        if enviar:

            if contenido.strip():

                if publicar_nota(contenido.strip(), color):

                    st.success("¡Tu pensamiento fue publicado!")

                    st.rerun()

            else:

                st.warning("Primero escribe algo.")

        st.image(IMG_FLORES, use_container_width=True)

    with col2:

        st.markdown("### Pensamientos compartidos")

        df = cargar_datos()

        categorias = ["Todas"] + sorted(
            df["Categoria"].unique().tolist()
        )

        filtro = st.selectbox(
            "Filtrar pensamientos",
            categorias
        )

        if filtro != "Todas":

            df = df[df["Categoria"] == filtro]

        df["orden"] = pd.to_numeric(df["ID"], errors="coerce")

        df = df.sort_values(
            "orden",
            ascending=False,
            na_position="last"
        )

        if not df.empty:

            for _, fila in df.iterrows():

                colores = {
                    "Aqua": "soft-aqua",
                    "Azul": "soft-blue",
                    "Lavanda": "soft-lavender",
                    "Rosa": "soft-pink"
                }

                clase = colores.get(fila["Color"], "soft-aqua")

                st.markdown(
                    f'<div class="card {clase}">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"**{fila['Categoria']}** · {fila['Color']}"
                )

                st.write(fila["Contenido"])

                st.caption(f"Publicado: {fila['Fecha']}")

                st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.info("Todavía no hay pensamientos para mostrar.")


# ==================================================
# 7. APOYO Y RECURSOS
# ==================================================

elif menu == "Apoyo y Recursos":

    st.title("🤍 Un espacio para encontrar apoyo")

    st.write(
        "Conocer, aprender y pedir orientación también son "
        "formas de cuidarte."
    )

    st.image(IMG_NATURALEZA, use_container_width=True)

    st.markdown("## Recursos que pueden ayudarte")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card soft-aqua">

        <h2>🌿</h2>
        <h3>Organización Mundial de la Salud</h3>

        <p>
        Información y recursos sobre salud y bienestar.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Visitar la OMS ↗️",
            "https://www.who.int/es",
            use_container_width=True
        )

        st.markdown("""
        <div class="card soft-lavender">

        <h2>💜</h2>
        <h3>UNICEF</h3>

        <p>
        Información sobre bienestar, adolescencia y derechos.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Visitar UNICEF ↗️",
            "https://www.unicef.org/es",
            use_container_width=True
        )

    with col2:

        st.markdown("""
        <div class="card soft-pink">

        <h2>🌸</h2>
        <h3>Secretaría de Salud</h3>

        <p>
        Consulta información y servicios oficiales de salud en México.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Visitar Secretaría de Salud ↗️",
            "https://www.gob.mx/salud",
            use_container_width=True
        )

        st.markdown("""
        <div class="card soft-blue">

        <h2>🤝</h2>
        <h3>Hablar con alguien</h3>

        <p>
        Acercarte a una persona adulta de confianza
        puede ser un buen primer paso.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Consultar recursos de UNICEF ↗️",
            "https://www.unicef.org/es",
            use_container_width=True
        )

    st.warning(
        "Voz Libre es un proyecto informativo y no sustituye "
        "la atención profesional. Ante un peligro inmediato, "
        "busca ayuda de una persona adulta de confianza "
        "o llama al 911."
    )


# ==================================================
# 8. ACTIVIDADES
# ==================================================

elif menu == "Actividades":

    st.title("🎨 Un espacio para crear")

    st.write(
        "Descubre diferentes formas de expresarte. "
        "Elige una actividad y encuentra inspiración."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.image(IMG_ARTE, use_container_width=True)

        st.markdown("""
        <div class="card soft-lavender">
        <h3>🎨 Dibujo y arte</h3>
        <p>Expresa tus ideas mediante colores y formas.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Descubrir actividad"):

            st.write(
                "Dibuja un paisaje que represente cómo te gustaría "
                "sentirte hoy. No necesitas que sea perfecto."
            )

            st.write("Materiales: papel, lápices y colores.")

    with col2:

        st.image(IMG_BAILE, use_container_width=True)

        st.markdown("""
        <div class="card soft-pink">
        <h3>💃 Baile y movimiento</h3>
        <p>Utiliza el movimiento para expresar lo que llevas dentro.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Descubrir actividad"):

            st.write(
                "Elige una canción que te guste e inventa "
                "movimientos que representen su ritmo."
            )

            st.write("Materiales: música y un espacio cómodo.")

    with col3:

        st.image(IMG_COCINA, use_container_width=True)

        st.markdown("""
        <div class="card soft-aqua">
        <h3>🍓 Cocina creativa</h3>
        <p>Explora nuevas combinaciones y disfruta crear algo.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Descubrir actividad"):

            st.write(
                "Prepara una merienda sencilla y decórala "
                "de una manera creativa."
            )

            st.write("Materiales: ingredientes disponibles y creatividad.")

    st.markdown("---")

    st.markdown("### ✨ Tu pequeño momento creativo")

    actividad = st.selectbox(
        "¿Qué te gustaría hacer hoy?",
        [
            "Escribir una frase positiva",
            "Hacer un dibujo libre",
            "Escuchar música",
            "Crear una pequeña coreografía",
            "Preparar una merienda"
        ]
    )

    if st.button("Elegir mi actividad"):

        st.success(f"¡Hoy puedes dedicar un momento a: {actividad}!")


# ==================================================
# 9. QUIÉNES SOMOS
# ==================================================

elif menu == "Quiénes Somos":

    st.title("🦋 Conoce Voz Libre")

    st.image(IMG_FLORES, use_container_width=True)

    st.markdown("""
    <div class="hero">

    <span class="eyebrow">NUESTRA HISTORIA</span>

    <h1>Una idea nacida de la escucha.</h1>

    <p>
    Voz Libre es un proyecto creado para abrir conversaciones
    sobre las emociones, compartir ideas de autocuidado y
    recordar que todas las personas merecen ser escuchadas.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Nuestras creadoras")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="card soft-aqua" style="text-align:center;">
        <h1>🌷</h1>
        <h3>Vanessa</h3>
        <p>Creadora de Voz Libre</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="card soft-lavender" style="text-align:center;">
        <h1>🦋</h1>
        <h3>Dea</h3>
        <p>Creadora de Voz Libre</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="card soft-pink" style="text-align:center;">
        <h1>🌸</h1>
        <h3>Fernanda</h3>
        <p>Creadora de Voz Libre</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Nuestra misión")

    st.write(
        "Crear un espacio digital donde las personas puedan "
        "expresarse, descubrir recursos útiles y encontrar "
        "inspiración para su bienestar."
    )


# ==================================================
# 10. PIE DE PÁGINA
# ==================================================

st.markdown("""
<div class="footer">

<h3>🦋 VOZ LIBRE</h3>

<p>
Un lugar para sentir, crear y compartir.
</p>

<p>
Tus emociones importan. Tu voz también.
</p>

<p>
Este proyecto ofrece información y actividades
de expresión personal. No sustituye la atención profesional.
</p>

<p>
©️ 2026 Voz Libre · Todos los derechos reservados.
</p>

</div>
""", unsafe_allow_html=True
)
