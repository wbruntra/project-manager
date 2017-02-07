$('.sp-create').on('click', function() {
  var project_id = $(this).data('project-id');
  var field = $('#newSubprojectModal form input[name="project-id"]');
  field.val(project_id);
  console.log(project_id);
});

$('.delete-subproject').click(function(e) {
  console.log('delete subproject!')
  e.preventDefault();
  if (confirm('Really delete?')) {
    window.document.location = $(this).data('href')
  }
});
