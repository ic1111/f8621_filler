import pdfrw
from reportlab.pdfgen import canvas
import subprocess
import tkinter
import os
import sys
import pandas as pd
import numpy as np

exec(open(r'8621_xy_coordinates.py').read())


def create_overlay(path):
    """
    Create the data that will be overlayed on top
    of the form that we want to fill
    """
    number_of_lots = 5
    data_dict, file_dict = create_gui()
    tax_year=2000+int(data_dict["Tax year"])
    df_lot = pd.read_excel(file_dict['file'],sheet_name = 'Lot Details')
    df_eoy = pd.read_excel(file_dict['file'],sheet_name = 'EOY Details')
    number_of_lots = len(df_lot.index)
    print(df_lot)
    c = canvas.Canvas(path)
    coordinates = get_coordinates()
    add_personal_info(c,coordinates,data_dict)
    add_pfic_info(c,coordinates,data_dict)
    add_part_1(c,coordinates,data_dict,df_lot, df_eoy,tax_year)
    add_part_2(c,coordinates,data_dict)
    for lot in range(number_of_lots):
        if not add_part_4(c,coordinates,df_lot,df_eoy,lot,tax_year):
            number_of_lots=number_of_lots-1
    c.save()
    return number_of_lots

def add_personal_info(c,coordinates,data_dict):
    keys = ['Name of shareholder', 'Identifying Number', 'Address', 'City, State, Zip', 'Tax year', 'Type of Shareholder']
    for key in keys:
        c.drawString(coordinates[key][0],coordinates[key][1], data_dict[key])

    c.drawString(196, 627, u'\u2713') # type of shareholder

def add_pfic_info(c,coordinates,data_dict):
    keys = ['Name of PFIC', 'PFIC Address', 'PFIC Reference ID']
    for key in keys:
        c.drawString(coordinates[key][0],coordinates[key][1], data_dict[key])

def add_part_1(c,coordinates,data_dict, df_lot, df_eoy,current_year):
    part_1_dict = {}
    part_1_dict['Date of Aquision'] = 'Multiple'
    part_1_dict['Number of Shares'] = 0
    part_1_dict["Amount of 1291"] = ''
    part_1_dict["Amount of 1293"] = ''
    part_1_dict['Descrition of each class of shares']='Class A'
    for lot in range(len(df_lot.index)):
        # Check if lot was sold and get last price and ER
        if np.isnan(df_lot["Price per share: Sale"][lot]):
            price_aquisition = df_lot['Price per share: Acquisition'][lot]
            cost_aquisition = df_lot['Cost: Acquisition'][lot]
            part_1_dict['Number of Shares'] = part_1_dict['Number of Shares'] + cost_aquisition/price_aquisition

    last_er = df_eoy[df_eoy['Year']==current_year]["Exchange Rate"].values[0]
    last_price = df_eoy[df_eoy['Year']==current_year]["Price"].values[0]
    part_1_dict['Amount of 1296']= round(part_1_dict["Number of Shares"]*last_price/last_er)


    for key in part_1_dict.keys():
        c.drawString(coordinates[key][0],coordinates[key][1], '{}'.format(part_1_dict[key]))

    value_of_pfic = part_1_dict['Amount of 1296']
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

