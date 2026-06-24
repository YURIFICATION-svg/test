function addComment() {
  c = document.createElement('p');
  c.innerHTML = document.getElementById('sendmessage').value;
  c.className = "blue";
	document.getElementById('chat').appendChild(c);
  document.getElementById('sendmessage').value = ""
}

function getComment() {
  c = document.createElement('p');
  c.innerHTML = document.getElementById('getmessage').value;
  c.className = "red";
	document.getElementById('chat').appendChild(c);
  document.getElementById('getmessage').value = ""
}
