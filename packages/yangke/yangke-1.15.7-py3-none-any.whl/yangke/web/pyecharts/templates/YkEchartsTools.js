// 该js文件定义了
var socket;

function hide_widget(widget_id) {
    // 隐藏指定id的元素
    let widget = document.getElementById(widget_id);
    if (widget !== null) {
        widget.style.display = 'none';
    }
}

function hide_all_widgets() {
    //   隐藏页面上除echarts图标以外的元素
    hide_widget('txt');
    hide_widget('connect');
    hide_widget('btn');
    hide_widget('close');
    hide_widget('state');
}

function sendMsg(msg) {
    //  前端画面向后台发送消息
    //  当不传入msg时，默认发送输入框[id = 'txt']中的内容
    if (msg === undefined || msg === null) {
        let txt = document.getElementById('txt')
        socket.send(txt.value)
        console.log(txt.value)
        txt.value = ""
    } else {
        socket.send(msg)
        console.log(msg)
    }
}

function getSeries() {
    if (chart.getOption() !== undefined) {
        let msg = JSON.stringify({"series": chart.getOption().series})
        sendMsg(msg)
    } else {
        sendMsg("当前echarts中不包含数据！")
    }
}

function appendData(var_name, var_value) {
    // 追加数据
    old_data.push([data_value.name, data_value.value]);
    chart.setOption({
        series: [{data: old_data}]
    });
}

function updateData(var_name, var_value) {
    // 更新数据
    // if (updateData.series !== undefined) {
    //     chart.setOption({series: updateData.series})
    // } else if (updateData.data !== undefined) {
    //     chart.setOption({
    //         series: [{data: updateData.data}]
    //     })
    // }
    // old_data = chart.getOption().series
    exp = `${var_name} = var_value`
    eval(exp)
}


function openConn() {
    // 建立websocket长连接，建立后，画面可以与后台随时传递数据
    socket = new WebSocket(url);
    document.getElementById('connect').setAttribute("disabled", "disabled")
    document.getElementById('btn').removeAttribute("disabled")
    document.getElementById('close').removeAttribute("disabled")
    socket.onopen = function () {
        console.log("服务器连接成功")
        document.getElementById('state').innerHTML = "【连接成功】"
        // 连接建立后，向后台发送"ready"字符串
        sendMsg("ready")
        if (typeof (option) !== "undefined") {  // 如果定义了option，就显示该echarts设置
            chart.setOption(option)
        }
    }

    socket.onmessage = function (event) {
        // 接收到消息
        let txt = document.getElementById('txt');

        let data_in = JSON.parse(event.data);
        let cmd = data_in.cmd;

        if (cmd === "initChart") {  // 说明接收到的是整个echarts图标的设置信息
            let option = JSON.parse(data_in.option);
            txt.value = "绘制图表";
            chart.setOption(option);
            old_data = chart.getOption().series
        } else if (cmd === "getSeries") {
            // 说面python端发送了获取前端显示的数据集的命令
            return getSeries()  // getSeries方法会发送当前页面数据给websocket另一端
        } else if (cmd === "appendData") {
            // 说明前端发送了新的需要追加的数据
            txt.value = "追加数据";
            return appendData(data_in["var"], data_in[data_in["var"]]);
        } else if (cmd === "updateData") {
            txt.value = "更新数据";
            return updateData(data_in["var"], data_in[data_in["var"]]);
        }

    }
}

function closeConn() {
    socket.send('close')
    socket.close()
    document.getElementById('btn').setAttribute("disabled", "disabled")
    document.getElementById('close').setAttribute("disabled", "disabled")
    document.getElementById('connect').removeAttribute("disabled")
    document.getElementById('state').innerHTML = "【连接已关闭】"
}

function connect_ready() {
    return new Promise((resolve, reject) => {
        setTimeout(
            () => {
                if (socket.readyState === 1) {
                    resolve("Resolved");
                } else {
                    reject("Rejected");
                }
            }, 2000  // 超时等待2s，等待长连接建立
        )

    });
}


// 建立长连接
openConn()
hide_all_widgets()