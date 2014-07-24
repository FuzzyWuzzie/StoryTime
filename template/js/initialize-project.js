$(document).ready(function() {
	$.ajax({
		type: "GET",
		url: "/projects",
		dataType: "json",
		success: function(data, textStatus, jqXHR) {
			$('#project-title').attr('project-id', data.projid);
			$('#project-title').html(data.projname);
		},
		error: function(data, textStatus, jqXHR) {
			alert("error, see console");
			console.log(data);
		}
	});
});