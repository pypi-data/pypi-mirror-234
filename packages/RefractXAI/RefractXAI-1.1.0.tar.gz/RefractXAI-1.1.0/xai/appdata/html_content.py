import random
import pandas as pd
def getMetricsHtml(metrics):
    html = '''
    "<table><thead><tr><th><b>Metric</b></th><th><b>Value</b></th></tr></thead><tbody>'''
    temp = ""
    for key,value in metrics.items():
        temp += f"<tr><td>{key}</td><td>{value}</td></tr>"

    html += temp
    html += '''</tbody></table>";'''
    modelMetrcis = '''function getModelMetrics() {
    let data = '''+html+'''
    document.getElementById('modelstats_overview_metrics').innerHTML = data };
    \n
    '''
    return modelMetrcis

def getConfusionMatrixHtml(confusionMatrix):
    # getConfusionMatrix
    maxValue = max(list(confusionMatrix.ravel()))
    tableCode = '''"<b>Confusion Matrix:</b></br><table><tr><td style='border:hidden'></td>'''
    matrxiLength = len(confusionMatrix)
    for i in range(matrxiLength):
        tableCode += f"<td style='border:hidden'>{i}</td>"
    tableCode += "</tr>"

    for i in range(matrxiLength):
        tableCode += f"<tr><td style='border:hidden'>{i}</td>"
        for j in range(matrxiLength):
            value = confusionMatrix[i][j]
            l = (value/maxValue)*100
            textColor = "#FFF" if int(l) < 35 else "#000"
            tableCode += f"<td style='background: hsl(310, 100%,{int(l)}%); color:{textColor}'>{value}</td>"
        tableCode += "</tr>"
    tableCode += '''</table>";'''
    html = '''
    function getConfusionMatrix(){
    let table ='''+str(tableCode)+'''
    document.getElementById('modelstats_overview').innerHTML = table
    }
    '''
    return html

def getRegressionPlot(data):
    target_name = data['target_name']
    axisLimits = data["rangePayload"]
    x_min = int(axisLimits["x_min"]) + 1
    x_max = int(axisLimits["x_max"]) + 1
    y_min = int(axisLimits["y_min"]) + 1
    y_max = int(axisLimits["y_max"]) + 1
    payLoad = data["regData"]
    echartHtml = '''
    function getRegressionPlot(){
    var regressionChart = echarts.init(document.getElementById("modelstats_overview_plots"));
        option = {
        title: {
                            text: 'Regression Plot',
                            x: 'center'
                            },
                          tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                              type: 'shadow'
                            }
        },
          xAxis: {
          name: "Actual '''+str(target_name)+''' value",
          min: '''+str(x_min)+''',
          max: '''+str(x_max)+''',
            nameGap: 0,
            nameTextStyle: {
            align: 'right',
            verticalAlign: 'top',
            padding: [30, 0, 0, 0],
        },
          },
          yAxis: {
          name: "Predicted '''+str(target_name)+''' value",
          min: '''+str(y_min)+''',
          max: '''+str(y_max)+'''
          },
          series: [
            {
              symbolSize: 5,
              data: '''+str(payLoad)+''',
              type: 'scatter'
            }
          ]
        };
        regressionChart.setOption(option);
    };
'''
    return echartHtml

def get_regression_stats_html(data):
    htmlScript = ""
    metrics = data["metrics"]
    regressionData = data["regression_plot"]
    htmlScript = '''
        $(window).on("load", function () {
        getModelMetrics();
        getRegressionPlot();
        });
    '''
    htmlScript += getMetricsHtml(metrics)
    htmlScript += getRegressionPlot(regressionData)
    return htmlScript

