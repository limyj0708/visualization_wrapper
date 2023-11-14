import statistics as stat

import plotly.figure_factory as ff
import plotly.graph_objects as go
from scipy.stats import ks_2samp, ttest_ind


def print_table_for_markdown(table:list, first_column_align:str='right', other_columns_align:str='center'):
    """
    2차원 테이블을 나타내는 이중 리스트를 넣으면, Markdown 테이블 형식에 맞는 텍스트로 출력해주는 함수입니다.
    
    ### Return
    - Markdown 테이블 규격에 맞는 텍스트

    ### Parameter
    - table : 이중 리스트. 첫 번째 element는 header가 되어야 합니다. [[헤더1, 헤더2, 헤더3], [값1, 값2, 값3], ...]
    - first_column_align : 첫 번째 컬럼의 정렬방식. 'left', 'right', 'center' 셋 중 하나의 값을 넣어야 합니다. 기본 값은 right입니다.
    - other_columns_align : 나머지 컬럼의 정렬방식. 'left', 'right', 'center' 셋 중 하나의 값을 넣어야 합니다. 기본 값은 center입니다.
    """
    header = table[0]
    header_len = len(header)
    max_text_len_in_columns = [max(len(str(row[i])) for row in table) for i in range(len(header))]
    # header의 원소 index를 각 컬럼을 구분하는 열 번호로 삼는다.
    align_text = ''
    
    if first_column_align == 'left':
        f_align = '|' + ':'+(max_text_len_in_columns[0]+1)*'-' + '|'
        f_align_char = '<'
    elif first_column_align == 'right':
        f_align = '|' + (max_text_len_in_columns[0]+1)*'-' + ':' + '|'
        f_align_char = '>'
    elif first_column_align == 'center':
        f_align = '|' + ':' + (max_text_len_in_columns[0])*'-' + ':' + '|'
        f_align_char = '^'
    else:
        raise ValueError(f"Invalid align value: {first_column_align}. You must use 'left' or 'right' or 'center'.")

    align_text += f_align
        
    if other_columns_align == 'left':
        o_align_char = '<'
        for idx in range(1, header_len):
            align_text += ':'+(max_text_len_in_columns[idx]+1)*'-' + '|'
    elif other_columns_align == 'right':
        o_align_char = '>'
        for idx in range(1, header_len):
            align_text += (max_text_len_in_columns[idx]+1)*'-' + ':' + '|'
    elif other_columns_align == 'center':
        o_align_char = '^'
        for idx in range(1, header_len):
            align_text += ':' + (max_text_len_in_columns[idx])*'-' + ':' + '|'
    else:
        raise ValueError(f"Invalid align value: {other_columns_align}. You must use 'left' or 'right' or 'center'.")
    
    format_text = f'| '
    format_text += '{:' + f_align_char + str(max_text_len_in_columns[0]) + '}' + ' |'
    for idx in range(1,header_len):
        format_text += ' {:' + o_align_char + str(max_text_len_in_columns[idx]) + '}' + ' |'

    len_divider = len(format_text.format(*header)) - 2

    print(format_text.format(*header))
    print(align_text)
    format_text.format(*header)
    for idx in range(1, len(table)):
        print(format_text.format(*table[idx]))
    
    
def print_table_for_cli(table:list, first_column_align:str='right', other_columns_align:str='center'):
    """
    2차원 테이블을 나타내는 이중 리스트를 넣으면, CLI에서 적당히 보기 좋은 테이블로 출력해주는 함수입니다.
    
    ### Return
    - CLI 환경에서 보기 좋은 테이블 텍스트. 아래처럼 출력됩니다.
    +-----------------------------------------------------------+
    |               Test | Statistics | P-value  |    Tttttt    |
    +-----------------------------------------------------------+
    |             T-test |  0.111111  | 0.333333 | 123456000000 |
    | Two sample KS test |  0.222222  | 0.444444 | 123456000000 |
    +-----------------------------------------------------------+

    ### Parameter
    - table : 이중 리스트. 첫 번째 element는 header가 되어야 합니다. [[헤더1, 헤더2, 헤더3], [값1, 값2, 값3], ...]
    - first_column_align : 첫 번째 컬럼의 정렬방식. 'left', 'right', 'center' 셋 중 하나의 값을 넣어야 합니다. 기본 값은 right입니다.
    - other_columns_align : 나머지 컬럼의 정렬방식. 'left', 'right', 'center' 셋 중 하나의 값을 넣어야 합니다. 기본 값은 center입니다.
    """
    header = table[0]
    header_len = len(header)
    max_text_len_in_columns = [max(len(str(row[i])) for row in table) for i in range(len(header))]
    # header의 원소 index를 각 컬럼을 구분하는 열 번호로 삼는다.
        
    if first_column_align == 'left':
        f_align_char = '<'
    elif first_column_align == 'right':
        f_align_char = '>'
    elif first_column_align == 'center':
        f_align_char = '^'
    else:
        raise ValueError(f"Invalid align value: {first_column_align}. You must use 'left' or 'right' or 'center'.")

    if other_columns_align == 'left':
        o_align_char = '<'
    elif other_columns_align == 'right':
        o_align_char = '>'
    elif other_columns_align == 'center':
        o_align_char = '^'
    else:
        raise ValueError(f"Invalid align value: {other_columns_align}. You must use 'left' or 'right' or 'center'.")
    
    format_text = f'| '
    format_text += '{:' + f_align_char + str(max_text_len_in_columns[0]) + '}' + ' |'
    for idx in range(1,header_len):
        format_text += ' {:' + o_align_char + str(max_text_len_in_columns[idx]) + '}' + ' |'

    len_divider = len(format_text.format(*header)) - 2

    print(f'+{"-" * (len_divider)}+')
    print(format_text.format(*header))
    print(f'+{"-" * (len_divider)}+')
    format_text.format(*header)
    for idx in range(1, len(table)):
        print(format_text.format(*table[idx]))

    print(f'+{"-" * (len_divider)}+')

