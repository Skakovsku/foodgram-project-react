from django.http import HttpResponse
from fpdf import FPDF


def get_list_shopping_cart(request, shopping_list):
    NUMBER_STRING = 22
    file_name = 'media/' + str(request.user) + '_shopping_cart.pdf'
    pdf = FPDF()
    pdf.add_font(
        'Sans',
        style='',
        fname='backend/foodgram/api/fount/NotoSans-Regular.ttf',
        uni=True
    )
    pdf.set_font('Sans', '', 16)
    page_count = 1
    pdf.add_page()
    for string_list in shopping_list:
        if page_count/NUMBER_STRING == int:
            pdf.add_page()
        product = str(string_list)
        amount = str(shopping_list[string_list][0])
        unit = str(shopping_list[string_list][1])
        string = str(product + ' ' + amount + ' ' + unit + '\n')
        pdf.cell(20, 10, txt=string, ln=1)
    pdf.output(file_name)
    response = HttpResponse(content_type='application/pdf')
    header_resp = 'attachment; filename= "{}"'.format(file_name)
    response['Content-Disposition'] = header_resp
    return response
