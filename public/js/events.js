$(document).ready(function() {
  $('#project').on('change',function() {
    getSubprojects($(this).val());
  });
});

$('#delete-button').click(function(e) {
  e.preventDefault();
  if (confirm('Are you sure?')) {
    window.document.location = "/events/delete/" + $(this).data('event-id');
  }
});

getSubprojects = function(project_id) {
  var url = '/api/get/subprojects/' + project_id;
  $.ajax({
     url: url,
     error: function() {
        $('#info').html('<p>An error has occurred</p>');
     },
     success: function(data) {
       $('#subproject').html(data);
     },
     type: 'GET'
  });
};
