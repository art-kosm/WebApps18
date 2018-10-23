$(document).ready(function() {
	$(".test").click(function() {
		$.ajax({
			type: "GET",
			// url: "/room?id=" + $(this).attr("id"),
			// data: "",
			success: function(data){
				alert("!");
			}
		});
	});
})