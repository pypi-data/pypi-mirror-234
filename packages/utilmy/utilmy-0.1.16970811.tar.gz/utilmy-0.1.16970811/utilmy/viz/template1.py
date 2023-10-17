""" Usage template to copy paste
Docs::

   pip install python-box python-highcharts mpld3 pandas-highcharts fire --quiet
   pip install pretty_html_table pyvis  utilmy

   https://arita37.github.io/myutil/en/zdocs_y23487teg65f6/utilmy.viz.html#module-utilmy.viz.vizhtml

    https://colab.research.google.com/drive/1NYQZrfAPqbuLCt9yhVROLMRJM-RrFYWr#scrollTo=Rrho08zYe6Gj
    https://colab.research.google.com/drive/1NYQZrfAPqbuLCt9yhVROLMRJM-RrFYWr#scrollTo=2zMKv6MXOJJu


"""

#################################################################################################################
#############  Template 1 #######################################################################################
from utilmy.viz import vizhtml as vi
import pandas as pd


url = 'https://raw.githubusercontent.com/AlexAdvent/high_charts/main/data/stock_data.csv'
df = pd.read_csv(url)
df.head()

doc = vi.htmlDoc(title='Stock Market Analysis',css_name = "border")

doc.h2('Stock Market Analysis')
doc.h4('Stock Data plot')
doc.table(df, use_datatable=True, table_id="test", custom_css_class='intro')
doc.hr()
doc.h4('Stock tseries graph') 
doc.plot_tseries(df,coldate='Date', date_format= '%m/%d/%Y', coly1=['Open', 'High', 'Low', 'Close'], coly2=['Turnover (Lacs)'],
                  title = "Stock",cfg={},mode='highcharts'
                 )
doc.hr()

doc.save('stock market analysis.html')

"""## Graph"""

doc = vi.htmlDoc(title='Graph Component')

# dataset for garph
df = pd.DataFrame({ 'from':['A', 'B', 'C','A'], 'to':['D', 'A', 'E','C'], 'weight':[1, 2, 1,5]})
doc.h4('Graph Data plot')
doc.table(df, use_datatable=True, table_id="test", 
    custom_css_class='intro')
doc.pd_plot_network(df, cola='from', colb='to', 
    coledge='col_edge',colweight="weight")

doc.save('graphplot.html')



#################################################################################################################
#############  Template 2 #######################################################################################























