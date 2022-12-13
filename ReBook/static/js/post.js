$(document).ready(function(){

	$("#sub").click(function() {
		
		$("#form_post").trigger("reset");

		setTimeout(function(){
			location.reload();
		}, 1000);

	});
});