var active_line = null;
$(document).ready(function(e) {
    $('#type_tabs').tabs({ selected: 1 });
    $('#post_options').tabs({ selected: 0 });
    $('.linenos a').click(function(e) {
        var target = $(e.target).attr('href');
        var lineno = target.replace('#line-', '');
        $.each($('.highlight a[name^="line"]'), function(index, value) {
            if (index + 1  == parseInt(lineno)) {
                if (active_line != null) {
                    active_line.removeClass('selected');
                }
                $(value).addClass('selected');
                active_line = $(value);
                return false;
            }
        });
    });
    $('#copy_post').zclip({
        path: '/site-media/js/ZeroClipboard.swf',
        copy: $('#textarea_wrapper textarea').text(),
        afterCopy: function() {}
    });
    $('#copy_url').zclip({
        path: '/site-media/js/ZeroClipboard.swf',
        copy: $('input[name="post_url"]').val(),
        afterCopy: function() {}
    });
    $('#new_post form').append('<input type="hidden" name="skey" value="3453151o43oofu87^&*^S^DhsU" />');
    $('.post_info .description').truncate({maxLength: 120, stripFormatting: true});
});