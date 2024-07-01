let INFO = document.getElementById("info");
let button = document.getElementById("to_server");

function userInfo() {
    BX24.selectUser(function info(res) {
        let id = res['id'];
        let name = res['name'];
        let text = "Выбран пользователь с id " + id + "; " + name;
        INFO.innerText = text;

        button.value = res['id'];
        button.disabled = false;
    });
};