$(function () {
  $('button.delete').click(function(e) {
    return confirm('Are you sure you wish to delete this?');
  });

  $('button.send').click(function(e) {
    return confirm('Are you sure you want to send this invoice?');
  });

  $('.invoice-row').click(function(e) {
    window.location = $(this).data("href");
  });
});