def two_distribution_dist_box_Ttest_KStest(data_dict:dict, plot_title:str, bin_size, alternative='two_sided'):
    """
    두 개의 연속형 변수의 분포를 비교하려고 만든 함수입니다.
    
    ### Return
    - plotly distplot의 histogram+KDE 부분과, 가로형 boxplot를 출력합니다.
    - T-test, Two sample Kolmogorov–Smirnov test의 결과를 출력합니다.
    
    ### Parameter
    - data : {key1:list1, key2:list2}의 구조를 가진 dictionary를 입력합니다. 비교하고 싶은 두 개의 데이터셋이 들어가 있어야 합니다.
    - plot_title : 플롯의 제목
    - bin_size : distplot의 historgram bin size입니다.
    - alternative : 양측검정인지, 단측검정인지 입력합니다. 기본 값은 'two_sided' 입니다.
      - {‘two-sided’, ‘less’, ‘greater’}, optional 
    """
    list_dict_keys = list(data_dict.keys())
    key_1 = list_dict_keys[0]
    key_2 = list_dict_keys[1]
    data_1 = data_dict[key_1]
    data_2 = data_dict[key_2]
    
    ttest_result = ttest_ind(data_1, data_2, alternative=alternative, equal_var=False)
    # equal_var : If True (default), perform a standard independent 2 sample test that assumes equal population variances.
    #             If False, perform Welch’s t-test, which does not assume equal population variance [2].
    ks_2samp_result = ks_2samp(data_1, data_2, alternative=alternative)

    hist_data = [data_2, data_1]
    group_labels = [list_dict_keys[1], list_dict_keys[0]]

    fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size, colors=['blue', 'red'], show_rug=False)
    fig.update_layout(
        barmode = "overlay"
        , title = {
            'text' : f"""<b style="font-size:22;">{plot_title}</b><br><a style="font-size:14;">T-test, p-value : {round(ttest_result[1],4)}</a><br><a style="font-size:14;">KS_test, p_value : {round(ks_2samp_result[1],4)}</a>"""
            , 'pad' : {"t" : 40}
            , 'y' : 1
        }
        , height = 750
        , width = 1000
        , margin={'b':0}
        , legend = {
            'font' : {'size' : 14}
            , 'traceorder': "reversed"    
        } 
    )
    fig.update_traces(opacity=0.4)
    
    fig2 = go.Figure()
    fig2.add_trace(
        go.Box(
                x = data_2
            , y = [key_2] * len(data_2)
            , name = key_2
            , marker_color = "blue"           
        )
    )
    fig2.add_trace(
        go.Box(
                x = data_1
            , y = [key_1] * len(data_1)
            , name = key_1
            , marker_color = "red"
        )
    )
    fig2.update_layout(
            height = 250
        , width = 1000
        , margin= {'t':30}
        , legend = {
                'font' : {'size' : 14}
            , 'traceorder' : "reversed"
        } 
    )
    fig2.update_traces(orientation = 'h')
    
    fig.show()
    fig2.show()

    print_table_for_markdown(table=[['Test', 'Statistics', 'P-value'], ['T-test', round(ttest_result[0],8), round(ttest_result[1],8)], ['Two sample KS test', round(ks_2samp_result[0],8), round(ks_2samp_result[1],8)]])


def one_distribution_dist_box(data_dict:dict, plot_title:str, bin_size):
    """
    데이터셋 하나에 대한 분포를 시각적으로 확인하려고 만든 함수입니다.
    # Return
    - plotly distplot의 histogram+KDE 부분과, 가로형 boxplot이 출력됩니다.
    
    # Parameter
    - data : {key1:list1}의 구조를 가진 dictionary를 입력합니다.
    - plot_title : 플롯의 제목
    - bin_size : distplot의 historgram bin size입니다.
    """
    list_dict_keys = list(data_dict.keys())
    key_1 = list_dict_keys[0]
    data_1 = data_dict[key_1]

    hist_data = [data_1]
    group_labels = [list_dict_keys[0]]

    fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size, colors=['red'], show_rug=False)
    fig.update_layout(
        barmode = "overlay"
        , title = {
        'text' : f"""<b style="font-size:22;">{plot_title}</b>"""
        , 'pad' : {"t" : 40}
        , 'y' : 1
        }
        , height = 750
        , width = 1000
        , margin={'b':0}
        , legend = {
            'font' : {'size' : 14}
        , 'traceorder': "reversed"    
        } 
    )
    fig.update_traces(opacity=0.4)
    
    fig2 = go.Figure()
    fig2.add_trace(
        go.Box(
            x = data_1
            , y = [key_1] * len(data_1)
            , name = key_1
            , marker_color = "red"
        )
    )
    fig2.update_layout(
        height = 250
        , width = 1000
        , margin= {'t':30}
        , legend = {
            'font' : {'size' : 14}
            , 'traceorder' : "reversed"
        } 
    )
    fig2.update_traces(orientation = 'h')
    
    fig.show()
    fig2.show()