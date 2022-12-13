$(document).ready(function(){

	$("button.follow").click(function() {
		const id = $(this).attr("id");
		$.ajax({
			data: {'follow': id},
			url: '/follow',
			type: 'POST'
		}).done(function(data){
			if (data.error) {
				alert("Error")
			} 
		});

		setTimeout(function(){
			location.reload();
		}, 1000);

	});

	$("button.unfollow").click(function() {
		const id = $(this).attr("id");
		$.ajax({
			data: {'unfollow': id},
			url: '/unfollow',
			type: 'POST'
		}).done(function(data){
			if (data.error) {
				alert("Error")
			}
		});

		setTimeout(function(){
			location.reload();
		}, 1000);

	});

});