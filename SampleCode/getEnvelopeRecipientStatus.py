from DocusignLib import DocusignAuth,DocusignMethods

#Create the DocusignAuth Object using Username,Password,Integrator Key,Docusign Login Url
docusignAuthObj = DocusignAuth('username','password','integratorkey','https://demo.docusign.net/restapi/v2/login_information')

#Now create DocusignMethods Object by passsing the Auth Object
docusignMethods = DocusignMethods(docusignAuthObj)

#Call the GetEnvelopeRecipientStatus method passing the Envelope Id
response =  docusignMethods.GetEnvelopeRecipientStatus('8db590e9-ed97-4fd1-9f74-51e8a7a3174b')

print response


