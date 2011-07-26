$(document).ready(function(){
  $("#showLatest").click(
    function(event){
      $(this).hide();
      $("#map").hide();
      $("#showMap").show();
      $("#piclist_container").hide();
      $("#latest_container").show();
    }
  );

  function refreshList(fetchOptions){
    var optionstring = '';
    if (fetchOptions){
      optionstring = ['?searchfor=',
                      $(":input[name=searchfor]")[0].value,
                      '&nearish=',
                      $(":input[name=nearish]")[0].value,
                      '&haspic=',
                      $(":input[name=haspic]")[0].value,
                      '&online=',
                      $(":input[name=lastonline]")[0].value].join('');
    }
    var req = new XMLHttpRequest();
    var url = '/rpc/nearby/' + optionstring;
    console.debug(url);
    req.open('GET', url, true);
    req.onreadystatechange = function(){
      if(req.readyState == 4 && req.status == 200) {
        var response = null;
        response = JSON.parse(req.responseText);
        //insert the table html in the container
        $("#piclist_container").hide();
        $("#piclist_container").html(response.tablehtml);
        $("#piclist_container").show("slow");
      }
    }
    req.send(null);
  }

  $(".optionchange").change(
      function(event){
        refreshList(true);
      });
  refreshList(true);

  //get latest pics
  //  var req = new XMLHttpRequest();
  //  var url = '/latest';
  //    req.open('GET', url, true);
  //    req.onreadystatechange = function(){
  //      if(req.readyState == 4 && req.status == 200) {
  //    //insert the table html in the container
  //    $("#latest_container").html(req.responseText);
  //      }
  //    }
  //    req.send(null);
});

