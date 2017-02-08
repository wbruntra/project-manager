console.log("hello, world!");

$('form').submit(function(e) {
  e.preventDefault();
  var formData = $(this).serialize();
  console.log(formData);
  // Submit the form using AJAX.
  $.ajax({
      type: 'POST',
      url: "/events/project",
      data: formData,
      success: function(data) {
        $('#event-list').html(data);
      }
  })
  var boxes = [];
  $(':checked').each(function() {
    var project_id = $(this).val();
    console.log(project_id);
  });
});

$(document).on('click','.clickable-row',function(){
  window.document.location = $(this).data('href');
});
