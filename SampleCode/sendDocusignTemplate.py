from DocusignLib import *

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('rodddy57@gmail.com','angel0121','RODX-d68b779e-5b41-44b0-8bac-1fcf1301a968','https://demo.docusign.net/restapi/v2/login_information')

#Now Create DocusignMethods Object and Pass the DocusignAuthObj to it
docusignMethod = DocusignMethods(docusignAuthObj) 

tempData = RequestSignatureData()
tempData.status = 'sent'
tempData.emailSubject = "Hello howdy";
tempData.emailBlurb = "From Jady";
tempData.templateId = '62AF9A9C-0794-40E1-822F-5F070151D790'


obj = []
obj.append(TemplateRole('123','','Admin','jake','jay3dec@gmail.com'))

tempData.templateRoles = obj

response = docusignMethod.sendDocusignTemplate(tempData)
print response


