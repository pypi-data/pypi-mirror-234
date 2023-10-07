
from sklearn.metrics import confusion_matrix

class ModelStats:

    def __init__(self,train_x,train_y,test_x,test_y,y_pred,model=None):
        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y
        self.model = model
        self.y_pred = y_pred

    def get_confusion_matrix(self):

        matrix = confusion_matrix(self.test_y.to_numpy(),self.y_pred)
        print(matrix)
        # print(dir(matrix))
        matrix = matrix[::-1]
        cus = []
        i = len(matrix)-1
        while i >= 0:
            print(i)
            for j in range(len(matrix)):
                print([i,j,matrix[i,j]])
                cus.append([i,j,matrix[i,j]])
            i -=1
        return cus

    def get_con_matrix_html(self):
        html = '''
                    var myChart = echarts.init(document.getElementById('modelstats_overview'));
                     // prettier-ignore
                    const hours = ["Positive","Negative"]
                    ];
                    // prettier-ignore
                    const days = [
                        'Negative', 'Positive'
                    ];
                    // prettier-ignore
                    const data = '''+str(self.get_confusion_matrix())+'''.map(function (item) {
                        return [item[1], item[0], item[2] || '-'];
                    });
                    option = {
                      tooltip: {
                        position: 'top'
                      },
                      grid: {
                        height: '50%',
                        top: '10%'
                      },
                      xAxis: {
                        type: 'category',
                        data: hours,
                        splitArea: {
                          show: true
                        }
                      },
                      yAxis: {
                        type: 'category',
                        data: days,
                        splitArea: {
                          show: true
                        }
                      },
                      visualMap: {
                        min: 0,
                        max: 10,
                        calculable: true,
                        orient: 'horizontal',
                        left: 'center',
                        bottom: '15%'
                      },
                      series: [
                        {
                          name: 'Punch Card',
                          type: 'heatmap',
                          data: data,
                          label: {
                            show: true
                          },
                          emphasis: {
                            itemStyle: {
                              shadowBlur: 10,
                              shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                          }
                        }
                      ]
                    };
                myChart.setOption(option);
        '''
        return html



