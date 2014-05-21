//	var id = $(this).data('id')


{% if user %}
$('#comment').submit(function(e) {
	e.preventDefault()
	var comment = $('#taComment').val();
	
	if (comment.length == 0) {
		alert("La longitud debe ser mayor que 0.")
	}
	
	doComment(comment, function(data) {
		var id = '{{post.key.id()}}'
		var comment_author = '{{user.nickname().capitalize().split("@")[0]}}'
		var date = 'Hace un instante'

		toAppend = 
			'<div class="panel panel-default">'
				+ '<div class="panel-heading">'
					+ date 
					+ ' - <strong>' + comment_author + '</strong>' 
					+ ' ha escrito:'
				+ '</div>'
				+ '<div class="panel-body">' + comment
				+ '</div></div>'
				
		$('#comments').prepend(toAppend)
	});
	
	$('#taComment').val("")
})
{% endif %}



function doComment(comment, done) {
	$.ajax({
		type: 'POST',
		data: { 'id': {{post.key.id()}}, 'comment': comment},
		url: '/comment',
	})
	.done(done)
//	.fail(fail)
}