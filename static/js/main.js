
function printView(){
	const id = document.getElementById('id').value;
	document.getElementById('resultId').innerText = id;

	const type = document.getElementById('type').value;
	document.getElementById('resultType').innerText = type;

	const tag = document.getElementById('tag').value;
	document.getElementById('resultTag').innerText = tag;
	// document.getElementById('resultTag').style.color = 'black';
}
const submit = document.querySelector('.submit');
submit.addEventListener("click", printView);