def getRocaucCurveHtml(roc_auc_data):

    roc_hashes = ""
    for entity in roc_auc_data:
        tempData = roc_auc_data[entity]
        roc_hashes += '''
            \"''' + str(entity) + '''\" : 
                    {
                    'payload': ''' + str(tempData["payload"]) + ''',
                    'auc_score': \"''' + str(tempData["auc_score"]) + '''\",
                    'maxvalue': ''' + str(tempData["maxValue"]) + ''',
                },
        '''
    roc_hashes = '''
    {'''+str(roc_hashes)+'''}
    '''
    roc_on_change_script = '''
     function getmulticlasslabelsroc(){
          var classname = $("#list_class_labels_roc").val();
          var rocpaylod = getrocpaylod(classname);
          var data = rocpaylod["payload"];
          var maxvalue = rocpaylod["maxvalue"];
          getRocAucCurve(data,maxvalue);
    }
    \n
    '''

    roc_content_script = "function getrocpaylod(classname){var data ="+roc_hashes+";return data[classname]}"

    # roc_auc_data=roc_auc_data["class_0"]
    # data = roc_auc_data["payload"]
    # auc_score  = roc_auc_data["auc_score"]
    # maxValue = roc_auc_data["maxValue"]

    echartHtml = '''
    \n
    function getRocAucCurve(data,maxvalue){
        var myChart = echarts.init(document.getElementById('modelstats_overview_plots'));
        option = {
              title: {
                text: 'Roc-Auc Curve',
                x: 'center'
                },
                tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
              },
               xAxis: {
                name: "FP Rate"
              },
              yAxis: {
                name: "True Positive Rate"
              },
              series: [
                {
                  data: data,
                  type: 'line'
                },
                {
                  data : [0, maxvalue],
                  type: 'line',
                  color: 'red'
                }
              ]
            };  
        myChart.setOption(option);
    }
    '''
    htmlScript = roc_on_change_script
    # htmlScript += roc_label_script
    htmlScript += roc_content_script
    htmlScript += echartHtml

    return  htmlScript

def get_binary_stats_html(data):
    htmlScript = ""
    metrics = data["metrics"]
    confusionMatrix = data["confusion_matrix_ui"]
    rocAucData = data["roc_auc"]
    htmlScript = '''
        $(window).on("load", function () {
        getModelMetrics();
        getConfusionMatrix();
        getmulticlasslabelsroc();
        });
    '''
    htmlScript += getMetricsHtml(metrics)
    htmlScript += getConfusionMatrixHtml(confusionMatrix)
    htmlScript += getRocaucCurveHtml(rocAucData)
    return htmlScript

def get_classification_stats_html(data):
    htmlDiv = ""
    htmlScript = ""
    metrics = data["metrics"]
    confusionMatrix = data["confusion_matrix_ui"]
    rocAucData = data["roc_auc"]
    htmlScript = '''
        $(window).on("load", function () {
        getModelMetrics();
        getConfusionMatrix();
        getmulticlasslabelsroc();
        });
    '''
    htmlScript += getMetricsHtml(metrics)
    htmlScript += getConfusionMatrixHtml(confusionMatrix)
    htmlScript += getRocaucCurveHtml(rocAucData)
    return htmlScript

def get_model_overview_html(ml_data,model_type):

    if model_type == "regression":
        return get_regression_stats_html(ml_data)
    if model_type == "binaryclassification":
        classNames  =  list(ml_data["roc_auc"].keys())
        return get_binary_stats_html(ml_data)
    if model_type == "multiclassification":
        classNames  =  list(ml_data["roc_auc"].keys())
        return get_classification_stats_html(ml_data)

def insert_class_labels_lime(lime_data):
    if not "regressionMode" in lime_data:
        classnames = list([lime_data[row_no].keys() for row_no in lime_data][0])
        html_options = ""
        for name in classnames:
            html_options += "<option>"+str(name)+"</option>"
        html = '''
            <label for="dataClasses"> Class :</label>
            <select id="list_lime_class" onchange="getlimerows()">'''+html_options+''''</select>   
        '''
        return html,classnames
    return "",""

