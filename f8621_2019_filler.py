import pdfrw
from reportlab.pdfgen import canvas
import subprocess
import tkinter
import os
import sys

exec(open(r'8621_xy_coordinates.py').read())


def create_overlay(path):
    """
    Create the data that will be overlayed on top
    of the form that we want to fill
    """
    data_dict, file_dict = create_gui()
    c = canvas.Canvas(path)
    coordinates = get_coordinates()
    add_personal_info(c,coordinates,data_dict)
    add_pfic_info(c,coordinates,data_dict)
    add_part_1(c,coordinates,data_dict)
    add_part_2(c,coordinates,data_dict)
    add_part_4(c,coordinates,data_dict)
    c.save()

def add_personal_info(c,coordinates,data_dict):
    keys = ['Name of shareholder', 'Identifying Number', 'Address', 'City, State, Zip', 'Tax year', 'Type of Shareholder']
    for key in keys:
        c.drawString(coordinates[key][0],coordinates[key][1], data_dict[key])

    c.drawString(196, 627, u'\u2713') # type of shareholder

def add_pfic_info(c,coordinates,data_dict):
    keys = ['Name of PFIC', 'PFIC Address', 'PFIC Reference ID']
    for key in keys:
        c.drawString(coordinates[key][0],coordinates[key][1], data_dict[key])

def add_part_1(c,coordinates,data_dict):
    c.drawString(281, 470, 'Descrition of each class of shares') # Descrition of each class of shares
    c.drawString(263, 434, 'Date of Aquision') # Date of Aquision
    c.drawString(243, 410, '# of shares') # number of shares
    c.drawString(152, 314, 'amount of 1291') # amount of 1291
    c.drawString(245.6, 302, 'amount of 1293') # amount of 1293
    c.drawString(217, 290, 'amount of 1296') # amount of 1296

    value_of_pfic = 300000
    if (value_of_pfic>0) and (value_of_pfic<=50000):
        c.drawString(79.2, 373.5, u'\u2713') # value of pfic
    elif (value_of_pfic>50000) and (value_of_pfic<=100000):
        c.drawString(151.2, 373.5, u'\u2713') # value of pfic
    elif (value_of_pfic>100000) and (value_of_pfic<=150000):
        c.drawString(245, 373.5, u'\u2713') # value of pfic
    elif (value_of_pfic>150000) and (value_of_pfic<=200000):
        c.drawString(345.6, 373.5, u'\u2713') # value of pfic
    else:
        c.drawString(199, 362, '{}'.format(value_of_pfic)) # value of pfic

    # Check marks
    c.drawString(79.2, 290, u'\u2713') # type of PFIC type c


def add_part_2(c,coordinates,data_dict):
    c.drawString(52.4, 205.5, u'\u2713') # Part II election to MTM PFIC stock

def add_part_4(c,coordinates,data_dict):
    c.showPage()
    c.drawString(489.606, 408.01, "10a")
    c.drawString(489.606, 396.011, "10b")
    c.drawString(489.606, 372.007, "10c")
    c.drawString(489.606, 360.008, "11")
    c.drawString(489.606, 336.007, "12")
    c.drawString(489.606, 312.009, "13a")
    c.drawString(489.606, 300.007, "13b")
    c.drawString(489.606, 276.009, "13c")
    c.drawString(489.606, 264.01, "14a")
    c.drawString(489.606, 228.01, "14b")
    c.drawString(489.606, 192.01, "14c")

def merge_pdfs(form_pdf, overlay_pdf, output):
    """
    Merge the specified fillable form PDF with the
    overlay PDF and save the output
    """
    form = pdfrw.PdfReader(form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)

    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()

    writer = pdfrw.PdfWriter()
    writer.write(output, form)