def add_part_4(c,coordinates,df_lot,df_eoy,lot,current_year):
    etf_dict = {}
    # Get info about origianl aquisition
    year_of_aqiusition = df_lot['Date: Acquisition'][lot].year
    price_aquisition = df_lot['Price per share: Acquisition'][lot]
    cost_aquisition = df_lot['Cost: Acquisition'][lot]
    er_of_aqiusition   = df_lot['Exchange Rate: Acquisition'][lot]

    number_of_shares = cost_aquisition/price_aquisition
    original_basis = cost_aquisition/er_of_aqiusition

    # Get last year's basis
    if current_year > year_of_aqiusition:
        prev_year_er = df_eoy[df_eoy['Year']==current_year-1]["Exchange Rate"].values[0]
        prev_year_price = df_eoy[df_eoy['Year']==current_year-1]["Price"].values[0]
        adjusted_basis = round(number_of_shares*prev_year_price/prev_year_er)
    else:
        adjusted_basis =  round(original_basis)


    # Check if lot was sold and get last price and ER
    if np.isnan(df_lot["Price per share: Sale"][lot]):
        print("no sale")
        last_er = df_eoy[df_eoy['Year']==current_year]["Exchange Rate"].values[0]
        last_price = df_eoy[df_eoy['Year']==current_year]["Price"].values[0]
        fmv_dollars = round(number_of_shares*last_price/last_er)
        print("Last ER={}, Last Price={}".format(last_er,last_price))
        print("FMV={}, Adjusted Basis={}".format(fmv_dollars,adjusted_basis))

        etf_dict['10a'] = fmv_dollars
        etf_dict['10b'] = adjusted_basis
        etf_dict['10c'] = etf_dict['10a'] - etf_dict['10b']
        if etf_dict['10c']<0:
            if adjusted_basis > original_basis:
                unreversed_inclusions = round(adjusted_basis - original_basis)
                if unreversed_inclusions>(-1*etf_dict['10c']):
                    loss_from_ten_c = etf_dict['10c']
                else:
                    loss_from_ten_c = -1*unreversed_inclusions
                etf_dict['11'] = unreversed_inclusions
                etf_dict['12'] = loss_from_ten_c
                print("12:  Include {} as an ordinary loss on your tax return".format(etf_dict['12']))
            else:
                etf_dict['11'] = ''
                etf_dict['12'] = ''
        else:
            etf_dict['11'] = ''
            etf_dict['12'] = ''
            print("10c: Add gain of {} to your ordinary income".format(etf_dict['10c']))
        etf_dict['13a'] = ''
        etf_dict['13b'] = ''
        etf_dict['13c'] = ''
        etf_dict['14a'] = ''
        etf_dict['14b'] = ''
        etf_dict['14c'] = ''

    else:
        print("sale")
        last_er = df_lot['Exchange Rate: Sale'][lot]
        last_price = df_lot['Price per share: Sale'][lot]
        year_of_sale = df_lot['Date: Sale'][lot].year
        if year_of_sale<current_year:
            return False
        fmv_dollars = round(number_of_shares*last_price/last_er)
        print("Last ER={}, Last Price={}".format(last_er,last_price))
        print("FMV={}, Adjusted Basis={}".format(fmv_dollars,adjusted_basis))
        etf_dict['13a'] = round(fmv_dollars)
        etf_dict['13b'] = round(adjusted_basis)
        etf_dict['13c'] = etf_dict['13a'] - etf_dict['13b']
        if etf_dict['13c']<0:
            if adjusted_basis > original_basis:
                unreversed_inclusions = round(adjusted_basis - original_basis)
                if unreversed_inclusions>(-1*etf_dict['13c']):
                    loss_from_thirteen_c = etf_dict['13c']
                else:
                    loss_from_thirteen_c = -1*unreversed_inclusions
                etf_dict['14a'] = unreversed_inclusions
                etf_dict['14b'] = loss_from_thirteen_c
                etf_dict['14c'] = ''
                print('14b: Enter {} as an ordinary loss'.format(etf_dict['14b']))
            else:
                etf_dict['14a'] = 0
                etf_dict['14b'] = 0
                etf_dict['14c'] = etf_dict['13c']
                print("14c: Include {} on tax return according to the rules generally applicable for losses provided elsewhere in the Code and regulations".format(etf_dict['14c']))
        else:
            etf_dict['14a'] = ''
            etf_dict['14b'] = ''
            etf_dict['14c'] = ''
            print("13c: Add gain of {} to your ordinary income".format(etf_dict['13c']))
        etf_dict['10a'] = ''
        etf_dict['10b'] = ''
        etf_dict['10c'] = ''
        etf_dict['11'] = ''
        etf_dict['12'] = ''

    c.showPage()
    for key in etf_dict.keys():
        c.drawString(coordinates[key][0],coordinates[key][1], '{}'.format(etf_dict[key]))
    return True


def merge_pdfs(pdf_1, pdf_2, output):
    """
    Merge the specified fillable form PDF with the
    overlay PDF and save the output
    """
    form = pdfrw.PdfReader(pdf_1)
    olay = pdfrw.PdfReader(pdf_2)

    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()

    writer = pdfrw.PdfWriter()
    writer.write(output, form)

def split(path, page, output):
    pdf_obj = pdfrw.PdfReader(path)
    total_pages = len(pdf_obj.pages)

    writer = pdfrw.PdfWriter()

    if page <= total_pages:
        writer.addpage(pdf_obj.pages[page])

    writer.write(output)

def concatenate(paths, output):
    writer = pdfrw.PdfWriter()

    for path in paths:
        reader = pdfrw.PdfReader(path)
        writer.addpages(reader.pages)

    writer.write(output)

def create_full_8621(path,number_of_page_2,output):
    orig_path = path + '.pdf'
    page_1_path = path + 'page1.pdf'
    page_2_path = path + 'page2.pdf'
    split(orig_path,0,page_1_path)
    split(orig_path,1,page_2_path)
    concatenate([page_1_path,page_2_path],output)
    for page in range(number_of_page_2-1):
        concatenate([output,page_2_path],output)

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
        data_dict['Tax year'] = '23'
        data_dict['Type of Shareholder'] = u'\u2713'
        data_dict['Name of PFIC'] = 'My_ETF'
        data_dict['PFIC Address'] = 'My_ETF_Address'
        data_dict['PFIC Reference ID'] = 'MY_ETF_REF_ID'
        file_dict['file'] = 'my_etf.xlsx'
    print(data_dict.keys())
    return data_dict, file_dict


def main():
    path = r'{}'
    form = "f8621"
    FORM_TEMPLATE_PATH = path.format(form) + '.pdf'
    FORM_FULL_PATH     = path.format(form) +'_full.pdf'
    FORM_OVERLAY_PATH = path.format(form) +'_overlay.pdf'
    FORM_OUTPUT_PATH = path.format(form) + '_filled_by_overlay.pdf'

    number_of_lots = create_overlay(FORM_OVERLAY_PATH)
    create_full_8621(form,number_of_lots,FORM_FULL_PATH)
    merge_pdfs(FORM_FULL_PATH,
               FORM_OVERLAY_PATH,
               FORM_OUTPUT_PATH)

    os.system(r"start chrome {}".format(FORM_OUTPUT_PATH))


main()