def get_lime_html(lime_data,classnames):
    lime_info = ""
    model_type = None
    target_name = None
    if not "regressionMode" in lime_data:
        model_type = "classification"
        lime_info = '''new Map([
        '''
        for row_num in lime_data:
            classData = lime_data[row_num]
            lime_info += '''
                ['''+str(row_num)+''',new Map([
                '''
            for className in classData.keys():
                data = classData[className]
                lime_info += '''
                    ["'''+className +'''",new Map([
                    '''
                lime_info += '''
                    ['predicted_value','''+str(data['predicted_value'])+'''],
                    ['list','''+str(data['list'])+'''],
                    ['feature_values','''+str(data['feature_values'])+''']
                '''
                lime_info += '''
                    ])],
                '''
            lime_info += '''
                ])],
            '''
        lime_info +='''
        ]);
        '''

    if "regressionMode" in lime_data:
        model_type = "regression"
        target_name = lime_data["target_name"] if "target_name" in lime_data else  None
        lime_data.pop("regressionMode")
        lime_data.pop("target_name")
        lime_info = ""
        for row_num in lime_data:
            regData = lime_data[row_num]
            lime_info += '''
                '''+str(row_num)+''' : {
                            "predicted_value":
                                {
                                "maxValue":'''+str(regData["predicted_value"]["maxValue"])+''',
                                "minValue":'''+str(regData["predicted_value"]["minValue"])+''',
                                "predictedValue":'''+str(regData["predicted_value"]["predictedValue"])+'''
                                },
                            "feature_values":'''+str(regData["feature_values"])+''',
                            "list":'''+str(regData["list"])+'''
                        },
            '''
        lime_info = '''
            {'''+lime_info+'''};
        '''

    lime_html = '''
         $(window).on('load', function() {
         getlimerows();

         });
        
        function getModelType(){
            return "'''+model_type+'''"
        }

       function getlimerows() {
          var lime_row_number = $("#list_lime__rows").val();
          var lime_class_name = $("#list_lime_class").val();
          var limecontent = getlimeinfo(lime_row_number,lime_class_name);
          var modelType = getModelType();
          getLimePercentageTable(limecontent,modelType,lime_class_name=lime_class_name);
       }


    function getLimePercentageTable(limecontent,modelType,lime_class_name=undefined){
        if (modelType=="regression") {
        
          var predictPerct = limecontent["predicted_value"];
          var listInfo = limecontent["list"];
          var featureInfo = limecontent["feature_values"];

          loadlimepercenthtml(predictPerct,mode=modelType);
          loadlimebarplots(listInfo);

          loadrowtablecontent(featureInfo);
        }
        else {
          var predictPerct = limecontent.get("predicted_value");
          var listInfo = limecontent.get("list");
          var featureInfo = limecontent.get("feature_values");

          loadlimepercenthtml(predictPerct,lime_class_name,mode=modelType);

          loadlimebarplots(listInfo);

          loadrowtablecontent(featureInfo);
        }

    };


    function loadrowtablecontent(featureInfo){
        html_content = "<b>Feature Values</b></br>";
        html_content += "<table style='border-style: solid'>";
            for (var i in featureInfo) {
                        if (featureInfo[i][2] == "positive"){

                            html_content += '<tr><td style="background-color:#ff9966;border:solid">'+featureInfo[i][1].toString()+'</td><td style="background-color:#ff9966;border:solid">'+featureInfo[i][0].toString()+'</td></tr>';
                    }
                    if (featureInfo[i][2] == "negative"){
                        html_content += '<tr><td style="background-color:#80aaff;border:solid">'+featureInfo[i][1].toString()+'</td><td style="background-color:#80aaff;border:solid">'+featureInfo[i][0].toString()+'</td></tr>';
                    }
            }

        html_content += '</table>';
        document.getElementById("row_tablecontent").innerHTML = html_content;
    }

    function loadlimebarplots(listInfo){
     var listKeys = [];
     var listValues = [];
     console.log(listKeys,listValues);
     for (var key in listInfo) {
            listKeys.push(key);
            if (listInfo[key]<0){
                 var valueInfo = {
                          "value": listInfo[key],
                          "label": "labelRight" ,
                          "itemStyle": {"color": '#80aaff'}
                        };
                 listValues.push(valueInfo);
            }
            if (listInfo[key]>=0){
                 var valueInfo = {
                          "value": listInfo[key],
                          "itemStyle": {"color": '#ff9966'}
                  };
                listValues.push(valueInfo);
            }
        }
        var limeChart = echarts.init(document.getElementById('lime_bar_plot'));
         const labelRight = {
           position: 'right'
         };
         option = {
          title: {
              text: 'Local Feature Importance ',
              x: 'center'
            },
                tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
           xAxis: {

             type: 'value',
             position: 'top'
           },
           yAxis: {
             type: 'category',
             axisLine: { show: false },
            axisLabel: { show: false },
            axisTick: { show: false },
            splitLine: { show: false },
             data: listKeys
           },
           series: [
             {
               name: 'Cost',
               type: 'bar',
               stack: 'Total',
               label: {
             show: true,
             formatter: '{b}'
               },
               data: listValues
             }
           ]
         };
     limeChart.setOption(option);

    }

    \n
        
    function getlimeinfo(lime_row_number,lime_class=undefined) {
        var map_objects = ''' + str(lime_info) + ''';
        if (lime_class){
            return map_objects.get(parseInt(lime_row_number)).get(lime_class);
        }
        return map_objects[lime_row_number];
    }

\n    
     function loadlimepercenthtml(predictPerct,classname,mode="regression"){
        console.log(predictPerct,classname,mode);
                if (mode=="regression") {
            var maxValue  = predictPerct["maxValue"].toFixed(0);
            var target_name = "'''+str(target_name)+'''";
            var minValue = predictPerct["minValue"].toFixed(0);
            var predictedValue = predictPerct["predictedValue"].toFixed(0);
            var classValue  = (predictedValue-minValue)/(maxValue-minValue);
            var classPercentageValue =  (classValue*100).toFixed(0);
            var	html_content = "<label>Predicted "+target_name+" value: <b>"+predictedValue.toString()+"</b></label>";
            html_content += "<p> Confidence Interval (CI) : <br>( <b>"+minValue.toString()+"</b>,<b>"+maxValue.toString()+"</b> )</p>";
            html_content += "<table style='width:100%'>";
            html_content += "<p>CI is the range of reasonable predicted values on similar data for the current instance</p>";
            html_content += "<p>Current prediction value is <b>"+classPercentageValue.toString()+"%</b> of Confidence Interval </p>";
            html_content += "<tr><td style='border:solid'><div style='width: "+(classPercentageValue).toString()+"%; background-color: #ff9966;float:left;'>&nbsp;</div>"+(classPercentageValue).toString()+"%</td></tr>";
            html_content += "</table>";
            html_content += "</br>";
            html_content += "<div><div style='width: 10%; background-color: #ff9966;float:left;'>&nbsp;</div><div style='padding-left:30px'> Postive </div></div>";
            html_content += "</br>";
            html_content += "<div><div style='width: 10%; background-color: #80aaff;float:left;'>&nbsp;</div><div style='padding-left:30px'> Negative </div></div>";
            document.getElementById("lime_class_percentage").innerHTML = html_content;
        }
        else {
         var classValue  = parseFloat(predictPerct[classname]);
         var classPercentageValue =  (classValue*100).toFixed(0);
         var	html_content = "<table>";
         html_content += "<p><b>Predictive Percentage</b></p>";
         html_content += "<tr style='width :100%'><td style='border:solid'><b>Positive</b></td><td style='width:100% ;border:solid'><div style='width: "+(classPercentageValue).toString()+"%; background-color: #ff9966;float:left;'>&nbsp;</div></br>"+(classPercentageValue).toString()+"%</td></tr>";
         html_content += "<tr style='width :100%'><td style='border:solid'><b>Negative</b></td><td style='width:100% ;border:solid'><div style='width: "+(100-classPercentageValue).toString()+"%; background-color: #80aaff;float:left;'>&nbsp;</div></br>"+(100-classPercentageValue).toString()+"%</td></tr>";
         html_content += "</table>";
         html_content += "<p>For current index, probability of prediction made for the class:<b>"+(classname).toString()+"</b> is:<b>"+classPercentageValue.toString()+"%</b></p>";
         html_content += "</br>";
        html_content += "<div><div style='width: 10%; background-color: #ff9966;float:left;'>&nbsp;</div><div style='padding-left:30px'> Postive </div></div>";
        html_content += "</br>";
        html_content += "<div><div style='width: 10%; background-color: #80aaff;float:left;'>&nbsp;</div><div style='padding-left:30px'> Negative </div></div>";
        document.getElementById("lime_class_percentage").innerHTML = html_content;
        }
    }
     '''
    return lime_html

