$( document ).ready(function(e) {
	
	var _search = "";
	var _type = "category";
	
	
	$('a.search-price').on("click",function(){
		var search_value = $("#search").val();;
		var search_type = $('#search-type').val();
		load_data(search_value, search_type);
	});

	var load_data = function(search, type){
		var get_params = [];
		var html = "";
		
		if(!type)
		{
			$('.error').text("Please select the category");
			return false;
		}
		$('.error').text("");
		if(search)
			get_params.push("search="+search);
		if(type)
			get_params.push("type="+type);
		
		var get_param_string = get_params.join("&");
		var url = "/businesses?limit=10&" + get_param_string;
		
		$.get( url, function( data ) {
			$.each( data['data'], function( key, _object ) {
				console.log(_object);
				html += '<div class="panel">\
                <div class="job_description">\
                    <div class="company_logo">\
                        <img src="../static/images/food.jpg">\
                    </div>\
                    <div class="description">\
                        <h3>'+_object.dish_name+'</h3>\
                        <h4>'+_object.business_name+'</h4>\
                        <p>'+_object.address+'</p>\
                        <div class="job_actions">\
                            <div class="job_specs">\
                                <div class="specs">\
                                    <label>Sub Name</label>\
                                    <span>'+_object.dish_sub_name+'</span>\
                                </div>\
                                <div class="specs">\
                                    <label>Price</label>\
                                    <span>£'+_object.dish_price+'</span>\
                                </div>\
                                <div class="specs">\
                                    <label>Rating</label>\
                                    <span>'+_object.rating+'</span>\
                                </div>\
								<div class="specs">\
                                    <label>Category</label>\
                                    <span>'+_object.dish_category+'</span>\
                                </div>\
                            </div>\
                            <a href="'+_object.url+'" target="_blank">\
							Visit Page \
						</a>\
                        </div>\
                    </div>\
                </div>\
            </div>';
			});
			//console.log(html);
			if(!html)
				$('#search-results').html("<h1 style='color:#e91e63;margin-top: 50px;'>No Result Found !</h1>");
			else
				$('#search-results').html(html);
		});
	}
	
	load_data(_search, _type);
});


