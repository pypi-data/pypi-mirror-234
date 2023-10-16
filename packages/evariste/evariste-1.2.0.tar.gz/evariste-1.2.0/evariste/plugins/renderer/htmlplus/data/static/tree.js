function toggle_visibility(id) {
  var element = document.getElementById(id);
  if(element.style.display == 'block')
    element.style.display = 'none';
  else
    element.style.display = 'block';
}

function toggle_openclosed(id) {
  var element = document.getElementById(id);
  if(element.classList.contains('open')) {
    element.classList.remove('open');
    element.classList.add('closed');
  } else {
    element.classList.remove('closed');
    element.classList.add('open');
  }
}