def insert_dplot_rows_class_info(shap_data_info):
    modelClassificationInfo = None
    shap_data = None
    htmlRows = ""
    htmlClasses = ""
    if "classificationDplot" in shap_data_info:
        modelClassificationInfo = shap_data_info["modelInfo"]
        shap_data = shap_data_info["classificationDplot"]

        htmlOptionsClasses = ""
        for i in list(shap_data.keys()):
            htmlOptionsClasses += f"<option>{i}</option>"

        htmlClasses = '''
            <label for="dataClasses"><b>Class :</b></label>
            <select id='dplot_class_name' onchange='getdplotrows()'>'''+htmlOptionsClasses+''''</select>   
        '''
        import random
        sample_class = random.choice(list(shap_data.keys()))

        sample_rows = list(shap_data[sample_class].keys())

        htmlRowOptions = ""
        for row_no in sample_rows:
            htmlRowOptions += f"<option>{row_no}</option>"

        htmlRows = '''
            <label for="dataRow"><b>Index no :</b></label>
            <select id='list_dplot_row' onchange='getdplotrows()'>''' + htmlRowOptions + ''''</select>   
        '''

    else:
        shap_data = shap_data_info["regressionDplot"]

        sample_rows = list(shap_data.keys())

        htmlRowOptions = ""
        for row_no in sample_rows:
            htmlRowOptions += f"<option>{row_no}</option>"

        htmlRows = '''
            <label for="dataRow"><b>Index no :</b></label>
            <select id='list_dplot_row' onchange='getdplotrows()'>''' + htmlRowOptions + ''''</select>   
        '''

    return htmlRows,htmlClasses

