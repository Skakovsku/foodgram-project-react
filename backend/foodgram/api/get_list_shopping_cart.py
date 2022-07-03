from django.http import HttpResponse


def get_list_shopping_cart(request, shopping_list):
    file_name = 'media/' + str(request.user) + '_shopping_cart.txt'
    with open(file_name, 'w+') as file_list:
        for string_list in shopping_list:
            product = str(string_list)
            amount = str(shopping_list[string_list][0])
            unit = str(shopping_list[string_list][1])
            string = str(product + ' ' + amount + ' ' + unit + '\n')
            file_list.write(string)
    with open(file_name, 'r') as txt:
        response = HttpResponse(txt.read(), content_type='text/plain')
        response['Content-Disposition'] = 'inline;filename=shopping_list.txt'
        return response
