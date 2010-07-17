$(document).ready(function(){
	$("#showformbutton").click(
		function(event){
			$(this).hide("slow");
			$("#formdiv").show("slow");
			$('html,body').animate({scrollTop: $("#formdiv").offset().top},500);
		}
	);
	
	$("#showLatest").click(
		function(event){
			$(this).hide();
			$("#map").hide();
			$("#showMap").show();
			$("#piclist_container").hide();
			$("#latest_container").show();
		}
	);
	
	$("#showMap").click(
		function(event){
			$(this).hide();
			$("#map").show();
			$("#showLatest").show();
			$("#piclist_container").show();
			$("#latest_container").hide();
		}
	);
	
	//get latest pics
	var req = new XMLHttpRequest();
	var url = '/latest';
    req.open('GET', url, true);
    req.onreadystatechange = function(){
      if(req.readyState == 4 && req.status == 200) {
		//insert the table html in the container
		$("#latest_container").html(req.responseText);
      }
    }
    req.send(null);
	
   initialize();
 });

locmap = {};      

function initialize() {
        if (GBrowserIsCompatible()){
          locmap.map = new GMap2(document.getElementById("map_canvas"));
			var lat = document.getElementById("center_lat");
			var lon = document.getElementById("center_lon");
			var latc = 47.617397308299999;
			var lonc = -122.19194030760001;
			if (lat && lon){
				var latc = lat.innerText || lat.textContent;
				var lonc = lon.innerText || lon.textContent;
			}
          locmap.map.setCenter(new GLatLng(lonc, latc), 13);
          locmap.map.addControl(new GLargeMapControl());
        }

		locmap.doRpc = function(lonc, latc){
			var req = new XMLHttpRequest();
			var url = '/rpc/nearby/?lat='+lonc+'&lon='+latc;
	        req.open('GET', url, true);

	        req.onreadystatechange = function(){
	          if(req.readyState == 4 && req.status == 200) {
	            var response = null;
	            response = JSON.parse(req.responseText);
				
				//insert the table html in the container
				$("#piclist_container").hide();
				$("#piclist_container").html(response.tablehtml);
				$("#piclist_container").show("slow");
				
				//put the markers on the map
	            addMarks(response.mapdata,locmap.map);
	          }
	        }
	        req.send(null);
		}
		locmap.doRpc(lonc, latc);
        

      }

      function createMarker(point, html) {
        
          var marker = new GMarker(point);
          GEvent.addListener(marker, "click", function(){
                        marker.openInfoWindow(html);
          });
          return marker;
      }


      function addMarks(response,map){
		if (!locmap.mgr) {
			locmap.mgr = new MarkerManager(map);
		}
		var mgr = locmap.mgr;
		mgr.clearMarkers();
        var batch = [];
        for (var phash in response) {
          var point = new GLatLng(response[phash]['lon'], response[phash]['lat']);
          var html = "<div class='infowindow'>"
				+ "<a href='/post/"+response[phash]['id']+"/'>"  
                + "<img src='/thumb/"+response[phash]['picid']+"' height='50'></img>"
                + "</a>"
                + "</div>";
          var marker = createMarker(point, html);
          batch.push(marker)
        }
        mgr.addMarkers(batch,0,17);
        mgr.refresh();
      }

		function search_on_map_center(){
			var lat = locmap.map.getCenter().lat(); 
			var lng = locmap.map.getCenter().lng();
			locmap.doRpc(lat, lng);
		}
		
		function set_location_here(){
			var lat = locmap.map.getCenter().lat(); 
			var lng = locmap.map.getCenter().lng();
			window.location = "/loc/coords/"+lng+"/"+lat+"/";
		}
		
		function getlocfrommap(){
			var lat = locmap.map.getCenter().lat(); 
			var lng = locmap.map.getCenter().lng();
			var locbox = document.getElementById("locbox");
			locbox.value = lng +", "+lat;
			document.getElementById("coordinput").checked = true;
		}