def insert_dplot_plot(dplot_data):
    # shap_data["classificationDplot"] = tempClassInfo
    # shap_data["modelInfo"] = {"name": "classification", "no_classes": len(expected_values)}

    model_type = "classification"
    if "regressionDplot" in dplot_data:
        model_type  = "regression"

    dplot_hashes = ""
    shap_data = None

    if model_type == "regression":
        shap_data = dplot_data["regressionDplot"]
    else:
        shap_data = dplot_data["classificationDplot"]


    onload_html = '''
        $(window).on('load', function() {
            getdplotrows()

    });

    \n
    function getdplotrows() {
        var row_number = $("#list_dplot_row").val();
        var class_name = $("#dplot_class_name").val();
       var dplotcontent = getdplotinfo(row_number,class_name);
       loaddplotchart(dplotcontent);
       loaddplotinfo(dplotcontent,class_name);
       } 

    function getModeltype(){
        return '''+str(model_type)+''';
    }
    \n

        
    function loaddplotinfo(dplotcontent,classname=undefined){
      max_value = dplotcontent["data"][0];
      mean_value = dplotcontent['meanValue'];
      target_name = dplotcontent['target_name'];
      if (classname){
        html_content = "<div style='padding-top:10px'><b style='color:#c033c9'>Description :</b> Plot explains the Model Prediction behavior for current index on <b>Prediction Probability vs Features</b>. </br>Green line indicates the average prediction made by all indexes for class :<b>"+classname+"</b>.</br>Final Predictive Prabability:<b>"+max_value.toString()+"</b></br>Mean Predictive Probability :<b>"+mean_value.toString()+"</b></div>";
        document.getElementById("dplot_info").innerHTML = html_content;
    }
      if (!classname){
          html_content = "<div style='padding-top:10px'><b style='color:#c033c9'>Description :</b> Plot explains the  Model Prediction behavior for current index on Target Column <b>"+target_name.toString()+"Vs Features</b>.</br>Green line indicates the average prediction made by all indexes.</br>Final Predictive "+target_name.toString()+" Value:<b>"+max_value.toString()+"</b></br>Mean Predictive "+target_name.toString()+"Value :<b>"+mean_value.toString()+"</b></div>";
          document.getElementById("dplot_info").innerHTML = html_content;
      }

    }


    \n

    function getdplotinfo(row_number,class_name=undefined) {
    var map_objects = ''' + str(shap_data) + ''';
    if (class_name) {
        return map_objects[class_name][row_number];
    }
    return map_objects[row_number];
    }
\n
    function loaddplotchart(dplotdata){
    var dplotChart = echarts.init(document.getElementById('dplot_plots_global_exp'));
            option = {
                     title: {
                            text: 'Decision Plot',
                            x: 'center'
                            },
                                tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                        },
                              yAxis: {
                                name: 'Feature Names',
                                type: 'category',
                                data: dplotdata['features_display']
                              },
              xAxis: {
                name: dplotdata['target_name'],
                type: 'value',
                min: dplotdata['min'],
                max: dplotdata['max'],
              },
                          series: [
                            {
                              data: dplotdata['data'],
                              type: 'line',
                              smooth: true
                            },
                             {
                              data: [
                                [dplotdata['meanValue'],dplotdata['start_y']],
                                [dplotdata['meanValue'],dplotdata['end_y']],
                              ],
                              type: 'line'
                            }
                          ]
            };
        dplotChart.setOption(option);    
    }

    '''

    return onload_html




