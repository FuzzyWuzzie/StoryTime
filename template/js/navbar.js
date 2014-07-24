$(document).ready(function() {
	$('#changeProjectBtn').click(function(e) {
		e.stopPropagation();
		e.preventDefault();

		$.ajax({
			type: "POST",
			url: "/projects",
			dataType: "json",
			data: {
				"projid": -1
			},
			success: function(data, textStatus, jqXHR) {
				window.location = '/';
			},
			error: function(data, textStatus, jqXHR) {
				alert("error, see console");
				console.log(data);
			}
		});
	});
});