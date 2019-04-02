$(function () {
  $('button.delete').click(function(e) {
    e.preventDefault();
    if(confirm('Are you sure you wish to delete this?')) {
      $(this).unbind('click').click();
    }
  });
});
