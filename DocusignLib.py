import sys, httplib2, json
class DocusignAuth:
	def __init__(self,username,password,integratorKey,url):
		self.AuthenticateStr = "<DocuSignCredentials>" \
					"<Username>" + username + "</Username>" \
					"<Password>" + password + "</Password>" \
					"<IntegratorKey>" + integratorKey + "</IntegratorKey>" \
					"</DocuSignCredentials>";
		self.Url = url;

class RequestSignatureData:
	accountId = ''
	status = ''
	emailSubject = ''
	emailBlurb = ''
	customFields = ''
	templateId = ''
	brandId = ''
	documents = []
	recipients = ''
	templateRoles = []
	messageLock = ''

class ListCustomFields:
	def __init__(self,listItems,value,required,show,name):
		self.listItems = listItems
		self.value = value
		self.required = required
		self.show = show
		self.name = name

class TextCustomFields:
	def __init__(self,value,required,show,name):
		self.value = value;
		self.required = required
		self.show = show
		self.name = name

class CustomFields:
	listCustomFields = []
	textCustomFields = []

class TemplateRole:
	def __init__(self,accessCode,client,roleName,name,email):
		self.accessCode = accessCode
		self.clientUserId = client
		self.roleName = roleName
		self.name = name
		self.email = email

class Document:
	def __init__(self,name,documentId):
		self.name = name
		self.documentId = documentId

class Signer:
	def __init__(self,name,email,recipientId,tabList):
		self.name = name
		self.email = email
		self.recipientId = recipientId
		self.tabs = tabList

class Tabs:
	def __init__(self,signHereTabList):
		self.tabs = signHereTabList

class SignHereTab:
	def __init__(self,xPosition,yPosition,documentId,pageNumber):
		self.xPosition = xPosition
		self.yPosition = yPosition
		self.documentId = documentId
		self.pageNumber = pageNumber

