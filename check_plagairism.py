import os
from difflib import SequenceMatcher
import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def func_check_plagiarism(fullPath, filename):
    #folder="files"
    file=[]
    file_data=[]
    #filelist=[]
    #acceptedfiletype=('.pdf','.txt')
    for files in fullPath :
        if files.endswith('.pdf'):
            file.append(open(files,'rb'))
        elif files.endswith('.txt'):
            file.append(open(files,'r'))
                    
    #punctuations=['(',')',';',':','[',']',',']
    #stop_words = stopwords.words('english')
    for i in file:
        if i.name.endswith('.pdf'):
            pdfReader = PyPDF2.PdfFileReader(i, strict=False)
            num_pages=pdfReader.numPages
            count=0
            text=""
            #filteredtext_pdf=[]
            while count<num_pages:
                pageobj=pdfReader.getPage(count)
                count+=1
                #filteredtext_pdf+=' '.join(str(elem) for elem in word_tokenize(pageobj.extractText()))
                text+=pageobj.extractText()
                
            tokens=word_tokenize(text)
            ##keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
            filteredtext_pdf=' '.join([str(elem) for elem in tokens])
            #filteredtext_pdf=' '.join(text.splitlines())
            #print(filteredtext_pdf)
            ##filteredtext=' '.join([str(elem) for elem in keywords]) 
            ##filteredtext.join(keywords)
            file_data.append(filteredtext_pdf)
            i.close()
            
        elif i.name.endswith('.txt'):
            #print(i.read())
            filteredtext_txt=' '.join(i.read().splitlines())             
            #print(filteredtext_txt)
            file_data.append(filteredtext_txt)
            i.close()

    #print(file_data)
    plagiarism_ratio=[]
    plagiarsim_matrix=[]
    similarity_ratio=[]
    
    result=[]
    i=0
    
    for x in range(0,len(file)):
        for z in range(0,x):
            similarity_ratio.append(plagiarsim_matrix[z][x])
        for y in range(x,len(file)):
            if x==y:
                similarity_ratio.append(0)
            else:
                similarity_ratio.append(round(SequenceMatcher(lambda x: x == " ",file_data[x],file_data[y]).ratio(),3))

        plagiarsim_matrix.append(similarity_ratio)
        #print(similarity_ratio)
        #print(plagiarsim_matrix)
        plagiarism_ratio.append(max(similarity_ratio))
        similarity_ratio=[]
        
        print(filename[x]," : ",round(plagiarism_ratio[x]*100,3),"%")  #plagiarism detected
        #result[filename[x]]=round(plagiarism_ratio[x]*100,2)

        result.append([])
        result[i].append(filename[x])
        result[i].append(round(plagiarism_ratio[x]*100,3))
        i=i+1
        #progress_callback.emit(result)
        
    
    return result
        #print(plagiarsim_matrix)
