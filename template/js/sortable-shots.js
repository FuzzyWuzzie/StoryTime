jQuery(function($) {
	var panelList = $('#storyBoardList');

	panelList.sortable({
		// only make the .panel-heading support dragging
		handle: '.panel-heading',
		update: function() {
			$('.panel', panelList).each(function(index, elem) {
				var $listItem = $(elem),
				newIndex = $listItem.index();

				// send an AJAX request to update the shot index
				$.ajax({
					type: "POST",
					url: "/shots",
					dataType: "json",
					data: {
						"shotID": $listItem.attr("shot-id"),
						"field": "index",
						"value": newIndex
					},
					success: function(data, textStatus, jqXHR) {
					},
					error: function(data, textStatus, jqXHR) {
						alert("error, see console");
						console.log(data);
					}
				});
			});
		}
	});
});