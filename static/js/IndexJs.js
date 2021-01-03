function getTextInput(){return document.getElementById("input").value;}
/*
BOW = 0
NGRAM = 2
STYLE = 3
ALL = 1
*/
var action = document.getElementById("acts");

var enums = {
	"BASIC": "BASIC-BOW",
	"TF-IDF": "TF-IDF-BOW",
	"SVC": "SVC",
	"Random Forest": "RF",
	"Multinomial Naive Bayes": "MNB",
	"Logistic Regression": "LR",
	"ALL IN ONE": "ALL",
	"BOW": null

};
var desc = {
	"BOW": "IN THIS MODEL, A TEXT (SUCH AS A SENTENCE OR A DOCUMENT) IS \
	REPRESENTED AS THE BAG (MULTISET) OF ITS WORDS, DISREGARDING GRAMMAR AND EVEN WORD ORDER BUT KEEPING MULTIPLICITY."
}

function getInput(text,default_val=0.2,min_val=0.01,max_val=0.99){
	do{
		var value = prompt(text,default_val);
		if(value==null)
		  return

		if (value != parseFloat(value, 10) || value <=min_val || value >=max_val)
		  alert("0.01 ve 0.99 arasında bir sayı girin.");
	  
	}while(value != parseFloat(value, 10) || value <=min_val || value >=max_val);

	return parseFloat(value);
  
}

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

function callIfSplit(){
	let endpoint = document.getElementById("acts").value;
	if(endpoint=="split")
		requestToRespondingAction([]);
}
// Additional: BASIC/TF-IDF SVC/RF/MNB CHR/WRD/POS
function requestToRespondingAction(args){
	let endpoint = document.getElementById("acts").value;
	let test_ratio = 0.2;
	if(endpoint=="split")
		test_ratio = getInput("Enter test ratio");

	let request = {
		"text": getTextInput(),
		"args": args,
		"test_ratio": test_ratio
	}
	console.log("Sended JSON: ",request);
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
	console.log("tıklanma çalışıyor");
	currentElement = event.target; 
	current =  getArgFromElement(currentElement);
	args = [current];

	while(current!="ALL IN ONE" && currentElement!=null){
		if(currentElement.tagName=="MENUITEM" && !args.includes(current))
			args.push(current);
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


	requestToRespondingAction(argsArray);



}



