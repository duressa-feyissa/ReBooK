import json 

def parse(data):
	hold = {}
	if "id" in data:
		hold['id'] = data['id']
		hold["title"] = data.get('volumeInfo[title]', "undefined")
		hold["subtitle"] = data.get('volumeInfo[subtitle]', "undefined")
		hold['authors'] = data.get("volumeInfo[authors]", "undefined")
		hold["publisher"] = data.get('volumeInfo[publisher]', "undefined")
		hold["publishedDate"] = data.get('volumeInfo[publishedDate]', "undefined")
		hold["description"] = data.get('volumeInfo[description]', "NO description available")
		hold["pageCount"] = data.get('volumeInfo[pageCount]', "undefined")
		hold["printType"] = data.get('volumeInfo[printType]', "undefined")
		hold["categories"] = data.get('volumeInfo[categories]'  ,'undefined')
		hold["averageRating"] = data.get('volumeInfo[averageRating]', "undefined")
		hold["ratingsCount"] = data.get('volumeInfo[ratingsCount]', "undefined")
		hold["maturityRating"] = data.get('volumeInfo[maturityRating]', "undefined")
		hold["thumbnail"] = data.get('volumeInfo[imageLinks][thumbnail]', "undefined")
		hold["language"] = data.get('volumeInfo[language]', "undefined")
		hold["previewLink"] = data.get('volumeInfo[previewLink]', "undefined")
		hold["volumeInfo"] = data.get('volumeInfo[infoLink]', "undefined")
		hold["scountry"] = data.get('saleInfo[country]', "undefined")
		hold["saleability"] = data.get('saleInfo[saleability]', "undefined")
		hold["isEbook"] =  data.get('saleInfo[isEbook]', "undefined")
		hold["country"] = data.get('accessInfo[country]', "undefined")
		hold["epub"] = data.get("epub", {}).get('accessInfo[epub][isAvailable]', "undefined")
		hold["pdf"] = data.get("pdf", {}).get('accessInfo[pdf][isAvailable]', "undefined")
		hold["viewability"] = data.get('accessInfo[viewability]', "undefined")
		hold["publicDomain"] = data.get('accessInfo[publicDomain]', "undefined")
		hold["embeddable"] = data.get('accessInfo[embeddable]', "undefined")
		hold["textToSpeechPermission"] = data.get('accessInfo[textToSpeechPermission]', "undefined")
		hold["webReaderLink"] = data.get('accessInfo[webReaderLink]', "undefined")
		hold["accessViewStatus"] = data.get('accessInfo[accessViewStatus]', "undefined")
		hold["quoteSharingAllowed"] = data.get('accessInfo[quoteSharingAllowed]', "undefined")
		hold["textSnippet"] = data.get('searchInfo[textSnippet]', "undefined")
	return hold
