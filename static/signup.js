/////////아이디 조건 확인//////////
function is_id(asValue) {
    var regExp = /^(?=.*[a-zA-Z0-9])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
}

/////////아이디 조건확인/////////
function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

/////////아이디 중복학인//////////
function check_dup() {
    let username = $("#user-id").val() //username 인풋으로 받기
    console.log(username)
    //아무것도 입력하지 않을경우
    if (username === "") {
        $("#help-id").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger dangerColor")
        $("#user-id").focus()
        return;
    }
    //무언가 입력했을 때
    if (!is_id(username)) {
        $("#help-id").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").removeClass("is-safe successColor").addClass("is-danger dangerColor")
        $("#user-id").focus()
        return;
    }
    $("#help-id").addClass("is-loading")
    // ajax로 아이디 중복확인 요청
    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            userid_give: username
        },
        //요청 성공을 하면
        success: function (response) {
            //서버에서 이미 그런 사람이 있다고 하는 경우
            if (response["exists"]) {
                $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger dangerColor")
                $("#user-id").focus()
            }
            // 없는 아이디일 경우
            else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger dangerColor").addClass("is-success successColor")
            } //=> is success클래스 추가해줌으로써 중복확인된 아이디라는 것을 알려주는 것. 서버에서 있는지 없는지를 구분해주기
            $("#help-id").removeClass("is-loading")

        }
    });
}   


/////////회원가입//////////
function sign_up() {
    // 아이디, 패스워드, 패스워드 값 변수 지정
    let userid = $("#user-id").val()
    let password = $("#user-pw").val()
    let password2 = $("#user-pw2").val()
    console.log(userid, password, password2)

// class를 통해 중복검사여부 확인
    if ($("#help-id").hasClass("is-danger")) {
        alert("아이디를 다시 확인해주세요.")
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.")
        return;
    }

    //패스워드가 빈칸인지 검사
    if (password === "") {
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe successColor").addClass("is-danger dangerColor")
        $("#user-pw").focus()
        return;
        //정규식 검사
   } else if (!is_password(password)) {
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe successColor").addClass("is-danger dangerColor")
        $("#user-pw").focus()
        return;
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger successColor").addClass("is-success successColor")
    }
    // 패스워드 확인란에 아무것도 입력하지 않았다면
    if (password2 === "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe successColor").addClass("is-danger dangerColor")
        $("#user-pw2").focus()
        return;   
        
    //패스워드1, 패스워드2 같은지 검사
    } else if (password2 !== password) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe successColor").addClass("is-danger dangerColor")
        $("#user-pw2").focus()
        return;  
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger dangerColor").addClass("is-success successColor")
    }
    // 패스워드 확인값이 조건에 맞는지 검사
    if (!is_password(password2)) {
        $("#help-password2").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe successColor").addClass("is-danger dangerColor")
        $("#user-pw2").focus()
        return;
    }
    // ajax로 가입요청
    $.ajax({
        type: "POST",
        url: '/sign_up/save',
        data: {
            userid_give: userid,
            password_give: password
        },
        // 가입요청 성공시 메세지를 띄워주고 login화면으로 이동
        success: function (response) {
            console.log(response)
            alert("회원가입이 완료되었습니다!")
            window.location.replace("/login")
        }
    });
}
// 패스워드 중복확인 구현을 못했다.