def create_gui():
    data_dict = {}
    file_dict = {}
    window = tkinter.Tk()
    window.title("8621 Filler")
    window.geometry('500x400')
    lbl0 = tkinter.Label(window, text='Name of shareholder')
    lbl0.grid(column=0, row=0)
    txt0=tkinter.Entry(window,width=30)
    txt0.grid(column=1, row=0)
    lbl1 = tkinter.Label(window, text='Identifying Number')
    lbl1.grid(column=0, row=1)
    txt1=tkinter.Entry(window,width=30)
    txt1.grid(column=1, row=1)
    lbl2 = tkinter.Label(window, text='Address')
    lbl2.grid(column=0, row=2)
    txt2=tkinter.Entry(window,width=30)
    txt2.grid(column=1, row=2)
    lbl3 = tkinter.Label(window, text='City, State, Zip')
    lbl3.grid(column=0, row=3)
    txt3=tkinter.Entry(window,width=30)
    txt3.grid(column=1, row=3)
    lbl4 = tkinter.Label(window, text='Tax year')
    lbl4.grid(column=0, row=4)
    txt4=tkinter.Entry(window,width=30)
    txt4.grid(column=1, row=4)
    lbl5 = tkinter.Label(window, text='Type of Shareholder')
    lbl5.grid(column=0, row=5)
    txt5=tkinter.Entry(window,width=30)
    txt5.grid(column=1, row=5)
    lbl6 = tkinter.Label(window, text='Name of PFIC')
    lbl6.grid(column=0, row=6)
    txt6=tkinter.Entry(window,width=30)
    txt6.grid(column=1, row=6)
    lbl7 = tkinter.Label(window, text='PFIC Address')
    lbl7.grid(column=0, row=7)
    txt7=tkinter.Entry(window,width=30)
    txt7.grid(column=1, row=7)
    lbl8 = tkinter.Label(window, text='PFIC Reference ID')
    lbl8.grid(column=0, row=8)
    txt8=tkinter.Entry(window,width=30)
    txt8.grid(column=1, row=8)
    def clicked():
        data_dict['Name of shareholder'] = txt0.get()
        data_dict['Identifying Number'] = txt1.get()
        data_dict['Address'] = txt2.get()
        data_dict['City, State, Zip'] = txt3.get()
        data_dict['Tax year'] = txt4.get()
        data_dict['Type of Shareholder'] = txt5.get()
        data_dict['Name of PFIC'] = txt6.get()
        data_dict['PFIC Address'] = txt7.get()
        data_dict['PFIC Reference ID'] = txt8.get()

    def clicked_files():
        file_dict['file'] = tkinter.filedialog.askopenfilename()


    btn1 = tkinter.Button(window, text="Select File", command=clicked_files)
    btn1.grid(column=2, row=5)

    btn = tkinter.Button(window, text="Enter and press exit", command=clicked)
    btn.grid(column=2, row=0)

    window.mainloop()
##    for key in data_dict.keys():
##        print(data_dict[key])
##    print(file_dict['file'])
    if True:
        data_dict['Name of shareholder'] = 'John Expat'
        data_dict['Identifying Number'] = '123-45-6789'
        data_dict['Address'] = '1600 Pennsylvania Avenue'
        data_dict['City, State, Zip'] = 'Washigton DC'
        data_dict['Tax year'] = '19'
        data_dict['Type of Shareholder'] = u'\u2713'
        data_dict['Name of PFIC'] = 'My_ETF'
        data_dict['PFIC Address'] = 'My_ETF_Address'
        data_dict['PFIC Reference ID'] = 'MY_ETF_REF_ID'
    print(data_dict.keys())
    return data_dict, file_dict


def main():
    path = r'{}'
    form = "f8621"
    FORM_TEMPLATE_PATH = path.format(form) + '.pdf'
    FORM_OVERLAY_PATH = path.format(form) +'_overlay.pdf'
    FORM_OUTPUT_PATH = path.format(form) + '_filled_by_overlay.pdf'

    create_overlay(FORM_OVERLAY_PATH)
    merge_pdfs(FORM_TEMPLATE_PATH,
               FORM_OVERLAY_PATH,
               FORM_OUTPUT_PATH)

    os.system(r"start chrome {}".format(FORM_OUTPUT_PATH))

#create_gui()
main()