def insert_random_dataindexes(row_count,plot_name):
    # sample_indexs = random.sample(range(0,row_count),100) if row_count > 100 else random.sample(range(0,row_count+1),row_count)
    sample_indexs = list(range(row_count))
    html_options = ""
    for id in sample_indexs:
        html_options += "<option>"+str(id)+"</option>"
    if plot_name=="lime":
        html = '''
            <label for="datarows"> Index no:</label>
            <select id="list_lime__rows" onchange="getlimerows()">'''+html_options+''''</select>   
        '''
    if plot_name=="decision_plot":
        html = '''
            <label for="datarows"> Index no:</label>
            <select id="list_dplot_row" onchange="getdplotrows()">'''+html_options+''''</select>   
        '''

    return html,sample_indexs

def insert_pdp_dropdown_list(features,target_labels,mode):
    html_options = ""
    for name in features:
        html_options += "<option>"+str(name)+"</option>"
    htmlRow = '''
        <label><b>Feature name :</b></label>
        <select id="pdp_feature_name" onchange="getpdpplots()">'''+html_options+''''</select>   
    '''
    htmlClass = None
    if not mode=="regression":
        html_class_options = ""
        for name in target_labels:
            html_class_options += f"<option>{name}</option>"
        htmlClass = '''
            <label><b>Class :</b></label>
            <select id="pdp_class_name" onchange="getpdpplots()">''' + html_class_options + ''''</select>   
        '''
    else :
        htmlClass = '''
            <label><b>Target Column: '''+target_labels[0]+'''</b></label> 
        '''


    return htmlRow,htmlClass

