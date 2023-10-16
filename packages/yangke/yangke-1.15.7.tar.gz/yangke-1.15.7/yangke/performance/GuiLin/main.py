from yangke.common.fileOperate import read_csv_ex


def nn_fit(file, x_titles, y_titles):
    """
    根据file中的数据，以x_titles列为输入，y_titles列为输出，拟合神经网络模型

    :param file:
    :param x_titles:
    :param y_titles:
    :return:
    """
    data = read_csv_ex(file)
    x_df = data[x_titles]
    y_df = data[y_titles]
