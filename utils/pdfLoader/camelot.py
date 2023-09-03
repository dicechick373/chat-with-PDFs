import camelot

tables = camelot.read_pdf("data/pdf/土木技術管理規程集_道路Ⅱ編_テスト1.pdf")

for ix in tables[0].df.index:
    print(ix, tables[0].df.loc[ix][0], '|', tables[0].df.loc[ix][1])

