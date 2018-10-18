// Arbalet Project
// Workshop admin page

(function worker() {
  $.get('admin/nicknames', function(jsonNicknames) {
    $.get('admin/active_nickname', function(jsonActiveNickname) {
      var activeNickname = JSON.parse(jsonActiveNickname);
      var nicknames = JSON.parse(jsonNicknames);

      // Generate empty list
      $("ul").children().remove();
      var checked = (nicknames.indexOf(activeNickname) > -1)? "" : "checked";
      $("#nicknames").append('<li class="list-group-item"><div class="form-check"><input class="form-check-input" type="radio" name="active_user" data-user-id=turnoff value="active" ' + checked + '><label class="radio">Tout éteindre</label></div></li>');

      for(var i = 0, len = nicknames.length; i < len; i++) {
        var nickname = nicknames[i];
        var checked = (nickname == activeNickname)? "checked" : "";
        $("#nicknames").append('<li class="list-group-item"><div class="form-check"><input class="form-check-input" type="radio" name="active_user" data-user-id=' + nickname + ' value="active" ' + checked + '><label class="radio">' + nickname + '</label></div></li>');
    };

    // Event for Authorize
    $('[name=active_user]').change(function() {
      $.post('/authorize', $(this).attr('data-user-id'));
    });
    setTimeout(worker, 500);
  })});
})();
