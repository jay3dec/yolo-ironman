from DocusignLib import DocusignAuth,DocusignMethods,RequestSignatureData,TemplateRole

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('rodddy57@gmail.com','angel0121','RODX-d68b779e-5b41-44b0-8bac-1fcf1301a968','https://demo.docusign.net/restapi/v2/login_information')

#Now create DocusignMethods Object by passsing the Auth Object
docusignMethods = DocusignMethods(docusignAuthObj)

tempData = RequestSignatureData()
tempData.status = 'created'
tempData.emailSubject = "Hello howdy";
tempData.emailBlurb = "From Jady";
tempData.templateId = '62AF9A9C-0794-40E1-822F-5F070151D790'
obj = []
obj.append(TemplateRole('','','Reader','jim','italespinner@gmail.com'))
tempData.templateRoles = obj

#Call the EmbeddedSigning method passing RequestSignatureData object and Username
response =  docusignMethods.EmbeddedSigning(tempData,"rodddy57@gmail.com","http://www.google.com")

print response


