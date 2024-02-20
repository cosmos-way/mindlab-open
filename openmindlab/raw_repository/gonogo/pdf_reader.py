import fitz  # Импорт библиотеки PyMuPDF

def extract_text_by_coordinates(pdf_path, rect):
    """
    Извлекает текст из PDF файла, расположенный внутри заданной прямоугольной области.

    :param pdf_path: Путь к PDF файлу.
    :param rect: Прямоугольная область в формате (x0, y0, x1, y1),
                 где (x0, y0) - координаты левого верхнего угла,
                 (x1, y1) - координаты правого нижнего угла.
    :return: Извлеченный текст из заданной области.
    """
    doc = fitz.open(pdf_path)  # Открытие PDF файла
    text = ""  # Строка для накопления извлеченного текста

    for page in doc:  # Перебор страниц в документе
        text += page.get_text("text", clip=fitz.Rect(rect))  # Извлечение текста из заданной области

    doc.close()  # Закрытие документа
    return text.strip()  # Удаление лишних пробелов и переносов строк


def find_text_in_pdf(file_path, search_text):
    doc = fitz.open(file_path)
    found_instances = []

    # Перебор страниц и поиск текста
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = page.search_for(search_text)
        
        # Добавление информации о найденных инстанциях
        for inst in text_instances:
            found_instances.append({
                "page": page_num + 1,  # Нумерация страниц для пользователя начинается с 1
                "coords": inst
            })

    doc.close()

    # Проверка, найден ли текст ровно один раз
    if len(found_instances) == 1:
        return found_instances[0]['coords']
    elif len(found_instances) == 0:
        return 0
    else:
        return 0
