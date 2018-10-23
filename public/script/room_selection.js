$(document).ready(function() {
	$(".room_area").click(function() {
		$(".cell").removeClass("room_selected");
		$(this).addClass("room_selected");
		$.ajax({
			type: "GET",
			url: "/room?id=" + $(this).attr("id"),
			success: function(data){
				$("#active_room")
					.empty()
					.append('<div style="text-align: center"><span><font size="4" color="black">Вы выбрали комнату - '+data.number+'</font></span></div>')
					.append('<div style="text-align: center"><span><font size="4" color="black">Тип комнаты - '+data.room_type_name+'</font></span></div>')
					.append('<div style="text-align: center"><span><font size="4" color="black"> Стоимость проживание за один день - '+data.room_type_cost+'</font></span></div>')
					.append('<div style="text-align: center"><h1><a href="#" id="deactivate_room">Отменить выбор</a></h1></div>')
				$("#deactivate_room").click(function() {
					$("#active_room").empty()
				});
			}
		});
	});
})
