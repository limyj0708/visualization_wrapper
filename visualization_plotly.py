import plotly.graph_objects as go
import plotly.figure_factory as ff
import statistics as stat
from scipy.stats import ks_2samp, ttest_ind

class CompareDistribution:
    def get_data(self, data_dict:dict):
        self.data_dict = data_dict
    
    def two_distribution_dist_box_Ttest_KStest(self, bin_size):
        list_dict_keys = list(self.data_dict.keys())
        data_1 = self.data_dict[list_dict_keys[0]]
        data_2 = self.data_dict[list_dict_keys[1]]
        
        ttest_result = ttest_ind(data_1, data_2, equal_bar=False)
        # equal_var : If True (default), perform a standard independent 2 sample test that assumes equal population variances.
        #             If False, perform Welch’s t-test, which does not assume equal population variance [2].
        ks_2samp_result = ks_2samp(data_1, data_2)

        hist_data = [data_1, data_2]
        group_labels = list_dict_keys

        fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size, colors=['red', 'blue'])
        fig.update_layout(
            barmode='overlay'
            , title = {
              "text" : f"""<b style="font-size:22;"></b><br><a style="font-size:14;">T-test p-value : {round(ttest_result[1],4)}</a><br><a style="font-size:14;">{round(ks_2samp_result[1],4)}</a>"""
              , "pad" : {"t" : 40}
              , "y" : 1
            }
            , height = 800
            , width = 1000
            , margin=dict(b=0)
            )
        
        fig2 = go.Figure()
        fig2.add_trace(
            go.Box(
                  x=data_1
                , y=list_dict_keys[0] * len(data_1)
                , name=list
                , marker_color='red'
            )
        )
        fig2.add_trace(
            go.Box(
                  x=data_2
                , y=list_dict_keys[1] * len(data_2)
                , name=list
                , marker_color='blue'
            )
        )

        fig2.update_layout(
            height = 400
            , width = 1000
            , margin= {'t':30}
            , legend = {
                'font' : {
                        'size' : 14
                }
            } 
        )
        fig2.update_traces(orientation='h')
        fig2.show()
