function initializeShots(scrollTarget) {
	$.ajax({
		type: "GET",
		url: "/shots",
		dataType: "json",
		success: function(data, textStatus, jqXHR) {
			var shotTemplate = '						<li class="panel panel-default" id="shot{{ shot-id }}" shot-id="{{ shot-id }}">\
							<div class="panel-heading">\
								<!--<div class="dropdown pull-right">\
									<a href="#" class="dropdown-toggle" data-toggle="dropdown"><span class="glyphicon glyphicon-th"></span> <b class="caret"></b></a>\
									<ul class="dropdown-menu" role="menu">\
										<li><a href="#" class="addShotBeforeBtn">Add Shot Before</a></li>\
										<li><a href="#" class="addShotAfterBtn">Add Shot After</a></li>\
										<li class="divider"></li>\
										<li><a href="" class="deleteShotBtn">Delete Shot</a></li>\
									</ul>\
								</div>-->\
								<div class="btn-group pull-right">\
									<a href="" class="addShotBeforeBtn btn btn-primary btn-xs" data-toggle="tooltip" data-placement="top" title="Add Shot Before"><span class="glyphicon glyphicon-chevron-up"></span></a>\
									<a href="" class="addShotAfterBtn btn btn-primary btn-xs" data-placement="top" title="Add Shot After"><span class="glyphicon glyphicon-chevron-down"></span></a>\
									<a href="" class="deleteShotBtn btn btn-danger btn-xs" data-placement="top" title="Delete Shot"><span class="glyphicon glyphicon-remove"></span></a>\
								</div>\
\
								<h3 class="panel-title">{{ shot-title }}</h3>\
							</div>\
							<div class="panel-body">\
								<div class="row">\
									<div class="col-xs-12 col-md-8 shot-img">\
										<img src="{{ shot-img-url }}" class="img-responsive"/>\
									</div>\
									<div class="col-xs-12 col-md-4 shot-notes">\
										{{ shot-notes }}\
									</div>\
								</div>\
							</div>\
						</li>';

			if(data[0].id == -1) {
				// we don't have any shots!
				// open the form for them to fill in
				$('#newShotModal').on('show.bs.modal', function(e) {
					$('#newShotProject').val($('#project-title').attr('project-id'));
				});
				$('#newShotModal').on('shown.bs.modal', function(e) {
					$('#newShotTitle').focus();
				});
				$('#newShotModal').modal({
					backdrop: 'static',
					keyboard: false
				});
				$('#newShotIndex').val(0);
				$('#newShotIndexTarget').val("after");
				$('#newShotCancelBtn').click(function(e) {
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
				$('#newShotCloseButton').hide();
				$('#newShotModal').modal('show');
			}
			else {
				for(var shotInfo in data) {
					// set up the shot template
					var shot = shotTemplate.replace("{{ shot-title }}", data[shotInfo].title);
					shot = shot.replace("{{ shot-id }}", data[shotInfo].id);
					shot = shot.replace("{{ shot-id }}", data[shotInfo].id);
					shot = shot.replace("{{ shot-img-url }}", data[shotInfo].img);
					shot = shot.replace("{{ shot-notes }}", marked(data[shotInfo].notes)); // parse the notes as markdown

					// add it
					$('#storyBoardList').append(shot);
				}

				if(scrollTarget != undefined) {
					//alert('scroll target: ' + scrollTarget);
					$('html, body').animate({
						scrollTop: $("#shot" + scrollTarget).offset().top
					}, 1000);
				}

				// allow the shots to be editable
				editableShots();
			}

			$('.addShotBeforeBtn').tooltip();
			$('.addShotAfterBtn').tooltip();
			$('.deleteShotBtn').tooltip();
		},
		error: function(data, textStatus, jqXHR) {
			alert("error, see console");
			console.log(data);
		}
	});
}

$(document).ready(function() {
	initializeShots(undefined);
});