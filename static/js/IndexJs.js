function getTextInput(){return document.getElementById("input").value;}
/*
BOW = 0
NGRAM = 2
STYLE = 3
ALL = 1
*/
var action = document.getElementById("acts");
function predLoc(){
	return document.getElementById("prediction");
}
var enums = {
	"BASIC": "BASIC-BOW",
	"TF-IDF": "TF-IDF-BOW",
	"SVC": "SVC",
	"Random Forest": "RF",
	"Multinomial Naive Bayes": "MNB",
	"Logistic Regression": "LR",
	"ALL IN ONE": "ALL",
	"XGBoost": "XGB",
	"Nearest Centroid": "NC",
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
    xhr.timeout = 60*1000;

    xhr.onreadystatechange = function () {
      if (this.readyState === 4   && 
		  this.status     ==  200 &&
  	      this.status < 300) {
			  if(this.responseText=="")
				  return
			  handleFunc(JSON.parse(this.responseText.replace(/\bNaN\b/g, "null")));
		  }
	  else if(this.status==500){
	  	predLoc().innerText="SERVER ERROR"
	  }
    }
}

function callIfSplit(){
	let endpoint = document.getElementById("acts").value;
	if(endpoint=="split")
		requestToRespondingAction([]);
}

function wait() {
  return new Promise(resolve => {
    resolve();
  });
}

var currentArgs;
async function destroyAndReturn(){


	request = {"args": currentArgs,"params":null}
	let formElement = document.getElementById("form");
	let inputs = formElement.getElementsByTagName("input");
	let obj = {}
	for(let i=0;i<inputs.length;i++)
		if(inputs[i].value!="null")
			obj[inputs[i].name] = parseFloat(inputs[i].value)
	request["params"] = obj;

	predLoc().innerText = "Training..."
	await wait();
	POST("/train",request,function(responseArray){predLoc().innerText=responseArray[0];})
	formElement.remove()
}

//Ask for parameters before training
function askForParams(paramSet){

	let currentParams = paramSet[0]

	function createInput(name,value){
		return '<label for="'+name+'">'+name+'</label><br> \
    	<input type="text" id="'+name+'" name="'+name+'" value = "'+value+'"><br> '
	}

	let start = '<div id="form" >';
	let end = '<button onclick="destroyAndReturn();">send</button> </div>';
	for(let key in currentParams) 
		if(parseFloat(currentParams[key])|| currentParams[key]==0)
  			start+=createInput(key,currentParams[key]);
	
	start+=end;
	document.getElementById("parameters").innerHTML =start;
	document.getElementById("form").focus();
}


async function requestToRespondingAction(args){


	let endpoint = document.getElementById("acts").value;
	predLoc().innerText = (endpoint+"ing...").toUpperCase()
	await wait();

	let request = {
		"text": getTextInput(),
		"args": args,
	}
	if(endpoint=="train"){
		currentArgs = args
		predLoc().innerText = "Enter parameters"
		await wait();
		POST("/"+"param",request,askForParams)
		return;
	}
	if(endpoint=="split"){
		test_ratio = getInput("Enter test ratio");
		request = {"test_ratio": test_ratio}
	}
	endpoint = endpoint.toLowerCase()
	POST("/"+endpoint,request,function(responseArray){predLoc().innerText=responseArray[0];})

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
async function elementHiden(element){
	element.style.visibility = element.style.visibility == "hidden" ? "visible": "hidden";
	await wait();
}

let descriptionLoc = document.getElementById("description");
function click(event){

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



