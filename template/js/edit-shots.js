function editableShots() {
	Hammer($('.panel-title')[0]).on("doubletap", function(e) {
		$(e.target).html("<input type='text' class='editing-title' value='" + $(e.target).text() + "'></input>");
		$('.editing-title').focus();
		$('.editing-title').blur(function(blurEvent) {
			var editedText = $(blurEvent.target).val();

			// and send an AJAX request to update the shot notes
			$.ajax({
				type: "POST",
				url: "/shots",
				dataType: "json",
				data: {
					"shotID": $(blurEvent.target).parents('li').attr('shot-id'),
					"field": "title",
					"value": editedText
				},
				success: function(data, textStatus, jqXHR) {
					$(blurEvent.target).parents('.panel-title').html(data.title);
				},
				error: function(data, textStatus, jqXHR) {
					alert("error, see console");
					console.log(data);
				}
			});
		});
	});
	
	Hammer($('.shot-img')[0]).on("doubletap", function(e) {
	//$('.shot-img').dblclick(function(e) {
		var currentPath = $(e.target).attr('src');
		var hostContainer = $(e.target).parents('.shot-img');
		var shotID = $(hostContainer).parents('li').attr('shot-id');
		console.log("shot id:" + shotID);
		if(currentPath == undefined) {
			currentPath = $(e.target).children('img').attr('src');
			hostContainer = $(e.target);
		}
		$(hostContainer).html('<img src="' + currentPath + '" class="img-responsive"/><br/><input id="uploadedFile" type="file" name="uploadedFile" data-url="/upload" accept="image/*">');

		$('#uploadedFile').fileupload({
			dataType: 'json',
			formData: {
				shotID: shotID
			},
			done: function(e, data) {
				$(hostContainer).html('<img src="' + data.result.url + '" class="img-responsive"/>');
			}
		});
	});

	Hammer($('.shot-notes')[0]).on("doubletap", function(e) {
	//$('.shot-notes').dblclick(function(e) {
		$.ajax({
			type: "GET",
			url: "/shots",
			dataType: "json",
			data: {
				"shotID": $(e.target).parents('li').attr('shot-id')
			},
			success: function(data, textStatus, jqXHR) {
				$(e.target).parents('.shot-notes').html("<textarea class='editing-notes form-control'>" + data.notes + "</textarea>");
				$('.editing-notes').elastic();
				$('.editing-notes').focus();
				$('.editing-notes').blur(function(blurEvent) {
					var editedText = $(blurEvent.target).val();

					// and send an AJAX request to update the shot notes
					$.ajax({
						type: "POST",
						url: "/shots",
						dataType: "json",
						data: {
							"shotID": $(blurEvent.target).parents('li').attr('shot-id'),
							"field": "notes",
							"value": editedText
						},
						success: function(data, textStatus, jqXHR) {
							$(blurEvent.target).parents('.shot-notes').html(marked(data.notes));
						},
						error: function(data, textStatus, jqXHR) {
							alert("error, see console");
							console.log(data);
						}
					});

				});
			},
			error: function(data, textStatus, jqXHR) {
				alert("error, see console");
				console.log(data);
			}
		});
	});

	function showNewShot(ndx, beforeAfter) {
		// set the various fields in the modal
		$('#newShotModal').on('show.bs.modal', function(e) {
			$('#newShotProject').val($('#project-title').attr('project-id'));
		});
		$('#newShotIndex').val(ndx);
		$('#newShotIndexTarget').val(beforeAfter);

		// focus the title when it opens
		$('#newShotModal').on('shown.bs.modal', function(e) {
			$('#newShotTitle').focus();
		});

		// allow the dialog to be closed
		$('#newShotCloseButton').show();
		$('#newShotModal').modal({
			backdrop: true,
			keyboard: true
		});

		$('#newShotCancelBtn').click(function(e) {
			e.stopPropagation();
			e.preventDefault();
			$('#newShotModal').modal('hide');
		});
		$('#newShotModal').modal('show');
	}

	$('.addShotAfterBtn').click(function(e) {
		e.stopPropagation();
		e.preventDefault();

		// we don't have any shots!
		showNewShot($(e.target).parents('li.panel').attr('shot-id'), 'after');
	});

	$('.addShotBeforeBtn').click(function(e) {
		e.stopPropagation();
		e.preventDefault();

		// we don't have any shots!
		showNewShot($(e.target).parents('li.panel').attr('shot-id'), 'before');
	});

	$('.deleteShotBtn').click(function(e) {
		e.stopPropagation();
		e.preventDefault();

		//alert('shot id: ' + $(e.target).parents('li').attr('shot-id'));
		$.ajax({
			type: "DELETE",
			url: "/shots" + '?' + $.param({"shotID": $(e.target).parents('li.panel').attr('shot-id')}),
			dataType: "json",
			success: function(data, textStatus, jqXHR) {
				// it worked, refresh the page
				window.location = '/';
			},
			error: function(data, textStatus, jqXHR) {
				alert("error, see console");
				console.log(data);
			}
		});
	});
}