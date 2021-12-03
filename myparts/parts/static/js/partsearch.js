$(function() {
	
    $("#myresult").hide();
	
	/*$('#mypart').keyup(function(){
        $(this).val($(this).val().toUpperCase());
    });
	*/
	$('#mypart').keyup(searchitemcode);
	
});


function searchitemcode()
{

	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	var mypart =$("#mypart").val();
	if(mypart == "---------" || mypart == "" || mypart == null ){mypart=0;}
	
	mystrlen=0
	if( Object.prototype.toString.call(mypart) != '[object String]' ) {
		n = mypart.toString();
		mystrlen = n.length;
	}
	else
	{
		mystrlen = mypart.length;		
	}   
		if (mystrlen>3)
		{		
			
			$.ajax(
			{
			type:"POST",
			url: "/parts/partssearch/",
			headers:{"X-CSRFToken": csrftoken},
			data:{					
					'mypart': mypart,					
			},
			success: function (data)
			{   
					
				$("#orresult").hide('slow');
				$("#myresult").html(data);
				$("#myresult").show('slow');				
			}
			});
		}
		else if (mystrlen==1)
		{
				$("#myresult").hide('slow');
				$("#orresult").show('slow');		
		}	
		else
		{	
			$("#myresult").hide('slow');	
		}
}


