$( document ).ready(function() {

	var taskresultClickEvent = $('.taskresult').trigger("click");

	clearTimeout()
	$(".add").click(function(){	
	    $.ajax({
	     type: "POST",
	     url: "api/crawl/",
	     contentType: "application/x-www-form-urlencoded",
	     data: $('.form-website').serialize(),
	     async: false,
	     success: function(data)
	     {
	     	var task = '<p>task status : '+data.status+'</p>'+
	     		'<p>task_id : '+data.task_id+'</p>'+
	     		'<p>unique_id : '+data.unique_id+'</p>';
	     	$(".response").html(task);
	     	$(".response").append('<a class="taskresult" href="task_id='+data.task_id+'&unique_id='+data.unique_id+'">Result</a>');
	     }
	  	});
	});
	$(".response").delegate(".taskresult","click", function(e){
    	 e.preventDefault();
		 $.ajax({
	     type: "GET",
	     url: "api/crawl/",
	     contentType: "application/x-www-form-urlencoded",
	     data: $(this).attr("href"),
	     async: false,
	     success: function(data)
	     {	

	     	if (data.status == undefined){
	     		$(".result").html("");
	     		for (itemId in data.data){
	     			$(".result").append("<p>"+data.data[itemId]+"</p>");
              	}
	     	}else{
	     		$(".result").html("");
	     		$(".result").append("<p>status "+data.status+"...</p>");
	     	}
	     }
	  	});
		 return false;
	});

});