def get_pdp_html(pdp_data):
    model_type = "classification"
    if "regressionMode" in pdp_data:
        model_type = "regression"
        # pdp_data.remove("regressionMode")

    pdp_hashes = ""
    for entity in pdp_data:
        if "regressionMode" in entity:
            pdp_hashes += '''
                \"''' + str(entity["feature_name"]) + '''\" : 
                        {
                        'feature_data': ''' + str(entity["feature_data"]) + ''',
                        'feature_name': \"''' + str(entity["feature_name"]) + '''\",
                        'pdp_value': ''' + str(entity["pdp_values"]) + ''',
                        'regressionMode' : true
                    },
            '''
        else:
            pdp_hashes += '''
                            \"''' + str(entity["feature_name"]) + '''\" : 
                                    {
                                    'feature_data': ''' + str(entity["feature_data"]) + ''',
                                    'feature_name': \"''' + str(entity["feature_name"]) + '''\",
                                    'pdp_value': ''' + str(entity["pdp_values"]) + ''',
                                    'regressionMode': false
                                },
            '''

    pdp_hashes = '''
    {'''+str(pdp_hashes)+'''}
    '''

    onload_html  = '''
       $(window).on('load', function() {
         getpdpplots();
    });

    function getpdpplots(){
      var pdp_feature_name = $("#pdp_feature_name").val();
      var pdpcontent = getpdpinfo(pdp_feature_name);
      var regMode = pdpcontent["regressionMode"];
      plotPDP(regMode,pdpcontent);
      pdp_info(pdp_feature_name,regMode);


    }
\n
    function pdp_info(feature_name,regMode){
      
      if (regMode){
        html_content = "<div style='padding-left:40px'><b style='color:#c033c9'>Description :</b>Above plots shows the relation between average prediction values made by model Vs range of feature values of <b>"+feature_name.toString()+"</b> on keeping all other featues at constant values.</div>";
        document.getElementById("pdp_info").innerHTML = html_content;
      } else {
      html_content = "<div style='padding-left:40px'><b style='color:#c033c9'>Description :</b>Above plots shows the relation between average prediction probabilities made by model Vs range of feature values of <b>"+feature_name.toString()+"</b> on keeping all other featues at constant values.</div>";
      document.getElementById("pdp_info").innerHTML = html_content;
      }
    }

\n

    function plotPDP(regMode,pdpcontent){
            if (!regMode) {
                                var classId = $("#pdp_class_name").val();
                               var fdata = pdpcontent["feature_data"];
                               var pdata = pdpcontent["pdp_value"][classId];
                               var fname = pdpcontent["feature_name"];
                               load_pdp_echarts(fname,fdata,pdata);
            }
            if (regMode) {
                       var fdata = pdpcontent["feature_data"];
                       var pdata = pdpcontent["pdp_value"];
                       var fname = pdpcontent["feature_name"];
                       load_pdp_echarts(fname,fdata,pdata);
            }
    }

       
    \n
        
    function getpdpinfo(feature_name) {
    var map_objects = ''' + str(pdp_hashes) + ''';
    return map_objects[feature_name];
    
    }
\n

    function load_pdp_echarts(fname,fdata,pdata){
        var pdpChart = echarts.init(document.getElementById('pdp_plots_local_exp'));
            option = {
                      title: {
                        text: 'Partial dependence plot',
                        x: 'center'
                        },
                    tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                    },
              xAxis: {
                name: fname,
                type: 'category',
                data: fdata,
                nameGap: 0,
                nameTextStyle: {
                    align: 'right',
                    verticalAlign: 'top',
                    padding: [30, 0, 0, 0],
            },
              },
              yAxis: {
                name: "Partial Dependency",
                type: 'value'
              },
              series: [
                {
                  data: pdata,
                  type: 'line'
                }
              ]
            };
        pdpChart.setOption(option);    
    }
    
    '''
    return onload_html

def pdp_echarts_html(pdp_data):

    echarts = '''
        var chartDom = document.getElementById('pdp_plots');
        var myChart = echarts.init(chartDom);
        var option;
        
        option = {
          xAxis: {
            name: pdp_feature_name,
            type: 'category',
            data: '''+str(pdp_data["feature_data"])+'''
          },
          yAxis: {
            name: 'Partial Dependency',
            type: 'value'
          },
          series: [
            {
              data: [820, 932, 901, 934, 1290, 1330, 1320],
              type: 'line',
              smooth: true
            }
          ]
        };
        
        option && myChart.setOption(option);
    
        
    '''
    return echarts

def load_multi_class_names_for_roc(data):
    dataInfo = data["roc_auc"]
    classLabels = ""
    for className in dataInfo.keys():
        classLabels += f"<option>{className}</option>"

    multipleClassNames = '''
        <label for="datarowsroc">Class name:</label>
        <select id="list_class_labels_roc" onchange="getmulticlasslabelsroc()">''' + classLabels + ''''</select>   
    '''
    return multipleClassNames
