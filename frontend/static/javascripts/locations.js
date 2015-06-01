	
				
				//START FILTERING LOCATIONS
				var locations = [];
				var villages   = [];
				var hps = [];
				var sectors = [];
				var cells = [];
				var villages = [];
				var url  = document.URL.split("?");
				var url2 = "";
				if (url.length > 1) url2 = url[1];
				$.getJSON( "/locs?"+url2 , function( result ){
				
						var provinces = _.map(_.indexBy(result['hcs'], 'province_id'), function(obj){return obj});
						locations = result['hcs'];
						hps = result['hps'];
						sectors = _.map(_.indexBy(result['villages'], 'sector_id'), function(obj){return obj});
						cells = _.map(_.indexBy(result['villages'], 'cell_id'), function(obj){return obj});
						villages = result['villages'];
					
						for ( var i=0; i<provinces.length; i++ ){
							province = provinces[i]
							document.getElementById('provchoose').options.length= provinces.length;
							document.getElementById('provchoose').options[i] = new Option(province.province_name, province.province_id);
							}

						for ( var i=0; i<hps.length; i++ ){
								hp = hps[i]
								document.getElementById('referralchoose').options.length = hps.length;
								document.getElementById('referralchoose').options[i] = new Option(hp.name, hp.id);
								}


						for ( var i=0; i<sectors.length; i++ ){
							sector = sectors[i]
							document.getElementById('secchoose').options.length= sectors.length;
							document.getElementById('secchoose').options[i] = new Option(sector.sector_name, sector.sector_id);
							}
						
						document.getElementById('provchoose').options[provinces.length] = new Option("", "");
						document.getElementById("provchoose").selectedIndex = provinces.length;
						
						document.getElementById('referralchoose').options[hps.length] = new Option("", "");
						document.getElementById("referralchoose").selectedIndex = hps.length;

						document.getElementById('secchoose').options[sectors.length] = new Option("", "");
						document.getElementById("secchoose").selectedIndex = sectors.length;

						// IS There a province selected, then apply
						sel_prov = getQueryParameter ( "province" );
						if (sel_prov != '' ){
								 changeDistrict(sel_prov);
								 prv_index = fetch_index_from_option_value(document.getElementById('provchoose').options, sel_prov);
								 document.getElementById('provchoose').options[prv_index].selected = true;
								 
								     }

						// IS There a district selected, then apply
						sel_dist = getQueryParameter ( "district" );
						if (sel_prov != '' && sel_dist != '') {
								changeLocation(sel_dist);
								dist_index = fetch_index_from_option_value(document.getElementById('distchoose').options, sel_dist);
							 	document.getElementById('distchoose').options[dist_index].selected = true;
									}

						// IS There a location selected, then apply
						sel_loc = getQueryParameter ( "hc" );
						if (sel_loc != '' && sel_dist != '') { 
									changeLocation(sel_dist);
								loc_index = fetch_index_from_option_value(document.getElementById('locchoose').options, sel_loc);
							 	document.getElementById('locchoose').options[loc_index].selected = true;
								}
						
						
	    					});
					
				function fetch_index_from_option_value(options, value){
											for(i=0;i<options.length;i++) 
											{ 
											if(options[i].value == value) break; 
											
											 }
											
											return i
											}

				function changeDistrict(value){

					var districts = _.map(_.indexBy(locations, 'district_id'), function(obj){ return obj });

					var selected_districts = _.filter(districts, function(item) {  return item.province_id == value;  });
			
					for ( var i=0; i<selected_districts.length; i++ ){
							district = selected_districts[i]
							document.getElementById('distchoose').options.length = selected_districts.length;
							document.getElementById('distchoose').options[i] = new Option(district.district_name, district.district_id);
								}
						document.getElementById('distchoose').options[selected_districts.length] = new Option("", "");
						document.getElementById("distchoose").selectedIndex = selected_districts.length;

					}

				function changeLocation(value){

					var selected_locations = _.filter(locations, function(item) {  return item.district_id == value; });
								
					for ( var i=0; i<selected_locations.length; i++ ){
								hc = selected_locations[i]
								document.getElementById('locchoose').options.length = selected_locations.length;
								document.getElementById('locchoose').options[i] = new Option(hc.name, hc.id);
								}
					
						document.getElementById('locchoose').options[selected_locations.length] = new Option("", "");
						document.getElementById("locchoose").selectedIndex = selected_locations.length;

					}

				function changeSector(value){
					
					var selected_cells = _.filter(cells, function(item) {  return item.sector_id == value;  });

					for ( var i=0; i<selected_cells.length; i++ ){
								cell = selected_cells[i]
								document.getElementById('cellchoose').options.length = selected_cells.length;
								document.getElementById('cellchoose').options[i] = new Option(cell.cell_name, cell.cell_id);
								}
						document.getElementById('cellchoose').options[selected_cells.length] = new Option("", "");
						document.getElementById("cellchoose").selectedIndex = selected_cells.length;
					}


			       function changeCell(value){

					var selected_villages = _.filter(villages, function(item) {  return item.cell_id == value;  });
			
					for ( var i=0; i<selected_villages.length; i++ ){
								village = selected_villages[i]
								document.getElementById('villchoose').options.length = selected_villages.length;
								document.getElementById('villchoose').options[i] = new Option(village.name, village.id);
								}
						document.getElementById('villchoose').options[selected_villages.length] = new Option("", "");
						document.getElementById("villchoose").selectedIndex = selected_villages.length;
					}
				
				function PassCheck(filter_form){
					
						// FIX CASES YOU CAN FORGET TO DISABLE SOME FILTERS AND THEY ARE EMPTY ... 
						if(filter_form.provchoose.value == ""){
											filter_form.provchoose.disabled = true;
											}
						else if(filter_form.distchoose.value == ""){
											filter_form.distchoose.disabled = true;
											}
						else if(filter_form.locchoose.value==""){
											filter_form.locchoose.disabled = true;
										}

						filter_form.submit();

					}

				function getQueryParameter ( parameterName ) {

						  var queryString = window.top.location.search.substring(1);
						  var parameterName = parameterName + "=";
						  if ( queryString.length > 0 ) {
						    begin = queryString.indexOf ( parameterName );
						    if ( begin != -1 ) {
						      begin += parameterName.length;
						      end = queryString.indexOf ( "&" , begin );
							if ( end == -1 ) {
							end = queryString.length
						      }
						      return unescape ( queryString.substring ( begin, end ) );
						    }
						  }
						  return "";

						} 
				function make_location_of_parent(name, url){
						var prv = getQueryParameter ( "province" );
						var dst = getQueryParameter ( "district" );
						var loc = getQueryParameter ( "hc" );
						if (name == 'province' && dst != ''){ 
											url = url.replace( "&district="+dst, "");
											if (loc != '') url = url.replace( "&hc="+loc, "");
											}
						if (name == 'district' && loc != '') url = url.replace( "&hc="+loc, ""); 
						
						return url;
							
						}
				function addInURL(name, value){
						var param = getQueryParameter ( name );
						var url  = document.URL ;
						if (param == "") url += "&"+ name + "=" + value; 
						url = make_location_of_parent(name, url);
						url = url.replace("#", '');
						window.location.href = url;
							
						}
				
				function getTotal(province, district, location, group, subcat){
							
							var prv = getQueryParameter ( "province" );
							var dst = getQueryParameter ( "district" );
							var loc = getQueryParameter ( "hc" );
							var param = getQueryParameter ( "summary" );
							var groupurl = getQueryParameter ( "group" );
							var subcaturl = getQueryParameter ( "subcat" );
							var url  = document.URL ;
							if (param != "") {	
										if (url.indexOf('?summary') > -1 )  url = url.replace("?summary="+param, "?");
										else url = url.replace("&summary="+param, "");
										}
							if (province != '' && prv == '' ) url = url + "&province="+ province;
							if (district != '' && dst == '' ) url = url + "&district="+ district;
							if (location != '' && loc == '' ) url = url + "&hc="+ location;
							if ( group && group != '' && groupurl == '' ) url = url + "&group="+ group;
							if ( subcat && subcat != '' && subcaturl == '' ) url = url + "&subcat="+ subcat;
							url = url.replace("#", '');
							//alert(province + "," + district + "," + location + "," + url) ;
							window.location.href = url; 

						}
				
				
				// END FILTERING
				
