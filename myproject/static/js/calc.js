//================================================== changes ======================================================
function clearCalcScreen()
{
    document.getElementById('display').value='';
}
//================================================== changes ======================================================
function addChar(character) { //================================================== changes ======================================================
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	//================================================== changes ======================================================
	if(input.value == null || input.value == "enter")
		input.value = character
	else{
		if(character === 'n'){
			console.log('nir is pressed');
		}
		input.value += character
	}
}

function deleteChar() {//================================================== changes ======================================================
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	//================================================== changes ======================================================
	input.value = input.value.substring(0, input.value.length - 1)
}

function cos() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='cos('
	else 
	    input.value =input.value +'cos('
}

function sin() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='sin('
	else 
	    input.value =input.value +'sin('
}

function tan() {
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='tan('
	else 
	    input.value =input.value +'tan('
}

function sqrt() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='sqrt('
	else 
	   input.value =input.value +'sqrt('
}

function log() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='log('
	else 
	    input.value =input.value +'log('
}

function exp() {
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='exp('
	else 
	    input.value =input.value +'exp('
}

function power() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='pow('
	else 
	    input.value =input.value +'pow('
}



function pi() {
	//================================================== changes ======================================================	
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='PI'
	else 
	    input.value =input.value +'PI'}


function ceil() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='ceil('
	else 
	    input.value =input.value +'ceil('}

function floor() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	if(input.value=="enter")
		input.value='floor('
	else 
	   input.value =input.value +'floor('}


function percent() { 
	//================================================== changes ======================================================
	let input = document.getElementById('display');
	input.value=input.value + '%(';
}