def load_multi_class_names(importanceData):
    importanceData = {key:value for key,value in importanceData.items() if not key=="model_target_info"}
    multipleClassNames = None
    multipleClassNamesRoc = None
    if len(importanceData) > 1:
        classLabels = ""
        for className in importanceData.keys():
            classLabels += "<option>" + str(className) + "</option>"

        multipleClassNames = '''
            <label for="datarows">Class name:</label>
            <select id="list_class_labels" onchange="getmulticlasslabels()">'''+classLabels+''''</select>   
        '''
    return multipleClassNames

def get_html_feature_importance(importanceData):

    target_name = importanceData["model_target_info"]["target_name"]
    importanceDataModified = ""
    for className in importanceData:
        if not className == "model_target_info" :
            importanceDataModified += '''
                \"''' + str(className) + '''\" : '''+str(importanceData[className])+''',
            '''
    importanceDataModified = '''
    {'''+str(importanceDataModified)+'''}
    '''

    onload_html = '''
            $(window).on('load', function() {
            featureimp = getfeatureimportanceinfo();
            classcounts = getclassescount(featureimp);
            loadfeatureimportance(classcounts,featureimp);
        
        });
        \n
        
        function loadfeatureimportance(classcounts,featureimpinfo){
            if (classcounts==1) {
                var data = featureimpinfo["predictions"];
                const keysinfo = [];
                const valuesinfo = [];
                for (key in data){
                    keysinfo.push(key);
                    valuesinfo.push(data[key]);
                }
                loadcorehtml(keysinfo,valuesinfo,"'''+str(" Target: <b>")+str(target_name)+'''</b>");
            
            }
            if (classcounts > 1){
            loadclasswiseimportance(featureimpinfo);
            }
            
        }


        function getmulticlasslabels(){
          var featureimpinfo = getfeatureimportanceinfo();
          loadclasswiseimportance(featureimpinfo);
        }

        \n

        function loadclasswiseimportance(featureimpinfo){
        var class_name = $("#list_class_labels").val();
        var data = featureimpinfo[class_name];
        const keysinfo = [];
        const valuesinfo = [];
        for (key in data){
            keysinfo.push(key);
            valuesinfo.push(data[key]);
        }
        loadcorehtml(keysinfo,valuesinfo,"Class: <b>"+class_name+"</b>");

        }

        
        
        \n
        function getclassescount(classinfo){
        var count = 0;
            for (var i in classinfo) {
               if (classinfo.hasOwnProperty(i)) count++;
            }
        return count 
        }
        
        \n
        
        function getfeatureimportanceinfo(){
            var map_objects = '''+str(importanceDataModified)+''';
            return map_objects
        }
        \n
        function load_chart_info(keys,values,target_name_var){
          importance = values.slice(-1)[0];
          feature_name = keys.slice(-1)[0];
          html_content = "<div style='padding-top:10px'><b style='color:#c033c9'>Description :</b> Plot shows the importances of the featues by thier impact percentages on Model Prediction of "+target_name_var+"</br>Its seen that highest impact made on prediction by the feature: <b>"+feature_name+"</b> and it's Importance is:<b>"+importance.toString()+"%</b></div>";
          document.getElementById("feature_importance_info").innerHTML = html_content;
        }

        
        \n
        function loadcorehtml(keysinfo,valuesinfo,target_name_var){
                load_chart_info(keysinfo,valuesinfo,target_name_var);
                var myChart = echarts.init(document.getElementById('featureimportance_graph'));
                        option = {
                          title: {
                            text: 'Feature Importance',
                            x: 'center'
                            },
                          tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                              type: 'shadow'
                            }
                          },
                          legend: {},
                          grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                          },
                          xAxis: {
                            type: 'value',
                            boundaryGap: [0, 0.01],
                            name : 'Percentage',
                            min : '0',
                            nameGap: 0,
                            nameTextStyle: {
                                align: 'right',
                                verticalAlign: 'top',
                                padding: [30, 0, 0, 0],
                            },
                          },
                          yAxis: {
                            type: 'category',
                            data: keysinfo,
                            name : 'Features'
                          },
                          series: [
                            {
            
                              type: 'bar',
                              data: valuesinfo
                            }
                          ]
                        };
                myChart.setOption(option);  
                    
        }
    \n
    '''
    return onload_html
