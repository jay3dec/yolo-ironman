from DocusignLib import *

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('rodddy57@gmail.com','angel0121','RODX-d68b779e-5b41-44b0-8bac-1fcf1301a968','https://demo.docusign.net/restapi/v2/login_information')

#Now Create DocusignMethods Object and Pass the DocusignAuthObj to it
docusignMethod = DocusignMethods(docusignAuthObj) 

tempData = RequestSignatureData()
tempData.status = 'sent'
tempData.emailSubject = "Hello howdy";
tempData.emailBlurb = "From Jady";


#Creating Document 
docList = []
docList.append(Document('test_doc.txt','1'))

tempData.documents = docList

#Creating SignHereTabList
signHereTBList = []
signHereTB = SignHereTab('100','100','1','1')
signHereTBList.append(signHereTB)

#Creating SignHere List
signerList = []
sign = Signer('name','jay3dec@gmail.com','1',signHereTBList)
signerList.append(sign)

tempData.recipients = signerList
tempData.signHereTabs = signHereTB

#Calling SendDocumentForSignature
response = docusignMethod.SendDocumentForSignature(tempData,'hello.txt')
print response