class DocusignMethods:
	def __init__(self,docusignObj):
		self.Docusign = docusignObj
		
	def sendDocusignTemplate(self,customData):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'}
		http = httplib2.Http(disable_ssl_certificate_validation=True)
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers)
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];

		customData.accountId = accountId

		#
		# STEP 2 - Create an Envelope with a Recipient and Send...
		#
 
		#construct the body of the request in JSON format
	
		listCustomFields = []
		if len(customData.customFields) > 0:
			for i in range(0,len(customData.customFields.listCustomFields)):
				listItems = []
				for j in range(0,len(customData.customFields.listCustomFields[i].listItems)):
						listItems.append(customData.customFields.listCustomFields[i].listItems[j])
				listField = {"listItems":listItems,
						"value":customData.customFields.listCustomFields[i].value,
						"required":customData.customFields.listCustomFields[i].required,
						"show":customData.customFields.listCustomFields[i].show,
						"name":customData.customFields.listCustomFields[i].name
					}
				listCustomFields.append(listField)
		#if len(listCustomFields) > 0:
		customFields = {"listCustomFields":listCustomFields}
		templateRoles = []
		for i in range(0,len(customData.templateRoles)):
			role = {"accessCode":customData.templateRoles[i].accessCode,
					"clientUserId":customData.templateRoles[i].clientUserId,
					"roleName":customData.templateRoles[i].roleName,
					"name":customData.templateRoles[i].name,
					"email":customData.templateRoles[i].email
					}
			templateRoles.append(role)

		requestBody1 = json.dumps({"accountId":accountId,
			"emailSubject":customData.emailSubject,
			"emailBlurb":customData.emailBlurb,
			"customFields":customFields,
			"templateId":customData.templateId,
			"brandId":customData.brandId,
			"templateRoles":templateRoles,
			"status":customData.status,
			"messageLock":customData.messageLock})

		requestBody = json.dumps({key: value for key, value in [
        			("accountId",accountId),
        			("emailSubject",customData.emailSubject),
        			("emailBlurb",customData.emailBlurb),
        			("customFields",customFields),
				("templateId",customData.templateId),
				("brandId",customData.brandId),
				("templateRoles",templateRoles),
        			("status",customData.status),
        			("messageLock",customData.messageLock),] if value})

		
				
 
		# append "/envelopes" to baseURL and use in the request
		
		url = baseUrl + "/envelopes";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'}
		http = httplib2.Http(disable_ssl_certificate_validation=True)
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
		return content
 
		

	def SendDocumentForSignature(self,customData,filename):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			 return "Error calling webservice, status is: %s" % status;
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
 
		#
		# STEP 2 - Add Signature Request to Document and Send
		#
	 
		#construct the body of the request in JSON format

		
		

		documentList = []
		for i in range(0,len(customData.documents)):
			doc = {"documentId":customData.documents[i].documentId,
					"name":customData.documents[i].name
					}
			documentList.append(doc)

		signHereTabList = []
		signerList = [];
		for i in range(0,len(customData.recipients)):
			for j in range(0,len(customData.recipients[i].tabs)):
					signHereTab = {"xPosition":customData.recipients[i].tabs[j].xPosition,
							"yPosition":customData.recipients[i].tabs[j].yPosition,
							"documentId":customData.recipients[i].tabs[j].documentId,
							"pageNumber":customData.recipients[i].tabs[j].pageNumber
							}
					signHereTabList.append(signHereTab)
			dt = {"signHereTabs":signHereTabList}
			row = {"name":customData.recipients[0].name,
					"email":customData.recipients[0].email,
					"recipientId":customData.recipients[0].recipientId,
					"tabs":dt
					}
			signerList.append(row)

		recip = {"signers":signerList}
		

		envelopeDef = json.dumps({key: value for key, value in [
        			("accountId",accountId),
				("emailSubject",customData.emailSubject),
				("emailBlurb",customData.emailBlurb),
				("documents",documentList),
				("recipients",recip),
				("brandId",customData.brandId),
				("status",customData.status),] if value})

 
		# convert the file into a string and add to the request body
		fileContents = open(filename, "r").read();
 
		requestBody = "\r\n\r\n--BOUNDARY\r\n" + \
                		"Content-Type: application/json\r\n" + \
                		"Content-Disposition: form-data\r\n" + \
                		"\r\n" + \
                		envelopeDef + "\r\n\r\n--BOUNDARY\r\n" + \
                		"Content-Type: text/plain\r\n" + \
                		"Content-Disposition: file; filename=\"test_doc.txt\"; documentId=1\r\n" + \
                		"\r\n" + \
                		fileContents + "\r\n" + \
                		"--BOUNDARY--\r\n\r\n";
 
		# append "/envelopes" to the baseUrl and use in the request
		url = baseUrl + "/envelopes";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Content-Type': 'multipart/form-data; boundary=BOUNDARY', 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			errorMsg = "Error calling webservice, status is: %s\nError description - %s" % (status, content);
			return errorMsg;
		data = json.loads(content);
		envId = data.get('envelopeId');
 
		return content

	def GetEnvelopeInformation(self,envelopeId):
		envelopeUri = "/envelopes/" + envelopeId;
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
		#
		# STEP 2 - Request Envelope Info
		#
 
		# append envelopeUri to baseURL and use in the request
		url = baseUrl + envelopeUri;
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'GET', headers=headers);
		status = response.get('status');
                
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
		return data

	def GetEnvelopeRecipientStatus(self,envelopeId):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		

		#
		# STEP 2 - Request Envelope Status using url query string 
		#
 
		# append "/envelopes" + query string to the URL
		url = baseUrl + '/envelopes/' + envelopeId + '/recipients';
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'GET', headers=headers);
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		#--- display results
		return content;


	def GetEnvelopeStatus(self,from_date,envStatus):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
 		from_date = from_date.replace('/','%2F').replace(' ','%20').replace(':','%3A')
		
		#
		# STEP 2 - Request Envelope Status using url query string 
		#
 
		# append "/envelopes" + query string to the URL
		url = baseUrl + '/envelopes?from_date='+from_date+'&status=' + envStatus;
		
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'GET', headers=headers);
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		return content

	def GetDownListAndDownLoadDoc(self,envelopeId):
		envelopeUri = "/envelopes/" + envelopeId;
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			error ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
 
		#
		# STEP 2 - Get Envelope Document(s) Info and Download Documents
		#
 
		# append envelopeUri to baseURL and use in the request
		url = baseUrl + envelopeUri + "/documents";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'GET', headers=headers);
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
 
		envelopeDocs = data.get('envelopeDocuments');
		uriList = [];
		for docs in envelopeDocs:
    		# print document info
    			uriList.append(docs.get("uri"));
    			#print("Document Name = %s, Uri = %s" % (docs.get("name"), uriList[len(uriList)-1]));
    
    			# download each document
    			url = baseUrl + uriList[len(uriList)-1];
    			headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr};
    			http = httplib2.Http(disable_ssl_certificate_validation=True);
    			response, content = http.request(url, 'GET', headers=headers);
    			status = response.get('status');
    			if (status != '200'): 
        			return ("Error calling webservice, status is: %s" % status);
    			fileName = "doc_" + str(len(uriList)) + ".pdf";
    			file = open(fileName, 'w');
    			file.write(content);
    			file.close();
 
		return data
	def EmbeddedSending(self,customData,username,returnUrl):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
 
		#
		# STEP 2 - Request Envelope Info
		#
 


		listCustomFields = []
		if len(customData.customFields) > 0:
			for i in range(0,len(customData.customFields.listCustomFields)):
				listItems = []
				for j in range(0,len(customData.customFields.listCustomFields[i].listItems)):
						listItems.append(customData.customFields.listCustomFields[i].listItems[j])
				listField = {"listItems":listItems,
						"value":customData.customFields.listCustomFields[i].value,
						"required":customData.customFields.listCustomFields[i].required,
						"show":customData.customFields.listCustomFields[i].show,
						"name":customData.customFields.listCustomFields[i].name
					}
				listCustomFields.append(listField)

		customFields = {"listCustomFields":listCustomFields}
		templateRoles = []
		for i in range(0,len(customData.templateRoles)):
			role = {"accessCode":customData.templateRoles[i].accessCode,
					"clientUserId":customData.templateRoles[i].clientUserId,
					"roleName":customData.templateRoles[i].roleName,
					"name":customData.templateRoles[i].name,
					"email":customData.templateRoles[i].email
					}
			templateRoles.append(role)

		requestBody = json.dumps({"accountId":accountId,
			"emailSubject":customData.emailSubject,
			"emailBlurb":customData.emailBlurb,
			"templateId":customData.templateId,
			"templateRoles":templateRoles,
			"status":customData.status
			})		
		



		#construct the body of the request in JSON format  
		requestBody1 = "{\"accountId\": \"" + accountId + "\"," + \
                	"\"status\": \"created\"," + \
                	"\"emailSubject\": \"API Call for sending signature request from template\"," + \
                	"\"emailBlurb\": \"This comes from Python\"," + \
                	"\"templateId\": \"" + customData.templateId + "\"," + \
                	"\"templateRoles\": [{" + \
                	"\"email\": \"" + username + "\"," + \
                	"\"name\": \"John Doe\"," + \
                	"\"roleName\": \"Role\" }] }";
 
		# append "/envelopes" to baseURL and use in the request
		url = baseUrl + "/envelopes";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
 
		# store the uri for next request
		uri = data.get('uri');
 
		#
		# STEP 3 - Get the Embedded Send View
		#
 
		#construct the body of the request in JSON format  
		requestBody =   "{ \"authenticationMethod\": \"email\"," + \
                	"\"email\": \"" + username + "\"," + \
                	"\"returnUrl\": \"" + returnUrl +"\"," + \
                	"\"userName\": \"John Doe\"," + \
                	"\"clientUserId\": \"1\" }";
 
		# append uri + "/views/sender" to the baseUrl and use in the request
		url = baseUrl + uri + "/views/sender";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
		return data
	
	def EmbeddedSigning(self,customData,username,returnUrl):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
		#
		# STEP 2 - Request Envelope Info
		#


		listCustomFields = []
		if len(customData.customFields) > 0:
			for i in range(0,len(customData.customFields.listCustomFields)):
				listItems = []
				for j in range(0,len(customData.customFields.listCustomFields[i].listItems)):
						listItems.append(customData.customFields.listCustomFields[i].listItems[j])
				listField = {"listItems":listItems,
						"value":customData.customFields.listCustomFields[i].value,
						"required":customData.customFields.listCustomFields[i].required,
						"show":customData.customFields.listCustomFields[i].show,
						"name":customData.customFields.listCustomFields[i].name
					}
				listCustomFields.append(listField)

		customFields = {"listCustomFields":listCustomFields}
		templateRoles = []
		for i in range(0,len(customData.templateRoles)):
			role = {"accessCode":customData.templateRoles[i].accessCode,
					"clientUserId":customData.templateRoles[i].clientUserId,
					"roleName":customData.templateRoles[i].roleName,
					"name":customData.templateRoles[i].name,
					"email":customData.templateRoles[i].email
					}
			templateRoles.append(role)

		requestBody = json.dumps({"accountId":accountId,
			"emailSubject":customData.emailSubject,
			"emailBlurb":customData.emailBlurb,
			"templateId":customData.templateId,
			"templateRoles":templateRoles,
			"status":customData.status
			})		
		


 
 
		# append "/envelopes" to baseURL and use in the request
		url = baseUrl + "/envelopes";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
 
		# store the uri for next request
		uri = data.get('uri');
 
		#
		# STEP 3 - Get the Embedded Send View
		#
 
		#construct the body of the request in JSON format  
		requestBody =   "{ \"authenticationMethod\": \"email\"," + \
                		"\"email\": \"" + username + "\"," + \
                		"\"returnUrl\": \"" + returnUrl + "\"," + \
                		"\"userName\": \"John Doe\"," + \
                		"\"clientUserId\": \"1\" }";
 
		# append uri + "/views/sender" to the baseUrl and use in the request
		url = baseUrl + uri + "/views/sender";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
		return data

	def EmbedDocusignConsoleView(self):
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json'};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(self.Docusign.Url, 'GET', headers=headers);
 
		status = response.get('status');
		if (status != '200'): 
    			return ("Error calling webservice, status is: %s" % status);
 
		# get the baseUrl and accountId from the response body
		data = json.loads(content);
		loginInfo = data.get('loginAccounts');
		D = loginInfo[0];
		baseUrl = D['baseUrl'];
		accountId = D['accountId'];
 
		
 
		#
		# STEP 2 - Get Console View
		#
 
		#construct the body of the request in JSON format.  In this case all we need is the accountId  
		requestBody = "{\"accountId\": \"" + accountId + "\"}";
 
		# append "/views/console" to the baseUrl and use in the request
		url = baseUrl + "/views/console";
		headers = {'X-DocuSign-Authentication': self.Docusign.AuthenticateStr, 'Accept': 'application/json', 'Content-Length': str(len(requestBody))};
		http = httplib2.Http(disable_ssl_certificate_validation=True);
		response, content = http.request(url, 'POST', headers=headers, body=requestBody);
		status = response.get('status');
		if (status != '201'): 
    			return ("Error calling webservice, status is: %s" % status);
		data = json.loads(content);
		return data
