#!/usr/bin/python3
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def pdf_create(text):
    c = canvas.Canvas('shopping_list.pdf', pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    c.setFont('FreeSans', 12)
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


if __name__ == '__main__':
    ctext = ['jopa', 'govno', 'Жопка-ложькя']
    pdf_create(ctext)
