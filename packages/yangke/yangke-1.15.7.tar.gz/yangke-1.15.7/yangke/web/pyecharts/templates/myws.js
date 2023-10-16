// 提供对外使用的接口
function myws_start(url) {
    myws_start_init(url);
}

function myws_send(data) {
    myws_send_data(data)
}

var myws = null;
var myws_url_0 = "";
var myws_init = false;
var myws_isok = false;
var myws_reconnect_interval_ms = 5000;
var myws_isneedreconnect = false;

var myws_onopen = null;
var myws_onmessage = null
var myws_onerror = null
var myws_onclose = null

function myws_start_init(url) {
    if (true === myws_init) {
        console.log("no need to repeat start..")
        return;
    }
    myws_init = true
    myws_url_0 = url;
    myws_connect();
}

function myws_send_data(data) {
    if (true === myws_isok) {
        myws.send(data)
    } else {
        console.log("websocket is not ok.")
    }
}

function myws_connect() {
    if ("webSocket" in window) {
        myws = new WebSocket(myws_url_0);
        myws.onopen = function () {
            console.log("连接成功...");
            if (null !== myws_onopen) {
                myws_onopen(); // 如果外部制定了onopen()方法，则调用
            }
        }
        myws.onmessage = function (evt) {
            if (null !== myws_onmessage) myws.onmessage(evt);
        }
        myws.onerror = function () {
            console.log("连接错误...")
            if (null != myws_onerror) myws_onerror();
            myws_isok = false;
            myws_isneedreconnect = true;
        }
        myws.onclose = function () {
            console.log("连接已关闭...")
            if (null !== myws.onclose) myws_onclose()
            myws_isok = false
            myws_isneedreconnect = true;
        }
        myws_isok = true;
    } else {
        console.log("浏览器不支持websocket")
    }
}

function myws_reconnect() {
    myws_connect()
}

function myws_checkconnect() {
    if (false === myws_isok && true === myws_isneedreconnect) {
        myws_isneedreconnect = false
        console.log("准备自动重连...")
        myws_reconnect()
    }
}

setInterval(function () {
    myws_checkconnect();
}, myws_reconnect_interval_ms)