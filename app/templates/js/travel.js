function searchAirport(){
	var result = "";
	var submitData = "apikey=" + RzGfJPsCmYIRlDmTi6Og2BAYAVviEAdh + "&term=" + $("#location").val();
	console.log(data)
	$.ajax({
		url: "http://api.sandbox.amadeus.com/v1.2/airports/autocomplete",
		data: submitData,
		type: "GET",
		success: function(getThis){
			result = $.parseJSON(getThis)
			console.log(result);
		}
	})
}