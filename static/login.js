// 로그인 버튼 누를 시
function sign_in() {
    // 아이디, 비밀번호 값을 변수에 담는다.
    let userid = $("#input-id").val()
    let password = $("#input-pw").val()
    // 아이디를 입력하지 않았다면 "아이디를 입력해주세요."라는 경고 메세지가 나오면서 인풋 박스에 포커스하고 함수 종료
    if (userid == "") {
        $("#help-id-login").text("아이디를 입력해주세요.").addClass('dangerColor')
        $("#input-id").focus()
        return;
        // 입력했으면 경고메세지 아무것도 나오지 않음
    } else {
        $("#help-id-login").text("")
    }
    if (password == "") {
        // 비밀번호를 입력하지 않았다면 인풋 박스 아래에 "비밀번호를 입력해주세요."라는 경고메세지가 나오면서 인풋 박스에 포커스하고 함수 종료
        $("#help-pw-login").text("비밀번호를 입력해주세요.").addClass('dangerColor')
        $("#input-pw").focus()
        return;
        // 입력했으면 경고메세지 아무것도 나오지 않음 
    } else {
        $("#help-pw-login").text("")
    }
    //ajax로 post방식을 통해 sign_in에 아이디와 비밀번호를 보냄
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            userid_give: userid,
            password_give: password
        },
        success: function (response) {
            // 결과값이 success라면
            if (response['result'] == 'success') {
                //쿠키생성, 메세지
                $.cookie('mytoken', response['token'], {path: '/'})
                window.location.href='memberView';
                alert('로그인완료!');
            } else {
                alert(response['msg'])
            }
        }
    });
}
