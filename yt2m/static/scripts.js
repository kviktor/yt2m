var inProgress = false;

$(function() {
  var helper = $("#helper-data");
  inProgress = helper.length && helper.data("state") < 2;

  if(inProgress) {
    updatePage();
  }

  $("#show-cut-link").click(function() {
    $("#cut-form").toggleClass("hidden");
  });

  $("#start-btn").on("click", function(e) {
    var width = $(this).width();
    $(this).html('<i class="fa fa-spinner fa-spin"></i>');
    $(this).width(width);
    $(this).prop("disabled", true);

    $("form").submit();
  });
});


function updatePage() {
  $.ajax({
    url: $("#helper-data").data("url"),
    method: "GET",
    success: function(data) {
      $("#progress-text").text(data.progress + "% - " + data.readable_state);
      var w = $(".section-progress").width();
      var progress = data.progress < 20 ? 20 : data.progress;

      $(".progress-bar").stop(true).animate({'width':  w * progress / 100}, 200);

      if(data.state == 2) {
        $("#download-button-container").fadeIn();
      }

      if(data.state == 3) {
        $("#download-error").slideDown();
      }

      if(data.state < 2) {
        setTimeout(
          function() {updatePage();},
          1000,
        );
      } else {
        inProgress = true;
      }
    }
  });
}
