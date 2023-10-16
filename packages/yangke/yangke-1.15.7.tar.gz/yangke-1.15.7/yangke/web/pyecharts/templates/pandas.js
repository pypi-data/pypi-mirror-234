function type(obj) {
    if (!obj) {
        if (obj !== 0) {
            return "null";
        }
    }
    return obj.constructor.name;
}

export function split(string, sep, num) {
    /**
     * 类似于python的split函数，第三个参数num限定了分割后数组的长度，行为和js的split函数不同
     */
    let list = string.split(sep);

    if (num < list.length) {
        let last = list[num - 1];
        for (let i = num; i < list.length; i++) {
            console.log(i);
            last = last + sep + list[i];
        }
        list[num - 1] = last;
        return list.slice(0, num)
    } else {
        return list;
    }
}

export function range(start, end, step) {
    return Array.from({length: Math.ceil((end - start) / step.toFixed(2))}, (e, i) => start + i * step)
}

function getStringLength(str) {
    /**
     * 获取字符串长度，其中中文字符长度按2统计
     * @type {number}
     */
    let totalLength = 0;
    const list = str.split("");
    for (let i = 0; i < list.length; i++) {
        const s = list[i];
        if (s.match(/[\u0000-\u00ff]/g)) { //半角
            totalLength += 1;
        } else if (s.match(/[\u4e00-\u9fa5]/g)) { //中文
            totalLength += 2;
        } else if (s.match(/[\uff00-\uffff]/g)) { //全角
            totalLength += 2;
        }
    }
    return totalLength;
}

export function format_string(str, length = 20) {
    /**
     * 在字符串str前补空格，将其长度补为length
     */
    if (!str && str !== 0) {
        str = ""
    } else {
        str = String(str);
    }
    let num = length - getStringLength(str);
    if (num > 0) {
        for (let i = 0; i < num; i++) {
            str = " " + str
        }
    }
    return str;
}

class Series {
    constructor(data, name) {
        if (type(data) === "Series") { // 如果传入的data对象是一个Series，则直接返回该对象即可
            return data;
        }
        if (data.length !== name.length) {
            console.error("Series：数据和数据名数组长度不行等")
            return null
        }
        this.data = data;
        this.length = data.length;
        this.name = name;
        if (!this.name) {  // 如果name为空，则自动分配整数索引的行名
            this.name = [];
            for (let i = 0; i < this.length; i++) {
                this.name.push(i);
            }
        }
    }

    get_value_by_name(name) {
        /**
         * 根据行名获取Series的值
         */
        for (let i=0;i<this.length;i++) {
            if (this.name[i] === name) {
                return this.data[i];
            }
        }
    }

    toArray() {
        /**
         * 将Series转换为Array，并保持顺序不变
         * @type {*[]}
         */
        let res = [];
        for (let i = 0; i < this.length; i++) {
            res.push(this.data[i]);
        }
        return res
    }

    get_value_by_index(index) {
        /**
         * 根据行索引获取Series的值
         */
        return this.data[index];
    }

    print() {
        let title_str;
        for (let i in this.name) {
            title_str = format_string(this.name[i]) + format_string(this.data[i])
            console.log(title_str);
        }
    }
}

class DataFrame {
    constructor(data) {
        if (type(data) === "DataFrame") {
            return data;
        }
        this.data = data;
        this.title = []  // 行名
        this.index = []  // 列名
        this.shape = [data.length, data[0].length];
        for (let i = 0; i < this.shape[0]; i++) {
            this.index.push(i)
        }
        for (let i = 0; i < this.shape[1]; i++) {
            this.title.push(i);
        }
    }

    dropna(axis = 0, how = "all") {
        /**
         * 删除空行货空列
         */
        if (axis === 0) { // 删除空行

        } else if (axis === 1) {
            // 删除空列
        } else {
            return this.data
        }
    }

    get_index_by_name(name, axis = 0) {
        /**
         * 获取行或列标题对应的索引
         */
        if (axis === 0) {
            for (let i in this.index) {
                if (this.index[i] === name) {
                    return i;
                }
            }
        } else if (axis === 1) {
            for (let i in this.title) {
                if (this.title[i] === name) {
                    return i;
                }
            }
        }
    }

    get_row_by_name(rol_name) {
        /**
         * 根据行名获取行数组
         * axis=0表示获取行，axis=1表示获取列
         */
        for (let idx in this.index) {
            if (rol_name === this.index[idx]) {
                return new Series(this.data[idx], this.title)
            }
        }
        return null
    }

    get_column_by_name(col_name) {
        /**
         * 根据列名获取列数组
         */
        for (let idx in this.title) {
            if (col_name === this.title[idx]) {
                return new Series(this.get_series_by_index(idx, 1), this.index)
            }
        }
    }

    get_series_by_index(index, axis = 0) {
        /**
         * 根据索引获取数组，axis=0表示获取行，axis=1表示获取列
         */
        if (axis === 1) {
            let col_arr = [];
            for (let row of this.data) {
                col_arr.push(row[index])
            }
            return new Series(col_arr, this.index);
        } else {
            return new Series(this.data[index], this.title)
        }
    }

    drop_by_index(index, axis = 0) {
        /**
         * 按索引删除dataframe中的某一行或列，该方法不是按列名或行名，而是按索引
         */
        if (axis === 0) {
            this.data.splice(index, 1);
            this.index.splice(index, 1);
        } else {
            for (let row of this.data) {
                row.splice(index, 1)
            }
            this.title.splice(index, 1)
        }
    }

    drop_by_name(name, axis = 0) {
        /**
         * 按标题删除dataframe中的某一行或列
         */
        this.drop_by_index(this.get_index_by_name(name, axis), axis)
        return this
    }

    set_axis(key_or_labels, axis = 0) {
        /**
         * 参考python-pandas库
         */
        if (axis === 0) { // 设置行标题
            this.set_index(key_or_labels)
        } else {
            // 设置列标题
            if (type(key_or_labels) === "Array") {
                this.title = key_or_labels
            } else if (type(key_or_labels) === "Series") {
                this.title = key_or_labels.data;
            } else if (type(key_or_labels) === "Number") {
                let title = this.get_series_by_index(key_or_labels);
                this.title = title.data;
                this.drop_by_index(key_or_labels, 0)
            }
        }
    }

    set_index(key) {
        /**
         * 参考python-Pandas库
         */
        if (type(key) === "Array") { // 传入数组
            // 说明传入的key是列表
            this.index = key
        } else if (type(key) === "Series") {
            this.index = key.data
        } else if (type(key) === "Number") { // 说明传入的是列名
            this.set_index(this.get_series_by_index(key, 1))
            this.drop_by_index(key, 1)
        }
    }



    print() {
        let title_str = format_string("");
        for (let i of this.title) {
            title_str = title_str + format_string(i)
        }
        console.log(title_str);
        for (let idx in this.data) {
            let row_str = format_string(this.index[idx]);
            for (let cell of this.data[idx]) {
                let str = format_string(cell)
                row_str = row_str + str
            }
            console.log(row_str);
        }
    }
}

export default {
    DataFrame,
    Series,
    type,
    getStringLength
};

// let x = new DataFrame([["", "THA", "TRL", "VWO"],
//     ["主汽温度", 11, 12, 13],
//     ["高压门杆漏气", 21, 22, 23]]);
// x.print();
// console.log(type(x))
// x.set_index(0)
// console.log("--------------------------------------")
// x.print()
// x.set_axis(0, 0)
// console.log("--------------------------------------")
// x.print()