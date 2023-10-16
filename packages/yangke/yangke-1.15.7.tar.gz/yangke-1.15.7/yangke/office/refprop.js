function fluid_string(燃料体积分数数组, 燃料气名称数组_opt) {
    /**
     * 参考REFPROP示例xls文件的FluidString函数，生成混合气体的描述字符串
     * 气体体积分数数组默认参考wps宏.js，也可以指定
     */
    let result = ""
    let data_list = _get_arr_of_range(燃料体积分数数组)
    if (!燃料气名称数组_opt) {
        let 组分名列表 = 常量().组分名列表;
        let refprop_name = 常量().REFPROP_Name;
        for (let i = 0; i < 组分名列表; i++) {
            if (data_list[i] !== 0) {
                let 组分名 = 组分名列表[i];
                let prop_name = refprop_name[组分名];
                result = result + prop_name + ";" + data_list[i] + ";"
            }
        }
    }
    return result;
}

function 焓_refprop(压力_MPa, 温度_K, 燃料气体积分数数组) {
    let string = fluid_string(燃料气体积分数数组);
    return Enthalpy(string, "PT", "SI", 压力_MPa, 温度_K);
}

function 密度_refprop(压力_MPa, 温度_K, 燃料气体积分数数组) {
    let string = fluid_string(燃料气体积分数数组);
    return Density(string, "PT", "SI", 压力_MPa, 温度_K);
}

function 低位热值_refprop(压力_MPa, 温度_K, 燃料气体积分数数组) {
    let string = fluid_string(燃料气体积分数数组);
    return NetHeatingValue(string, "PT", "SI", 压力_MPa, 温度_K);
}

function 高位热值_refprop(压力_MPa, 温度_K, 燃料气体积分数数组) {
    let string = fluid_string(燃料气体积分数数组);
    return NetHeatingValue(string, "PT", "SI", 压力_MPa, 温度_K);
}