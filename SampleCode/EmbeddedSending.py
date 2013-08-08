from DocusignLib import DocusignAuth,DocusignMethods,RequestSignatureData,TemplateRole

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('username','password','integratorkey','https://demo.docusign.net/restapi/v2/login_information')

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
response =  docusignMethods.EmbeddedSending(tempData,"rodddy57@gmail.com","http://www.google.com")

print response


