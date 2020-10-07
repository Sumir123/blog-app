// email validation
$(document).ready(function() {
    $('input[name="email"]').focusout(function(e) {
        e.stopPropagation()
        var regx = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        var email = $('input[name="email"]').val();
        var l = email.length;
        if (regx.test(email) && l != 0) {
            document.getElementById('spam1').style.visibility = "hidden";
        } else {
            document.getElementById('spam1').innerHTML = "Email empty or invalid";
            document.getElementById('spam1').style.visibility = "visible";
            e.preventDefault();
        }
    })
    $('input[type="submit"]').click(function(e) {
            e.stopPropagation()
            var regx = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
            var email = $('input[name="email"]').val();
            if (regx.test(email) && l != 0) {
                document.getElementById('spam1').style.visibility = "hidden";
            } else {
                document.getElementById('spam1').innerHTML = "Email empty or invalid";
                document.getElementById('spam1').style.visibility = "visible";
                e.preventDefault();
            }
        })
        // delet post
    $(".post_delete").click(function() {
        id = $(".id").attr("id");
        $.ajax({
            url: "/post/delete/" + id,
            type: 'POST',
            success: function() {
                $('#' + id).remove();
            },
            error: function() {
                alert("error");
            }
        })
    })

});


//Auto load
$(document).ready(function(e) {
    $('.nopost').hide();
    var nopost = true;
    $(window).scroll(function(e) {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && nopost) {
            var id = $('div#post > div.id').length;
            $.ajax('/home', {
                type: 'POST',
                contentType: 'application/json; charset-utf8',
                dataType: 'json',
                async: false,
                data: JSON.stringify({ "count": id }),
                success: function(data) {
                    if (data.data == 'end') {
                        nopost = false;
                        $('.nopost').show();
                        return true;
                    }
                    for (var i = 0, len = data.length; i < len; i++) {
                        var $div = $("<div id =" + data[i].id + " class='id' data-id=" + data[i].id + "> </div>")
                        var txt1 = $("<h5 id='post_title'></h5>").text(data[i].title);
                        var txt2 = $("<p id='post_username'> </p>").text("Written by:" + data[i].username);
                        var txt3 = $("<p id='post_description'> </p>").text(data[i].description);
                        var btn1 = $("<button class='post_delete'> </button>").text('Delete');
                        var btn2 = $("<a id='post_edit' href='/post/edit/" + data[i].id + "'>Edit</a>").text('Edit');
                        $('#post').append($div);
                        $($div).append(txt1, txt2, txt3, btn1, btn2);
                    }
                    id = id + 10;
                },

                error: function() {
                    console.log("error")
                },
                timeout: 5000,
            });
            ready = true;
        }
    })
});