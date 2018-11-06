$(document).ready(function() {
    var eventDates = {};
    
	$(".room_area").click(function() {
		$(".cell").removeClass("room_selected");
		$(this).addClass("room_selected");
        var id = $(this).attr("id");
        var s = id.toString();
        eventDates = {};
        
        $.post("/submit_dates",
            {room_id: $(this).attr("id")},
            function(data) {
            $("#p1").html("Выбрана комната с номером " + s + ". Недоступные для выбора дни отмечены красным цветом.");
            for (var i = 0; i < data.dates.length; i++) {
                    eventDates[(new Date(data.dates[i])).setHours(0, 0, 0, 0)] = (new Date (data.dates[i])).setHours(0, 0, 0, 0);
                }
                $("#calendar").datepicker("refresh");
            }, 
            "json") 
	});
    
    $('.room_area').contextmenu(function() {
        $(".cell").removeClass("room_selected");
        $("#p1").html("Выберите комнату. <br/> &nbsp; ");
        return false;
    });
    
    $("#calendar").datepicker({
        firstDay: 1,
        minDate: 0,
        maxDate: 365 * 2,
        beforeShowDay: function(date) {
            var highlight = eventDates[date.setHours(0, 0, 0, 0)];
            if (highlight) {
                return [false, "highlight", "unAvailable"];
            }
            else {
                return [true, "", "Available"];
            }   
        }
    });
})
