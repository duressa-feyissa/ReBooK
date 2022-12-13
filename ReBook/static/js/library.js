$(document).ready(function(){

	$(".addread").on("click", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		$.ajax({
			data: {'book_id': SplitArray[1]},
			url: '/readend',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: readend");
			} else {
				alert(data['data']);
			}
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	});

	$(".addfav").on("click", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		$.ajax({
			data: {'book_id': SplitArray[1]},
			url: '/addfav',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: readend");
			} else {
				alert(data['data']);
			}
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	});

	$(".removebmk").on("click", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		$.ajax({
			data: {'book_id': SplitArray[1]},
			url: '/removebmk',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: readend");
			} else {
				alert(data['data']);
			}
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	});

	$(".removebmk").on("click", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		$.ajax({
			data: {'book_id': SplitArray[1]},
			url: '/removebmk',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: Fail to remove from bookmark!");
			} 
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	});

	$(".removefav").on("click", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		$.ajax({
			data: {'book_id': SplitArray[1]},
			url: '/removefav',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: Fail to remove from favorite!");
			} 
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	});


	$(".removeend").on("click", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		$.ajax({
			data: {'book_id': SplitArray[1]},
			url: '/removeend',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: Fail to remove from read!");
			}
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	});


	$(".track_reading").on("change", function(){
		let text = $(this).attr("class");
		const SplitArray = text.split(" ");
		const page = $(this).val();
		$.ajax({
			data: {'book_id': SplitArray[1], 'page': page},
			url: '/track_reading',
			type: 'POST'
		})
		.done(function(data) {
			if(data.error) {
				alert("Error: Fail to remove from read!");
			} 
		});
		setTimeout(function(){
			location.reload();
		}, 1000);
	}); 

});
