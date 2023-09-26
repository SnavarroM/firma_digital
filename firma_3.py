import PyPDF4
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

# Generar una clave privada RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Obtener la clave pública correspondiente
public_key = private_key.public_key()

# Crear un archivo PDF en blanco para la firma digital
firma_pdf = canvas.Canvas("firma.pdf", pagesize=letter)
firma_pdf.setFont("Helvetica", 8)  # Cambiar el tamaño de la fuente a 8

# Dibujar el sello con tu nombre en el archivo PDF
firma_pdf.drawString(10, 10, "Arquitecto de software Cenabast")  # Cambiar la posición del sello
firma_pdf.drawString(10, 25, "Firmado por: Sergio Navarro M.")  # Cambiar la posición del sello

# Guardar el archivo PDF con el sello
firma_pdf.save()

# Abrir el archivo PDF a firmar
with open('ejemplo.pdf', 'rb') as file:
    pdf = PyPDF4.PdfFileReader(file)
    num_pages = pdf.getNumPages()

    # Agregar el sello en cada página del archivo PDF
    writer = PyPDF4.PdfFileWriter()

    for page_num in range(num_pages):
        page = pdf.getPage(page_num)

        # Agregar el sello como anotación en forma de sello
        x = 10  # Cambiar la coordenada x a un valor más pequeño
        y = 10  # Cambiar la coordenada y a un valor más pequeño
        width = 200
        height = 50
        stamp = PyPDF4.PdfFileReader("firma.pdf").getPage(0)
        page.mergeTranslatedPage(stamp, x, y, expand=True)

        # Agregar la página firmada al objeto PdfFileWriter
        writer.addPage(page)

    # Guardar el archivo PDF firmado
    with open('ejemplo_firmado.pdf', 'wb') as output_file:
        writer.write(output_file)