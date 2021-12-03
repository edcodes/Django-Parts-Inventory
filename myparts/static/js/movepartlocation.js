$(function() {

	$("#move_location").click(movelocation);
	
	loaddropdown();

	
});

function loaddropdown()
{

		var csrftoken = $("[name=csrfmiddlewaretoken]").val();

		$.ajax(
			{
			type:"POST",
			url: "/parts/loaddropdown/",
			headers:{"X-CSRFToken": csrftoken},
			data:{					      
				'style':'number'
			},
			success: function (data)
			{   
				$("#id_bay_id").html(data);
				$("#id_position_id").html(data);

			}
			});
			
		$.ajax(
			{
			type:"POST",
			url: "/parts/loaddropdown/",
			headers:{"X-CSRFToken": csrftoken},
			data:{					      
				'style':'letter'
			},
			success: function (data)
			{   
				$("#id_rack_id").html(data);
				$("#id_level_id").html(data);

			}
			});	
		$.ajax(
			{
			type:"POST",
			url: "/warehouse/getwarehouselist/",
			headers:{"X-CSRFToken": csrftoken},
			data:{					      
				
			},
			success: function (data)
			{   
				$("#id_warehouse_id").html(data);
				

			}
			});	

}

function movelocation()
{

	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	
	var partid=$("#id_partid_id").val();
	var existingid = $("#id_existingid_id").val();
	var redirect=$("#id_redirect_id").val();
	
	var warehouse=$( "select#id_warehouse_id option:checked" ).val();
	var rack=$( "select#id_rack_id option:checked" ).val();
	var bay=$( "select#id_bay_id option:checked" ).val();
	var level=$( "select#id_level_id option:checked" ).val();
	var position=$( "select#id_position_id option:checked" ).val();
	var quantity=$("#id_quantity_id").val();


	if(partid == "---------" || partid == "" || partid == null ){partid=0;}
	if(existingid == "---------" || existingid == "" || existingid == null ){existingid=0;}
	if(warehouse == "---------" || warehouse == "" || warehouse == null ){warehouse=0;}
	if(rack == "---------" || rack == "" || rack == null ){rack=0;}	
	if(bay == "---------" || bay == "" || bay == null ){bay=0;}
	if(level == "---------" || level == "" || level == null ){level=0;}
	if(position == "---------" || position == "" || position == null ){position=0;}
	if(quantity == "---------" || quantity == "" || quantity == null ){quantity=0;}	
	
		
		if( partid > 0 && existingid != 0 && warehouse !=0 && quantity>0 )
		{		
			$.ajax(
			{
			type:"POST",
			url: "/parts/movelocationto/",
			headers:{"X-CSRFToken": csrftoken},
			data:{					
					'existingid':existingid,
					'partid':partid,
					'warehouse':warehouse,
					'rack':rack,
					'bay':bay,
					'level':level,
					'position':position,
					'quantity':quantity,					
			},
			success: function (data)
			{   
			window.location.replace(redirect);		
							
			}
			});
		}
		else{
			alert("Wrong Item Code, Warehouse or Quantity!!!!");
		}
		
}

