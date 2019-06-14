function addChar(input, character) {
	if(input.value == null || input.value == "enter")
		input.value = character
	else{
		if(character === 'n'){
			console.log('nir is pressed');
		}
		input.value += character
	}
}

function deleteChar(input) {
	input.value = input.value.substring(0, input.value.length - 1)
}

function cos(input) {
	if(input.value=="enter")
		input.value='cos('
	else 
	    input.value =input.value +'cos('
}

function sin(input) {
	if(input.value=="enter")
		input.value='sin('
	else 
	    input.value =input.value +'sin('
}

function tan(input) {
	if(input.value=="enter")
		input.value='tan('
	else 
	    input.value =input.value +'tan('
}

function sqrt(input) {
	if(input.value=="enter")
		input.value='sqrt('
	else 
	   input.value =input.value +'sqrt('
}

function log(input) {
	if(input.value=="enter")
		input.value='log('
	else 
	    input.value =input.value +'log('
}

function exp(input) {
	if(input.value=="enter")
		input.value='exp('
	else 
	    input.value =input.value +'exp('
}

function power(input) {
	if(input.value=="enter")
		input.value='pow('
	else 
	    input.value =input.value +'pow('
}



function pi(input){
	if(input.value=="enter")
		input.value='PI'
	else 
	    input.value =input.value +'PI'}


function ceil(input){
	if(input.value=="enter")
		input.value='ceil('
	else 
	    input.value =input.value +'ceil('}

function floor(input){
	if(input.value=="enter")
		input.value='floor('
	else 
	   input.value =input.value +'floor('}


function percent(input){
	input.value=input.value + '%(';}












