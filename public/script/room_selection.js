$(document).ready(function() {
    var eventDates = {};
	var selectedRangeStart = null;
	var selectedRangeEnd = null;
	var selectedRoom;
    
	$(".room_area").click(function() {
		$(".cell").removeClass("room_selected");
		$(this).addClass("room_selected");
        var id = $(this).attr("id");
        var s = id.toString();
		selectedRoom = id;
        eventDates = {};
		selectedRangeStart = null;
		selectedRangeEnd = null;
        
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
		eventDates = {};
		selectedRangeStart = null;
		selectedRangeEnd = null;
		$("#calendar").datepicker("refresh");
        return false;
    });
    
    $("#calendar").datepicker({
        firstDay: 1,
        minDate: 0,
        maxDate: 365 * 2,
        beforeShowDay: function(date) {
            var highlight = eventDates[date.setHours(0, 0, 0, 0)];
			var d = date.setHours(0, 0, 0, 0);
			var min = selectedRangeStart;
			var max = selectedRangeEnd;
			if (min > max) {
				min = selectedRangeEnd;
				max = selectedRangeStart;
			}
            if (highlight) {
                return [false, "highlight", "unAvailable"];
            }
			else if (selectedRangeEnd != null && (d >= min && d <= max)) {
				return [true, "selectedDay", "Available"];
			}
			else if (d == selectedRangeStart) {
				return [true, "selectedStartDay", "Available"];
			}
            else {
                return [true, "", "Available"];
            }   
        },
		onSelect: function(date) {
			if ($(".cell").hasClass('room_selected')) {
				selectDate(date);
			}
		}
    });
	
	function selectDate(date) {
		$("#p2").html("");
		var selectedDate = (new Date (date)).setHours(0, 0, 0, 0);
		if (selectedDate == selectedRangeEnd) {
			selectedRangeEnd = null;
		}
		else if (selectedDate == selectedRangeStart) {
			selectedRangeStart = selectedRangeEnd;
			selectedRangeEnd = null;
		}
		else if (selectedRangeStart == null) {
			selectedRangeStart = selectedDate;
		}
		else {
			selectedRangeEnd = selectedDate;
			var min = selectedRangeStart;
			var max = selectedRangeEnd;
			if (min > max) {
				min = selectedRangeEnd;
				max = selectedRangeStart;
			}
			//86 400 000 ms in 1 day
			for (var i = min; i <= max; i += 86400000) {
				if (eventDates[i]) {
					selectedRangeEnd = null;
					$("#p2").html("Выбранная комната недоступна в выбранные вами дни. Пожалуйста, выберите другие даты.");
					break;
				}
			}
			$("#calendar").datepicker("refresh");
		}
	};
	
	$("#submit-book").on("click", function() {
		if (selectedRangeStart == null) {
			$("#p2").html("Даты бронирования не выбраны.");
		}
		else {
			if (selectedRangeEnd == null) {
				selectedRangeEnd = selectedRangeStart;
			}
			var min = selectedRangeStart;
			var max = selectedRangeEnd;
			if (min > max) {
				min = selectedRangeEnd;
				max = selectedRangeStart;
			}
			var start = new Date(min);
			var end = new Date(max);
			var insertion = $.post("/book_dates",
            {room_id: selectedRoom,
			start_date: start.getDate().toString() + "/" + (start.getMonth() + 1).toString() + "/" + start.getFullYear().toString(),
			end_date: end.getDate().toString() + "/" + (end.getMonth() + 1).toString() + "/" + end.getFullYear().toString()},
            "json")
			insertion.done( function() {
				for (var i = min; i <= max; i += 86400000) {
					eventDates[i] = i;
				}
				selectedRangeStart = null;
				selectedRangeEnd = null;
				$("#calendar").datepicker("refresh");
			}
			);
		}
	});
});