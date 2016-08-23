		$( document ).ready(function() {

		function loadChiTable(name){
			var values = {"polymer" : name};
                        $.ajax({
                                      method: "POST",
                                        url: "/chis",
                                        contentType: "application/json",
                                        data:  JSON.stringify(values)
                                        }).done(function( html ) {
                                                 $("#resultdiv2").html(html);
                                        });
		}

		function getWiki(name){
			// Form wikipedia api with polymer as title
			$.getJSON("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&titles="+name+"&format=json&callback=?", function(data) {
	
				// Get image file? This is hacky and polymer names
				// can be complex, but the info paragraph and the data
				// just does not display when no information is found.
				var wikidata = JSON.stringify(data);
				// Image file is sometimes under ImageFile, sometimes
				// under File, elimiate 6 and 11 because it means
				// indexOf = -1, select remaining index.
				var start_pos0 = wikidata.indexOf('File:') + 5;
				var start_pos1 = wikidata.indexOf('ImageFile = ') + 12;
				var ar = [start_pos0,start_pos1];
				var removeItem = 6;
				ar = jQuery.grep(ar, function(value) {
					return value != removeItem;
					});
				var removeItem = 11;
				ar = jQuery.grep(ar, function(value) {
		  		return value != removeItem;
				});
				// Detect end for image file name
				var armin = Math.min.apply(Math,ar);
				var end_pos0 = wikidata.indexOf('\\n',armin);	// This was first test, not necessary anymore since we use image extension
				var end_pos1 = wikidata.indexOf('jpg',armin)+3;
				var end_pos2 = wikidata.indexOf('png',armin)+3;
				var end_pos3 = wikidata.indexOf('svg',armin)+3;
				var arr = [end_pos0,end_pos1,end_pos2,end_pos3];
				// Similarly remove indexOf = -1
				var removeItem = 2;
				arr = jQuery.grep(arr, function(value) {
						return value != removeItem;
						});
				// Select minimum index
				var arrmin = Math.min.apply(Math,arr);
				var imgurl = "https://en.wikipedia.org/wiki/"+name+"#/media/File:";
				// Even though we have the url, the way wikipedia works, the image loads after a redirect and this is not a direct address. Therefore currently making a button to view the image (maybe discarded later).
				var imagename = wikidata.substring(armin,arrmin)
				imgurl = imgurl + imagename;
				$("#imgdiv").html("<a target=\"_blank\" href='"+imgurl+"'>View Image</a>");

				// Now get the first paragraph
				// Manipulation is needed to get rid of wikipedia formating
				// perhaps html would simplify this but symbols are {{}} ''' etc.
				// FIXME: Still problems with this {first|second}
				// in polystyrene aromaticity|aromatic, we only need one.
				var firstpar = JSON.stringify(data).split('\\n\\n')[1];
				firstpar = firstpar.replace(/\{{2}[^\]]+\}{2}/ig, "");
				firstpar = firstpar.replace(/\<ref[^\]]+\>/ig,'');
				firstpar = firstpar.replace(/\\/g, '');
				firstpar = firstpar.replace(/'''/ig, '');
				firstpar = firstpar.replace(/"/g,'');
				firstpar = firstpar.replace(/\[{2}/g,'');
				firstpar = firstpar.replace(/\]{2}/g,'');
				$("#resultdiv").text(JSON.stringify(firstpar)).html();
			});
		}

		// Get html query parameters
		function getParameterByName(name) {
			name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
			var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
			    results = regex.exec(location.search);
			return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
		}

		// Get query parameter
		var pol = getParameterByName('poly');

		// Get wikipedia for this polymer
		getWiki(pol);

		// Load DB data for this polymer
		loadChiTable(pol);

		// Format polymer name for heading
		pol = pol.toUpperCase();
		$('#title').text(pol);

		// FIXME: Loading datatables script on button click, otherwise 
		// it does not get loaded
			$('#container').on('click', '#btn', function(){
				$('#chitable').DataTable();
			});
		});
