#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, 'reportlab', 'FreeSans.ttf')


def pdf_create(text):
    c = canvas.Canvas('shopping_list.pdf', pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', path))
    c.setFont('FreeSans', 12)
    
    buffer = BytesIO()
    
    user = 'Пользователь'

    string_height = 750
    c.drawString(50, 800, 'Shopping list')
    c.drawString(400, 800, f'{user}: Username')
    c.line(0, 790, 800, 790)
    for line in text:
        c.drawString(50, string_height, line)
        string_height -= 30
    
    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    
    # c.showPage()
    # c.save()
    return pdf


if __name__ == '__main__':
    ctext = ['jopa', 'govno', 'Жопка-ложькя']
    pdf_create(ctext)
