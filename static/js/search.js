//$("#search-key").on("keyup", function () {
$("#search").on("click", function () {
//  var key = $(this).val();
  var key = $("#search-key").val();
  console.log(key);
  if(key.length >= 3){
      $.ajax({
        url: '/',
        data: {
          'key': key
        },
        dataType: 'json',
        success: function (data) {
          var list = "";
          $("#result-list").html(list);
          if (data.message) {
            $("#message").html(data.message);
          }else{
            $("#message").html("Results");
            for (i = 0; i < data.search_result.length; i++) {
                list += "<li>" + data.search_result[i] + "<li>";
            };
            $("#result-list").html(list);
          };
        }
      });
      console.log(key);
  }
  else{
    var list = "";
    $("#result-list").html(list);
    $("#message").html("Please enter more than 3 letter");
  };
});
