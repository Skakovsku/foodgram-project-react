import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


def get_list_shopping_cart(request, shopping_list):
    filename = str(request.user) + '_shopping.pdf'
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(21 * cm, 29.7 * cm))
    pdfmetrics.registerFont(TTFont('Sans', 'NotoSans-Regular.ttf'))
    pdf.setFont('Sans', 16)
    x, y = 2 * cm, 27 * cm
    text = 'Список планируемых покупок:'
    pdf.drawString(x, 28*cm, text=text)
    for string_list in shopping_list:
        product = str(string_list)
        amount = str(shopping_list[string_list][0])
        unit = str(shopping_list[string_list][1])
        string = str('- ' + product + ' ' + amount + ' ' + unit)
        pdf.drawString(x, y, text=string)
        y -= 1 * cm
        if y == (1 * cm):
            pdf.showPage()
            y = 28 * cm
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)
