from io import BytesIO

from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from rest_framework import viewsets

from djangoMovies import settings
from .models import Movie, Actor, Director
from .serializers import MovieSerializer, ActorSerializer, DirectorSerializer

# Create your views here.


class MovieSet(viewsets.ModelViewSet):
    print('Im here')
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ActorSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class DirectorSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


def write_pdf_view(request, *args, **kwargs):
    movie = Movie.objects.get(pk=1)
    doc = SimpleDocTemplate("teste.pdf")
    styles = getSampleStyleSheet()
    Story = [Spacer(1,2*inch)]
    style = styles["Normal"]
    for i in range(5):
       bogustext = ("This is Paragraph number %s.  " % i)
       bogustext = ("Movie name = " + movie.name)
       p = Paragraph(bogustext, style)
       Story.append(p)
       Story.append(Spacer(1,0.2*inch))
    doc.build(Story)

    fs = FileSystemStorage("")
    with fs.open("teste.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        return response


def write_exam_pdf(request, id, *args, **kwargs):
    movie = Movie.objects.get(pk=id)

    response = HttpResponse(content_type='application/pdf')
    elements = []
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    y = 600
    c.setTitle("Hospital das Clinicas da UFMG")
    c.setLineWidth(.3)
    c.setFont("Times-Bold", 12)
    titulo1 = c.drawString(200, 780, 'HOSPITAL DAS CLINICAS DA UFMG')
    c.drawString(200, 760, 'PEDIDO DE EXAME COMPLEMENTAR')
    image = "C:/Users/felip/Documents/Projects/djangoMovies/djangoMovies/media/image.png"
    c.drawImage(image, 70, 750, width=110, height=80)

    styles = getSampleStyleSheet()
    stylesBH = styles["Normal"]
    stylesBH.alignment = TA_CENTER
    stylesBH.fontSize = 12

    headings = ('Nome: ' + str(movie.name) + 'Terra do Tio Sam',)
    headings1 = ('Clinicia/UI: ' + str(movie.id),)
    headings2 = ('Prontuário: ' + str(movie.year), 'Leito:       ')
    c.acroForm.checkbox(
        name='Emrg',
        tooltip='Sim',
        x=182, y=640,
        borderStyle='solid',
        borderWidth=1,
        size=15,
        fieldFlags='readOnly'
    )
    c.acroForm.checkbox(
        name='Emrg1',
        tooltip='Não',
        x=222, y=640,
        borderStyle='solid',
        borderWidth=1,
        size=15,
        checked=True,
        fieldFlags='readOnly'
    )
    c.acroForm.checkbox(
        name='Emrg2',
        tooltip='SUS',
        x=305, y=640,
        borderStyle='solid',
        borderWidth=1,
        size=15,
        fieldFlags='readOnly'
    )
    c.acroForm.checkbox(
        name='Emrg3',
        tooltip='Convenio',
        x=382, y=640,
        borderStyle='solid',
        borderWidth=1,
        size=15,
        fieldFlags='readOnly'
    )
    c.acroForm.checkbox(
        name='Emrg4',
        tooltip='Particular',
        x=477, y=640,
        borderStyle='solid',
        borderWidth=1,
        size=15,
        fieldFlags='readOnly'
    )

    elements.append(headings)
    c.setFont("Times-Roman", 6)
    table = Table([headings], colWidths=None, rowHeights=0.20*inch, splitByRow=3)
    table.setStyle(TableStyle(
        [
            #('GRID', (0, 0), (4, -3), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            #('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            #('BACKGROUND', (0, 0), (-1, 0), colors.transparent),
        ]
    ))

    table1 = Table([headings1], colWidths=None, rowHeights=0.20 * inch, splitByRow=3)
    table1.setStyle(TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ]
    ))

    table2 = Table([headings2], colWidths=None, rowHeights=0.20 * inch, splitByRow=3)
    table2.setStyle(TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ]
    ))

    table.wrapOn(c, 600, 800)
    table.drawOn(c, 80, 700)
    table1.wrapOn(c, 600, 790)
    table1.drawOn(c, 80, 670)
    table2.wrapOn(c, 600, 790)
    table2.drawOn(c, 80, 685)
    c.setFont("Times-Bold", 12)
    c.drawString(80, 640, "Emergência:   Sim ")
    c.drawString(200, 640, "Não")
    c.drawString(280, 640, "SUS")
    c.drawString(330, 640, "Convênio")
    c.drawString(420, 640, "Particular")
    c.drawString(80, 600, "Diagnóstico")
    c.line(80, 575, 520, 575)
    c.line(80, 550, 520, 550)
    c.line(80, 525, 520, 525)
    c.line(80, 465, 520, 465)
    c.setFont("Helvetica", 9)
    c.drawString(80, 500, "QUANDO NECESSITAR DE URGÊNCIA NO ATENDIMENTO, JUSTIFIQUE NO VERSO O MOTIVO")
    c.drawString(80, 480, "PARA QUAISQUER OBSERVAÇÕES NECESSÁRIAS, USE TAMBÉM O VERSO DESTE IMPRESSO")
    c.setFont("Times-Bold", 12)
    c.drawString(80, 448, "EXAMES SOLICITADOS")
    c.acroForm.checkbox(name='Exam1', tooltip='Hemograma', checked=True, x=80, y=417, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam2', tooltip='Plaquetas', x=80, y=399, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam3', tooltip='AP/RNI', x=80, y=381, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam4', tooltip='PTTA', checked=True, x=80, y=363, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam5', tooltip='T4 Livre', x=80, y=345, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam6', tooltip='TSH', checked=True, x=80, y=327, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam7', tooltip='Anti-TPO', x=80, y=309, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam8', tooltip='Fator Reumatóide', x=80, y=291, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam9', tooltip='Anti-LKM', x=80, y=273, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam10', tooltip='Anti-mitocôndria (AMA)', checked=True, x=80, y=255, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam11', tooltip='Anti-músculo liso (ASMA)', x=80, y=237, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam12', tooltip='Anti-nuclear (ANA)', x=80, y=219, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam13', tooltip='Alfafetoproteina', checked=True, x=80, y=201, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam14', tooltip='Crioglobulinas', checked=True, x=80, y=183, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam15', tooltip='Insulina Sérica', x=80, y=165, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam16', tooltip='Urina rotina', x=80, y=147, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam17', tooltip='Proteinuria 24h', checked=True, x=80, y=129, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.drawString(94, 418, "Hemograma")
    c.drawString(94, 400, "Plaquetas")
    c.drawString(94, 382, "AP/RNI")
    c.drawString(94, 364, "PTTa")
    c.drawString(94, 346, "T4 Livre")
    c.drawString(94, 328, "TSH")
    c.drawString(94, 310, "Anti-TPO")
    c.drawString(94, 292, "Fator Reumatóide")
    c.drawString(94, 274, "Anti-LKM")
    c.drawString(94, 256, "Anti-Mitocondria(AMA)")
    c.drawString(94, 238, "Anti Musculo Liso (ASMA)")
    c.drawString(94, 220, "Anti-nuclear")
    c.drawString(94, 202, "Alfafetoproteina")
    c.drawString(94, 184, "Crioglobulinas")
    c.drawString(94, 166, "Insulina Sérica")
    c.drawString(94, 148, "Urina rotina")
    c.drawString(94, 130, "Proteinuria 24h")
    c.acroForm.checkbox(name='Exam18', tooltip='Clearence Creat 24h', checked=True, x=250, y=417, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam19', tooltip='EPF 3 amostras MIF', checked=True, x=250, y=399, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam20', tooltip='EPF 3 amostras K. Katz', checked=True, x=250, y=381, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam21', tooltip='Glicemia Jejum', checked=True, x=250, y=363, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam22', tooltip='AST/ALT', checked=True, x=250, y=345, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam23', tooltip='Bil. Total', checked=False, x=250, y=327, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam24', tooltip='Bil direta/indireta', checked=True, x=250, y=309, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam25', tooltip='Uréia', checked=True, x=250, y=291, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam26', tooltip='Creatima', checked=False, x=250, y=273, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam27', tooltip='Fosf. Alcalina', checked=False, x=250, y=255, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam28', tooltip='GGT', checked=True, x=250, y=237, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam29', tooltip='Proteina total', checked=False, x=250, y=219, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam30', tooltip='Albumina', checked=False, x=250, y=201, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam31', tooltip='Globulinas', checked=True, x=250, y=183, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam32', tooltip='Amilase', checked=True, x=250, y=165, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam33', tooltip='Lipase', checked=True, x=250, y=147, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam34', tooltip='Lactato', checked=True, x=250, y=129, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.drawString(264, 418, "Clearance Creat 24h")
    c.drawString(264, 400, "EPF 3 amostras MIF")
    c.drawString(264, 382, "EPF 3 amostras K. Katz")
    c.drawString(264, 364, "Glicemia Jejum")
    c.drawString(264, 346, "AST/ALT")
    c.drawString(264, 328, "Bil. Total")
    c.drawString(264, 310, "Bil direta/indireta")
    c.drawString(264, 292, "Uréia")
    c.drawString(264, 274, "Creatinina")
    c.drawString(264, 256, "Fosf Alcalina")
    c.drawString(264, 238, "GGT")
    c.drawString(264, 220, "Proteína Total")
    c.drawString(264, 202, "Albumina")
    c.drawString(264, 184, "Globulinas")
    c.drawString(264, 166, "Amilase")
    c.drawString(264, 148, "Lipase")
    c.drawString(264, 130, "Lactato")

    c.acroForm.checkbox(name='Exam35', tooltip='Ácido Úrico', checked=True, x=410, y=417, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam36', tooltip='Cálcio', checked=True, x=410, y=399, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam37', tooltip='Sódio', checked=True, x=410, y=381, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam38', tooltip='Potássio', checked=True, x=410, y=363, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam39', tooltip='Col. total e Frações', checked=True, x=410, y=345, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam40', tooltip='Triglicerídeos', checked=True, x=410, y=327, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam41', tooltip='Ferro Sérico', checked=True, x=410, y=309, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam42', tooltip='Ferritina', checked=True, x=410, y=291, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam43', tooltip='IST', checked=True, x=410, y=273, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam44', tooltip='HBsAg', checked=True, x=410, y=255, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam45', tooltip='HBeAG', checked=False, x=410, y=237, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam46', tooltip='Anti-HBs', checked=True, x=410, y=219, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam47', tooltip='Anti-HBe', checked=False, x=410, y=201, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam48', tooltip='Anti-HBc IgG', checked=True, x=410, y=183, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam49', tooltip='Anti-HBc IgM', checked=False, x=410, y=165, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam50', tooltip='Anti-HAV', checked=True, x=410, y=147, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.acroForm.checkbox(name='Exam51', tooltip='Anti-HCV', checked=False, x=410, y=129, borderStyle='solid', borderWidth=1, size=10, fieldFlags='readOnly')
    c.drawString(424, 418, "Clearance Creat 24h")
    c.drawString(424, 400, "EPF 3 amostras MIF")
    c.drawString(424, 382, "EPF 3 amostras K. Katz")
    c.drawString(424, 364, "Glicemia Jejum")
    c.drawString(424, 346, "AST/ALT")
    c.drawString(424, 328, "Bil. Total")
    c.drawString(424, 310, "Bil direta/indireta")
    c.drawString(424, 292, "Uréia")
    c.drawString(424, 274, "Creatinina")
    c.drawString(424, 256, "Fosf Alcalina")
    c.drawString(424, 238, "GGT")
    c.drawString(424, 220, "Proteína Total")
    c.drawString(424, 202, "Albumina")
    c.drawString(424, 184, "Globulinas")
    c.drawString(424, 166, "Amilase")
    c.drawString(424, 148, "Lipase")
    c.drawString(424, 130, "Lactato")

    c.line(80, 70, 220, 70)
    # c.line(270, 70, 350, 70)
    c.line(410, 70, 500, 70)
    c.setFont("Times-Roman", 8)
    c.drawString(105, 60, "Assinatura/CRM Carimbo")
    # c.drawString(280, 60, "Jefe de Est.")
    c.drawString(450, 60, "Data")

    c.save()
    pdf = buffer.getvalue()
    response.write(pdf)
    return response
