from DocusignLib import DocusignAuth,DocusignMethods

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('username','password','integratorkey','https://demo.docusign.net/restapi/v2/login_information')

#Now create DocusignMethods Object by passsing the Auth Object
docusignMethods = DocusignMethods(docusignAuthObj)

#Call the EmbedDocusignConsoleView method
response =  docusignMethods.EmbedDocusignConsoleView()

print response


