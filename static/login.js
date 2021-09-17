function sign_in() {
    let userid = $("#input-id").val()
    let password = $("#input-pw").val()

    if (userid == "") {
        $("#help-id-login").text("아이디를 입력해주세요.")
        $("#input-id").focus()
        return;
    } else {
        $("#help-id-login").text("")
    }

    if (password == "") {
        $("#help-pw-login").text("비밀번호를 입력해주세요.")
        $("#input-pw").focus()
        return;
    } else {
        $("#help-pw-login").text("")
    }
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            userid_give: userid,
            password_give: password
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                console.log('토큰발행')
                window.location.replace("/member")
            } else {
                alert(response['msg'])
                console.log('토큰안됨')
            }
        }
    });
}