//function appendHeader(div) {
//	$(div).load('header')
//};
//
//$(document).ready(
//	appendHeader('#header')
//)
//

$('#btnSave').on('click', function(url) {
	var href = $(this).attr('href')
	var textSave = $('p#textSave').text()
	
	alert(href+textSave)
	
	$(this).attr('href',href+textSave)
})