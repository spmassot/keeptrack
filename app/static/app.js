$(function () {
  $('button.delete').click(function(e) {
    return confirm('Are you sure you wish to delete this?');
  });

  $('.invoice-row').click(function(e) {
    window.location = $(this).data("href");
  });
});
