from DocusignLib import DocusignAuth,DocusignMethods

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('rodddy57@gmail.com','angel0121','RODX-d68b779e-5b41-44b0-8bac-1fcf1301a968','https://demo.docusign.net/restapi/v2/login_information')

#Now create DocusignMethods Object by passsing the Auth Object
docusignMethods = DocusignMethods(docusignAuthObj)

#Call the EmbedDocusignConsoleView method
response =  docusignMethods.EmbedDocusignConsoleView()

print response


