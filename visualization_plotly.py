import plotly.graph_objects as go
import plotly.figure_factory as ff
import statistics as stat
from scipy.stats import ks_2samp, ttest_ind

class CompareDistribution:
    def get_data(self, data_dict:dict):
        self.data_dict = data_dict
    
    def two_distribution_dist_box_Ttest_KStest(self, plot_title, bin_size):
        list_dict_keys = list(self.data_dict.keys())
        key_1 = list_dict_keys[0]
        key_2 = list_dict_keys[1]
        data_1 = self.data_dict[key_1]
        data_2 = self.data_dict[key_2]
        
        ttest_result = ttest_ind(data_1, data_2, equal_var=False)
        # equal_var : If True (default), perform a standard independent 2 sample test that assumes equal population variances.
        #             If False, perform Welch’s t-test, which does not assume equal population variance [2].
        ks_2samp_result = ks_2samp(data_1, data_2)

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