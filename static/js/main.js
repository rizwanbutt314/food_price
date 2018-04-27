$( document ).ready(function(e) {

	$('a.search-price').on("click",function(){
		load_data(load_source="click");
	});

	var load_data = function(load_source){
		var get_params = [];

        var search_value = $("#search").val();
        var search_type = $('#type').val();
        var postcode = $('#postcode').val();

		$('.error').text("");
		if(search_value)
			get_params.push("search="+search_value);
		if(postcode)
			get_params.push("postcode="+postcode);
        if(search_type)
            get_params.push("type="+search_type);

        get_params.push("load_source="+load_source);
		
		var get_param_string = get_params.join("&");
		var url = "/businesses?limit=10&" + get_param_string;
		
		$.get( url, function( data ) {
			var html = generate_html(data);
			if(!html)
				$('#search-results').html("<h1 style='color:#e91e63;margin-top: 50px;'>No Result Found !</h1>");
			else
				$('#search-results').html(html);
		}).fail(function(jqXHR, textStatus, errorThrown){
            $('.error').text(jqXHR.responseJSON['error']);
        });
	}

	var generate_html = function(data){
        var html = "";
        $.each( data['data'], function( key, _object ) {
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
                                <div class="specs">\
                                    <label>Cuisines</label>\
                                    <span>'+_object.cuisines+'</span>\
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
        return html;
	}
	
	load_data(load_source="load");
});


