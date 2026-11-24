import streamlit as st
import json
import os
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
st.set_page_config(
    page_title="Generador de cotizaciones",
    page_icon="📋",
    layout="wide"
)

st.markdown("""
<style>
h1 {
    color: #4A90E2;
}

h2, h3 {
    color: #5B9BD5;
}

.stButton > button {
    border-radius: 8px;
    border: 1px solid #4A90E2;
}
</style>
""", unsafe_allow_html=True)
def generar_pdf(cotizacion):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))

    pdf.setFillColorRGB(0.05, 0.35, 0.75)
    pdf.circle(65, 550, 18, fill=1, stroke=0)

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(65, 544, "N")

    pdf.setFillColorRGB(0.05, 0.15, 0.30)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(92, 545, "NEXA DIGITAL")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(92, 527, "Soluciones digitales para tu negocio")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 485, "COTIZACION")
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(350, 455, f"Fecha: {fecha}")
    pdf.setStrokeColorRGB(0.15, 0.35, 0.60)
    pdf.setLineWidth(2)
    pdf.line(50, 435, 790, 435)
    

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 455, f"Numero: {cotizacion['numero']:03d}")
    pdf.drawString(50, 405, f"Cliente: {cotizacion['cliente']}")
    pdf.setFillColorRGB(0.09, 0.21, 0.36)
    pdf.rect(50, 350, 740, 25, fill=1)

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, 359, "PRODUCTO")
    pdf.drawString(300, 359, "CANTIDAD")
    pdf.drawString(410, 359, "PRECIO")

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, 325, str(cotizacion['producto']))
    pdf.drawString(300, 325, str(cotizacion['cantidad']))
    pdf.drawString(410, 325, f"${cotizacion['precio']:,.0f}")

    total = cotizacion.get(
        "total",
        cotizacion["cantidad"] * cotizacion["precio"]
    )
    pdf.setFillColorRGB(0.88, 0.93, 0.98)
    pdf.roundRect(50, 255, 740, 40, 8, fill=1, stroke=0)

    pdf.setFillColorRGB(0.09, 0.21, 0.36)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(65, 269, f"TOTAL: ${total:,.0f}")
    pdf.setFillColorRGB(0.35, 0.35, 0.35)
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawCentredString(
    421, 220,
    "Gracias por confiar en Nexa Digital")
    pdf.setFillColorRGB(0.05, 0.15, 0.30)
    pdf.setFont("Helvetica", 9)

    pdf.drawString(50, 80, "WhatsApp: +57 300 000 0000")
    pdf.drawString(50, 65, "Correo: contacto@nexadigital.com")


    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()
ARCHIVO = "cotizaciones.json"

def cargar_cotizaciones():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []

def guardar_cotizaciones():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(
            st.session_state["cotizaciones"],
            archivo,
            ensure_ascii=False,
            indent=4
        )

if "cotizaciones" not in st.session_state:
    st.session_state["cotizaciones"] = cargar_cotizaciones()

st.title("📋 Generador de cotizaciones")
st.markdown("### Sistema de gestión de cotizaciones")
st.caption("Crea, consulta, actualiza y administra tus cotizaciones fácilmente.")



st.divider()

st.subheader("Panel principal")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de cotizaciones", len(st.session_state["cotizaciones"]))

with col2:
    st.metric("Estado", "Activo")

with col3:
    st.metric("Módulo", "Gestión")

st.success("Sistema listo para gestionar tus cotizaciones.")
st.subheader("Crear nueva cotización")
col1, col2 = st.columns(2)

with col1:
    nombre_cliente = st.text_input("Nombre del cliente")

with col2:
    producto = st.text_input("Producto o servicio")

with col1:
    cantidad = st.number_input("Cantidad", min_value=1, step=1)

with col2:
    precio = st.number_input("Precio unitario", min_value=0.0, step=1000.0)
total = cantidad * precio

st.write(f"### Total de la cotización: ${total:,.0f}")
if st.button("Guardar cotización"):
    numero = len(st.session_state["cotizaciones"]) + 1

    cotizacion = {
        "numero": numero,
        "cliente": nombre_cliente,
        "producto": producto,
        "cantidad": cantidad,
        "precio": precio,
        "total" : total 
    }

    st.session_state["cotizaciones"].append(cotizacion)
    guardar_cotizaciones()

    st.success(f"¡Cotización {numero:03d} registrada correctamente!")
    st.divider()

st.subheader("Consultar cotizaciones")

if st.session_state["cotizaciones"]:
    for cotizacion in st.session_state["cotizaciones"]:
        st.write(f"*Cotización {cotizacion['numero']:03d}*")
        st.write(f"Cliente: {cotizacion['cliente']}")
        st.write(f"Producto: {cotizacion['producto']}")
        st.write(f"Cantidad: {cotizacion['cantidad']}")
        st.write(f"Precio unitario: ${cotizacion['precio']:,.0f}")
        total_guardado = cotizacion.get("total", cotizacion["cantidad"] * cotizacion["precio"])
        st.write(f"*Total: ${total_guardado:,.0f}*")
        st.write("---")
        pdf = generar_pdf(cotizacion)

        st.download_button(
            label="📄 Descargar cotización en PDF",
            data=pdf,
            file_name=f"cotizacion_{cotizacion['numero']:03d}.pdf",
            mime="application/pdf"
        )
else:
        st.info("Todavía no hay cotizaciones registradas.")
        st.divider()

st.subheader("Actualizar cotización")

if st.session_state["cotizaciones"]:

    numeros = [
        cotizacion["numero"]
        for cotizacion in st.session_state["cotizaciones"]
    ]

    seleccion = st.selectbox(
        "Selecciona el número de cotización",
        numeros
    )

    cotizacion_seleccionada = next(
        c for c in st.session_state["cotizaciones"]
        if c["numero"] == seleccion
    )

    nuevo_cliente = st.text_input(
        "Nombre del cliente",
        value=cotizacion_seleccionada["cliente"]
    )

    nuevo_producto = st.text_input(
        "Producto o servicio",
        value=cotizacion_seleccionada["producto"],
        key= "editar_producto"
    )

    nueva_cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        value=int(cotizacion_seleccionada["cantidad"]),
        key="nueva_cantidad"
    )

    nuevo_precio = st.number_input(
        "Precio unitario",
        min_value=0.0,
        value=float(cotizacion_seleccionada["precio"]),
        key="nuevo_precio"
    )

    if st.button("Actualizar cotización"):
        cotizacion_seleccionada["cliente"] = nuevo_cliente
        cotizacion_seleccionada["producto"] = nuevo_producto
        cotizacion_seleccionada["cantidad"] = nueva_cantidad
        cotizacion_seleccionada["precio"] = nuevo_precio
        guardar_cotizaciones()

        st.success("¡Cotización actualizada correctamente!")
        st.rerun()

else:
    st.info("No hay cotizaciones para actualizar.")
    st.divider()

st.subheader("Eliminar cotización")

if st.session_state["cotizaciones"]:

    numeros = [
        cotizacion["numero"]
        for cotizacion in st.session_state["cotizaciones"]
    ]

    numero_eliminar = st.selectbox(
        "Selecciona la cotización que deseas eliminar",
        numeros,
        key="eliminar_cotizacion"
    )

    if st.button("Eliminar cotización"):
        st.session_state["cotizaciones"] = [
            cotizacion
            for cotizacion in st.session_state["cotizaciones"]
            if cotizacion["numero"] != numero_eliminar
        ]
        guardar_cotizaciones()

        st.success("¡Cotización eliminada correctamente!")
        st.rerun()

else:
    st.info("No hay cotizaciones para eliminar.")
