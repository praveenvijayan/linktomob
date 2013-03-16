$(function (argument) {
	// tour.init()
	// $('.info').on('click',function (argument) {
	// 	$('#tour').toggle();
	// });

	$(window).on('click',function (event) {

		console.log(event)

		if($(event.target).attr('class') == 'info'){
			$('#tour').show();
			return
		}

		if(event.target.id === 'tour' || $(event.target).parents('#tour').length){
			return
		}else{
			$('#tour').hide();
		}

	});

	$(window).on('keydown', function (code) {
		if(code.keyCode == 27){
			$('#tour').hide();
		}
	})
});


/*


if(event.target.class == 'info'){
			$('#tour').show()
			return
		}
		if (event.target.id !== 'tour'){
			$('#tour').hide();
		}

(function ($) {

	var tour = tour || {};
	var intVal = 0;
	tour = {
		stages:['email','email-hover','email-sent','gmail','activation','show-bookmarklet','dnd','site','myurl','site-show','lsiting','bookmark'],
		init:function  (argument) {
			// console.log(this.stages)
			var tourElem = $('#tour');
			// clearTimeout(tour.tout);
			//this.timeOut(function(){$('#tour').addClass(this.stages[intVal])},1000);

			tour.tout = setInterval(function() {
				// $('#tour').attr('class','');
				$('#tour').addClass(tour.stages[intVal++]);
			}, 2000);
		},
		timeOut:function (fun, time) {
			tour.tout = setTimeout(function() {
				fun()
			}, time);
		}
	}

	return window.tour = tour;
}(jQuery))*/