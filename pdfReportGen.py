from fpdf import FPDF
from datetime import datetime
class PDF(FPDF):
    def titles(self):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=30.0, align='C', txt="Plagiarism Report", border=0)
    def lines(self):
        self.rect(5.0, 5.0, 200.0,287.0)
        self.rect(8.0, 8.0, 194.0,282.0)
    def myData1(self,name):
        self.set_y(20)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(220, 50, 50)
        self.cell(w=190.0, h=10.0, txt="Name :"+str(name), border=1,align='L')
        self.ln(20)
    def myTable(self,data):
        self.set_font('Times','',10.0) 
        
        #data = [['Name','Plagiarism Percentage']]
 
        # Document title centered, 'B'old, 14 pt
        self.set_font('Times','',10.0) 
        self.ln(0.5)
 
        # Text height is the same as current font size
        th = self.font_size
        # for data in data:
        #     self.cell(40,0,str(data),1)
        # self.ln()
        for row in data:
            for col in row:
                self.cell(80,10,str(col),1)
            self.ln()
def setData(name,result):
    print('setData Called')
    print(result)
    pdf=PDF(orientation='P',unit='mm',format='A4')
    pdf.add_page()
    pdf.lines()
    pdf.titles()
    pdf.myData1(name)
    pdf.myTable(result)

    now = datetime.now()
    # dd/mm/YY H:M:S
    #dt_string = now.strftime("%Y_%m_%d-%I_%M_%S_%p")
    dt_string=name

    print(dt_string)
    pdf.output("./Reports/"+(dt_string)+".pdf")

