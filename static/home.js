$(document).ready(function(){
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
