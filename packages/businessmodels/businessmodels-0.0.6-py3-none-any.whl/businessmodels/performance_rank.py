from business_models_initial import chi_performance, chi_performance_parsed_table
class feed_data:
  def __init__(self, data, percentage, column1, column2, column3):
    self.df=data
    self.percentage=percentage
    self.column1=column1
    self.column2=column2
    self.column3=column3
    obj=chi_performance.test(self.df,self.column1, self.column2, self.column3)
    a,b=obj.result()
    self.w=chi_performance_parsed_table.data_feed(self.percentage,self.df,a,b,self.column1, self.column2, self.column3)
  def interpret(self):
    w=self.w
    intprt=w.interpret()
    return intprt
  def output_table(self):
    w=self.w
    op_table=w.output_table()
    return op_table