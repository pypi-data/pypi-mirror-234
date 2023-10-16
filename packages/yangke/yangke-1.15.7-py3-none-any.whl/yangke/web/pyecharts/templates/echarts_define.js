const upColor = '#ec0000';
const upBorderColor = '#8A0000';
const downColor = '#00da3c';
const downBorderColor = '#008F28';
const dataCount = 2e5;
var data = [ // data中的每条数据分别对应：日期、开盘价、最高价、最低价、收盘价、成交量、涨跌标签
    // ["2000-00-00", "open", "high", "low", "close", "volume", "sign"]
];

option = generate_option() // 当data数据改变时，会触发generate_option()方法并将生成的option设置给charts

function generate_option() {

    let _data = data;
    _data = deal_data(_data);  // 根据开盘、收盘等基础数据计算涨跌、MA5等结果数据，并合并数组
    // _data中的每条数据分别对应：日期、开盘价、最高价、最低价、收盘价、成交量、涨跌标签
    // ["2000-00-00", "1:open", "2:high", "3:low", "4:close", "5:volume", "6:sign", "7:ma5", "8:ma10", "9:ma20",
    //  "10:ma30"
    // ]
    return {
        dataset: {
            source: _data
        },
        title: {
            text: 'Data Amount: ' + echarts.format.addCommas(dataCount)
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'  // 'line'  # cross为十字网格线显示，line为单x轴显示
            }
        },
        toolbox: {
            feature: {
                dataZoom: {  // 是否在toolbox中显示缩放区域的按钮
                    yAxisIndex: false
                }
            }
        },
        legend: {
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: [
            {
                left: '5%',
                right: '5%',
                bottom: 200
            },
            {
                left: '5%',
                right: '5%',
                height: 80,
                bottom: 80
            }
        ],
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                // inverse: true,
                axisLine: {onZero: false},
                splitLine: {show: false},
                min: 'dataMin',
                max: 'dataMax'
            },
            {
                type: 'category',
                gridIndex: 1,
                boundaryGap: false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                min: 'dataMin',
                max: 'dataMax'
            },

        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false}
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                // start: 10,  # 数据缩放百分比
                // end: 100,
                show: true,
                color: "#333",
                startValue: Math.max(data.length - 100, 0),  // 数据缩放数值索引
                endValue: data.length - 1,
                minValueSpan: 30,
                maxValueSpan: 300,
            },
            {  // 拖动条形式的缩放工具
                show: true,  // 是否显示
                xAxisIndex: [0, 1],  // 表示拖动条同时控制0、1两个坐标轴，因为有成交量和K线图两个图，因此两个图同步控制
                type: 'slider',
                bottom: 10,
                backgroundColor: "#f3a4f2",
                minValueSpan: 30,
                // maxValueSpan: 3000,
                fillerColor: "#23aaad",
                textStyle: {
                    color: "#000000"
                }
                // startValue: data.length - 100,
                // endValue: data.length
            }
        ],
        visualMap: {
            show: false, // 是否显示涨跌颜色图例
            seriesIndex: 1,
            dimension: 6,
            pieces: [
                {
                    value: 1,  // 定义涨时对应的颜色
                    color: upColor
                },
                {
                    value: -1,
                    color: downColor
                }
            ]
        },
        series: [
            {
                type: 'candlestick',
                itemStyle: {
                    color: upColor,
                    color0: downColor,
                    borderColor: upBorderColor,
                    borderColor0: downBorderColor
                },
                encode: {
                    x: 0, // 指定x轴数据为dataset.source中第一列
                    y: [1, 4, 3, 2]  // 指定candlestick图中OHLC四个价格在dataset中的位置
                }
            },
            {
                name: 'MA5',
                type: 'line',
                xAxisIndex: 0,  // 指定绘制在0,0位置的图中
                yAxisIndex: 0,
                encode: {
                    x: 0, // 指定x轴数据为dataset.source中第一列
                    y: 7  // 指定y轴数据为dataset.source中第二列
                },
                smooth: true,
                lineStyle: {
                    opacity: 0.5,
                    width: 2,
                    type: "solid"
                },

            },
            {
                name: 'MA10',
                type: 'line',
                xAxisIndex: 0,  // 指定绘制在0,0位置的图中
                yAxisIndex: 0,
                encode: {
                    x: 0, // 指定x轴数据为dataset.source中第一列
                    y: 8  // 指定y轴数据为dataset.source中第二列
                },
                smooth: true,
                lineStyle: {
                    opacity: 0.5,
                    width: 2,
                    type: "solid"
                },

            },
            {
                name: 'MA20',
                type: 'line',
                xAxisIndex: 0,  // 指定绘制在0,0位置的图中
                yAxisIndex: 0,
                encode: {
                    x: 0, // 指定x轴数据为dataset.source中第一列
                    y: 9  // 指定y轴数据为dataset.source中第二列
                },
                smooth: true,
                lineStyle: {
                    opacity: 0.5,
                    width: 2,
                    type: "solid"
                },

            },
            {
                name: 'MA30',
                type: 'line',
                xAxisIndex: 0,  // 指定绘制在0,0位置的图中
                yAxisIndex: 0,
                encode: {
                    x: 0, // 指定x轴数据为dataset.source中第一列
                    y: 10  // 指定y轴数据为dataset.source中第二列
                },
                smooth: true,
                lineStyle: {
                    opacity: 0.5,
                    width: 2,
                    type: "solid"
                },

            },
            {
                name: 'Volumn',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                itemStyle: {
                    color: '#7fbe9e'
                },
                large: true,
                encode: {
                    x: 0,
                    y: 5
                }
            },

        ]
    };
}

function calculateMA(dayCount, data) {
    let result = [];
    for (let i = 0, len = data.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        let sum = 0;
        for (let j = 0; j < dayCount; j++) {
            sum += data[i - j][1];
        }
        result.push(sum / dayCount);
    }
    return result;
}


function deal_data(data) {
    let ma5 = calculateMA(5, data)
    let ma10 = calculateMA(10, data);
    let ma20 = calculateMA(20, data);
    let ma30 = calculateMA(30, data);
    let res = merge_array(data, ma5, 1)
    res = merge_array(res, ma10, 1)
    res = merge_array(res, ma20, 1)
    res = merge_array(res, ma30, 1)
    return res;
}

function merge_array(arr1, arr2, axis = 0) {
    // 目前只支持二维数组按行还是按列合并
    let res;
    if (axis === 0) {
        res = arr1.concat(arr2);
    } else {
        let arr = [];
        arr1.forEach((item, i) => {
            let _ = item.concat(arr2[i])
            arr.push(_)
        })
        res = arr
    }
    return res
}