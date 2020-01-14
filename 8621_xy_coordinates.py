coordinate_dict = {
# persoanl info
"Name of shareholder"               :(36, 688), # Name
"Identifying Number"                :(336, 688), # SS Number
"Address"                           :(36, 662),  # Address
"City, State, Zip"                  :(36, 638), # city stare zip
"Tax year"                          :(459, 675), # tax year
"Type of Shareholder"               :(196, 627), # type of shareholder
#PFIC info
"Name of PFIC"                      :(36, 567), # PFIC
"PFIC Address"                      :(36, 530), # PFIC address
"PFIC Reference ID"                 :(361, 543), # PFIC ref id
#PART I
"Descrition of each class of shares":(281, 470), # Descrition of each class of shares
"Date of Aquision"                  :(263, 434), # Date of Aquision
"Number of shares"                  :(243, 410), # number of shares
"Amount of 1291"                    :(152, 314), # amount of 1291
"Amount of 1293"                    :(245.6, 302), # amount of 1293
"Amount of 1296"                    :(217, 290), # amount of 1296
"Amount of 1296- Check"             :(79.2, 290), # type of PFIC type c
#Part II
"Check MTM"                         :(52.4, 205.5),
#PART IV
"FMV of PFIC at end of tax year"                               :(489.606, 408.01),
"adjusted cost basis at end of tax year"                               :(489.606, 396.011),
"a-b"                               :(489.606, 372.007),
"Unreversed inclusions"                                :(489.606, 360.008),
"lost from 10c"                                :(489.606, 336.007),
"FMV of sale"                               :(489.606, 312.009),
"adjusted cost basis of sale"                               :(489.606, 300.007),
"13a - 13b"                               :(489.606, 276.009),
"Unreversed inclusions on sale"                               :(489.606, 264.01),
"loss of 13c"                               :(489.606, 228.01),
"14c"                               :(489.606, 192.01),
}

def get_coordinates():
    return coordinate_dict
##row = 0
##for key in coordinate_dict.keys():
##    print("lbl{} = tkinter.Label(window, text='{}')".format(row,key))
##    print("lbl{}.grid(column=0, row={})".format(row,row))
##    print("txt{}=tkinter.Entry(window,width=30)".format(row))
##    print("txt{}.grid(column=1, row={})".format(row,row))
##    row = row+1
##
##row = 0
##for key in coordinate_dict.keys():
##    print("data_dict['{}'] = txt{}.get()".format(key,row))
##    row = row+1