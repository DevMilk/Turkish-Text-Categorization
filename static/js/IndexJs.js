function getInput(){return document.getElementById("input").value;}
/*
BOW = 0
NGRAM = 2
STYLE = 3
ALL = 1
*/

function POST(endpoint, requestBody,handleFunc){
	const xhr = new XMLHttpRequest();   // new HttpRequest instance 
	xhr.open("POST", endpoint);
	xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(requestBody));

    xhr.onreadystatechange = function () {
      if (this.readyState === 4   && 
		  this.status     ==  200 &&
  	      this.status < 300) {
			  if(this.responseText=="")
				  return
			  handleFunc(JSON.parse(this.responseText));
		  }
    }
}

var enums = {
	"BASIC": "BASIC-BOW",
	"TF-IDF": "TF-IDF-BOW",
	"STYLE-BASED":"STYLE-BASED",
	"SVC": "SVC",
	"Random Forest": "RF",
	"Multinomial Naive Bayes": "MNB",
	"Logistic Regression": "LR",
	"LR": "LR",

	"Character Based": "CHR",
	"Word Based" : "WRD",
	"POS Based" : "POS",

	"ALL IN ONE": "ALL",
	"NGRAM": "NGRAM",
	"BOW": null

};
var desc = {
	"BOW": "IN THIS MODEL, A TEXT (SUCH AS A SENTENCE OR A DOCUMENT) IS \
	REPRESENTED AS THE BAG (MULTISET) OF ITS WORDS, DISREGARDING GRAMMAR AND EVEN WORD ORDER BUT KEEPING MULTIPLICITY.",
	"NGRAM": "NGRAM IS A METHOD THAT EXTRACTS MOST FREQUENT WORD, CHARACTER OR POS TAGS TO \
		IDENTIFY DOCUMENT",
	"STYLE-BASED": "STYLE BASED CLASSIFICATION USES DOZENS OF ATTRIBUTES OF TEXT SUCH AS TOTAL SENTENCES IN TEXT, \
	AVERAGE WORD LENGTH IN TEXT, NOUN COUNT, VERB COUNT ETC. "

}
// Additional: BASIC/TF-IDF SVC/RF/MNB CHR/WRD/POS
function predict(args){
	let input = getInput();
	let request = {
		"text": input,
		"args": args
	}
	console.log("Sended JSON: ",request);
	endpoint = document.getElementById("acts").value;
	POST("/"+endpoint,request,function(responseArray){document.getElementById("prediction").innerText=responseArray[0];})

}

function getArgFromElement(element){
	return element.innerText.split("\n")[0];
}
function getTag(element){
	return element.getElementsByTagName("a")[0];
}
function getParent(element){
	return element.parentNode;
}

let descriptionLoc = document.getElementById("description");
function click(event){
	currentElement = event.target; 
	current =  getArgFromElement(currentElement);
	args = [current];

	while(current!="ALL IN ONE" && currentElement!=null){
		if(currentElement.tagName=="MENUITEM" && !args.includes(current))
			args.push(current);
		if(desc[current]!=null)
			descriptionLoc.innerText = desc[current];
		currentElement = getParent(currentElement);
		current = getArgFromElement(currentElement);
	}

	


	let argsArray = []
	if(args.length!=0){
		for(var i = 0;i<args.length;i++){
			if(enums[args[i]]!=null)
				argsArray.push(enums[args[i]])
		}
	}
	predict(argsArray);



}
var items = document.getElementsByTagName("a");

for(var i=0;i<items.length;i++){
	items[i].onclick = click;
}



