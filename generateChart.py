def dataPreprocess(data):
    import json,numpy
    # totalData=json.loads(data)
    fields=data['search_result']['fields']
    fields.remove('_time')
    fields.remove('_span')
    datetimeValue=[]
    allInfo=[[] for i in range(len(fields))]
    from datetime import datetime
    totalData=data['search_result']['rows']
    for singleData in totalData:
        singleDatetime=datetime.fromtimestamp(singleData[0]/1000)
        datetimeValue.append(singleDatetime)
        for i in range(len(fields)):
            allInfo[i].append(float(singleData[i+1]) if singleData[i+1] else numpy.nan)#numpy.nan
        
    return {'dateTime':datetimeValue,'allInfo':allInfo,'fields':fields,'db':data['choose_db'],'y_name':data['choose_info_type'].upper()+'_util'}


def plotPicAnd2Base64(data):
    import matplotlib.pyplot as plt
    print(plt.get_backend())
    processedData=dataPreprocess(data)
    print('processedData:\n',processedData)
    allInfo=processedData['allInfo']
    print('allInfo:\n',len(allInfo[0]),allInfo[0],len(allInfo[0]),allInfo[1],sep='\n\n',end='\n\n')
    for i in range(len(allInfo)):
        plt.plot(processedData['dateTime'],allInfo[i], marker='.', linestyle = '-',label=processedData['fields'][i])

    plt.legend(loc = 'upper left')
    plt.xlabel('DateTime', color = 'black')
    plt.ylabel(processedData['y_name'], color = 'black',rotation ='vertical')
    plt.title(processedData['db'], color = 'black')
    plt.ylim(0, 100) #if processedData['y_name']=='CPU_util' else None
    # plt.show()
    import io,base64
    plotfig_stringIObytes=io.BytesIO()
    plt.savefig(plotfig_stringIObytes,format='jpg')
    plotfig_stringIObytes.seek(0)
    base64_plotFig = base64.b64encode(plotfig_stringIObytes).read()
    return base64_plotFig
