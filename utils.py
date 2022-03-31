import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import pycountry_convert as pc
from datetime import datetime


# tracxn raw data 파싱할때 na 값 때문에 반복문이 깨지는 것을 방지함
def prevent_break(row,key):
    try: 
        o = row[key]
        code = 0
    except: 
        o = '-'
        code = 1
    return o,code

def json_to_excel(data):
    df = pd.DataFrame()
    for n,row in enumerate(data['result']):
        com_name, com_name_err = prevent_break(row,'name')
        com_domain, com_domain_err = prevent_break(row,'domain')

        com_location, com_location_err = prevent_break(row,'location')
        com_location_country, com_location_country_err = prevent_break(com_location,'country')
        com_location_continent, com_location_continent_err = prevent_break(com_location,'continent')

        com_totalMoneyRaised, com_totalMoneyRaised_err = prevent_break(row,'totalMoneyRaised')
        if com_totalMoneyRaised_err == 0 :
            com_totalMoneyRaised = com_totalMoneyRaised['totalAmount']['amount']

        com_businessModel, com_businessModel_err = prevent_break(row,'businessModelList')
        if com_businessModel_err == 0:
            com_businessModel = list(set([_ for sublist in com_businessModel for _ in sublist['fullPathString'].split('>') if '-' not in _]))    

        com_practiceAreaList, com_practiceAreaList_err = prevent_break(row,'practiceAreaList')
        if com_practiceAreaList_err == 0:
            com_practiceAreaList = [_['name'] for _ in com_practiceAreaList]

        com_companyFeed = list(set(com_businessModel+com_practiceAreaList))
        com_companyFeed = '\n'.join(com_companyFeed)

        com_stage, com_stage_err = prevent_break(row,'stage')
        
        com_fundingDate,com_fundingDate_err = prevent_break(row,'fundingInfo') 
        com_fundingDate,com_fundingDate_err = prevent_break(com_fundingDate,'latestRoundInfo')
        com_fundingDate,com_fundingDate_err = prevent_break(com_fundingDate,'date') 

        if com_fundingDate_err == 0:
            com_fundingDate_Year = com_fundingDate['year']
            com_fundingDate_Month = com_fundingDate['month']
        else:
            com_fundingDate_Year = '-'
            com_fundingDate_Month = '-'

        com_description, com_description_err = prevent_break(row,'description')
        com_longDescription, com_longDescription_err = prevent_break(com_description,'long')
        com_shortDescription, com_shortDescription_err = prevent_break(com_description,'short')

        com_investorList, com_investorList_err = prevent_break(row,'investorList')
        if com_investorList_err == 0:
            com_investorList = [_['domain'] for _ in com_investorList if _['type']=='COMPANY']
        com_investorList = '\n'.join(com_investorList)

        com_tracxnScore, com_tracxnScore_err = prevent_break(row,'tracxnScore')
        com_tracxnTeamScore, com_tracxnTeamScore_err = prevent_break(row,'tracxnTeamScore')

        row_df = pd.DataFrame({'com_name':com_name,
                               'com_domain':com_domain,
                               'com_stage':com_stage,
                               'com_fundingDate_Year':com_fundingDate_Year,
                               'com_fundingDate_Month':com_fundingDate_Month,
                               'com_location_continent':com_location_continent,
                               'com_location_country':com_location_country,
                               'com_longDescription':com_longDescription,
                               'com_shortDescription':com_shortDescription,
                               'com_totalMoneyRaised':com_totalMoneyRaised,
                               'com_companyFeed':com_companyFeed,
                               'com_investorList':com_investorList,
                               'com_tracxnScore':com_tracxnScore,
                               'com_tracxnTeamScore':com_tracxnTeamScore}, index=[n])
        df = pd.concat([df,row_df])
        
    df = df[df['com_stage']!='Series B']    
    return df.astype(str)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data


deduplicate_tracxn_to_lv2 = pd.read_excel('asset/Feed_Deduplicate_Tracxn_To_FeedLV2.xlsx')
deduplicate_lv2_to_lv1 = pd.read_excel('asset/Feed_Deduplicate_FeedLV2_To_FeedLV1.xlsx')

def deduplicate_data(data):
    df = pd.DataFrame()
    for row in data.iterrows():
        n = row[0]
        row = row[1]
        com_companyFeed = row['com_companyFeed'].split('\n')
        com_companyFeedLV2 = []
        for feed in com_companyFeed:
            if feed in deduplicate_tracxn_to_lv2['Feed'].values:
                FeedLV2 = deduplicate_tracxn_to_lv2[deduplicate_tracxn_to_lv2['Feed']==feed][['Label #0','Label #1','Label #2', 'Label #3']].values[0].tolist()
                com_companyFeedLV2.extend(FeedLV2)

        com_companyFeedLV2 = list(set([_ for _ in com_companyFeedLV2 if type(_) != float]))[:20]
        com_companyFeedLV2 += ['-' for _ in range(20-len(com_companyFeedLV2))]
        com_companyFeedLV2_df = pd.DataFrame(com_companyFeedLV2).T
        com_companyFeedLV2_df.columns = [f'companyFeedLV2 #{_}' for _ in range(20)]


        com_companyFeedLV1 = []
        for feedLV2 in com_companyFeedLV2:
            if feedLV2 in deduplicate_lv2_to_lv1['Deduplicated Feeds (LV2)'].values:
                FeedLV1 = deduplicate_lv2_to_lv1[deduplicate_lv2_to_lv1['Deduplicated Feeds (LV2)'] == feedLV2]['Deduplicated Feeds (LV1)'].values.tolist()            
                com_companyFeedLV1.extend(FeedLV1)

        com_companyFeedLV1 = list(set([_ for _ in com_companyFeedLV1 if type(_) != float]))[:10]
        com_companyFeedLV1 += ['-' for _ in range(10-len(com_companyFeedLV1))]
        com_companyFeedLV1_df = pd.DataFrame(com_companyFeedLV1).T
        com_companyFeedLV1_df.columns = [f'companyFeedLV1 #{_}' for _ in range(10)]

        com_companyFeed = pd.concat([com_companyFeedLV1_df,com_companyFeedLV2_df],axis=1)    

        row = pd.DataFrame(row).T
        col = row.columns.tolist() + com_companyFeed.columns.tolist()
        a = row.values.tolist() 
        b = com_companyFeed.values.tolist()
        val = a[0] + b[0]
        row_df = pd.DataFrame(val).T
        row_df.columns = col

        df = pd.concat([df,row_df])
    return df.astype(str)

def tracxn_export_to_fdi(df):
    continents = {'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'}
    tot = pd.DataFrame()
    for row in df.iterrows():
        n, row = row
        com_name = row['Company Name']
        com_domain = row['Domain Name']
        com_stage = row['Round Name']

        com_location_country = row['Location'].split(',')[-1].strip()
        country_code = pc.country_name_to_country_alpha2(com_location_country, cn_name_format="default")
        com_location_continent = continents[pc.country_alpha2_to_continent_code(country_code)]

        com_longDescription = row['Overview']
        com_shortDescription = '-'

        com_totalMoneyRaised = row['Total Funding (USD)']

        com_companyFeed = row['Business Models']
        if type(com_companyFeed) != float:
            com_companyFeed = [feed.strip() for feed in com_companyFeed.replace('\n','>').split('>') if '-' not in feed]    
            com_companyFeed = list(set(com_companyFeed))
            com_companyFeed = '\n'.join(com_companyFeed)
        else:
            com_companyFeed = '-'

        com_investorList = row['Institutional Investors']

        com_tracxnScore = '-'
        com_tracxnTeamScore = '-'

        row_dict = {'com_name':com_name,
                   'com_domain':com_domain,
                   'com_stage':com_stage,
                   'com_location_continent':com_location_continent,
                   'com_location_country':com_location_country,
                   'com_longDescription':com_longDescription,
                   'com_shortDescription':com_shortDescription,
                   'com_totalMoneyRaised':com_totalMoneyRaised,
                   'com_companyFeed':com_companyFeed,
                   'com_investorList':com_investorList,
                   'com_tracxnScore':com_tracxnScore,
                   'com_tracxnTeamScore':com_tracxnTeamScore}

        row_df = pd.DataFrame(row_dict.values()).T
        row_df.columns = row_dict.keys()
        tot = pd.concat([tot,row_df])
    return tot.astype(str)

def calculate_feed_score(df, score, top_n, feedLV):
    output = {}

    feed_col = [_ for _ in df.columns if _.startswith(f'{feedLV}')]
    for row in df.iterrows():
        n,row = row
        investors = row['com_investorList'].split('\n')
        feeds = [_ for _ in row[feed_col] if _ != '-']

        occ_weight = 0
        investor_weight = 0

        if row['com_totalMoneyRaised'] != '-':
            funded_weight = int(row['com_totalMoneyRaised'])
        else:
            funded_weight = 0


        for i in investors:
            if i in score[:top_n]['Investor Domain'].values:
                occ_weight +=1 
                investor_weight += score[score['Investor Domain'] == i]['Investor Score'].values[0]

        for feed in feeds:
            if output.get(feed) is None:
                output[feed] = [occ_weight,investor_weight,funded_weight]
            else:
                output[feed][0] += occ_weight
                output[feed][1] += investor_weight
                output[feed][2] += funded_weight

    output_df = pd.DataFrame({f'{feedLV}':output.keys(),
                               'feedScore'            : [b for a,b,c in output.values()],
                               'fundedAmount'         : [c for a,b,c in output.values()],
                               'occurence'            : [a for a,b,c in output.values()],})
    
    output_df['occurenceRatio_by_feedNum'] = (output_df['occurence']/output_df['occurence'].sum()*100)
    output_df['occurenceRatio_by_comNum'] = (output_df['occurence']/len(df)*100)
    output_df['feedScore'] = (output_df['feedScore']/output_df['occurence'])
    output_df['fdiRank'] = output_df['occurenceRatio_by_feedNum'].rank(ascending=False, method = 'max').astype(int)
    
    output_df = output_df.sort_values(by=['fdiRank'])
    output_df = output_df[['fdiRank',f'{feedLV}','feedScore','fundedAmount','occurence','occurenceRatio_by_comNum','occurenceRatio_by_feedNum']]
    return output_df

def filter_feed_score_by_time(df,lower_bound,upper_bound):
    date = [datetime(y,m,1) for y,m in zip(df['com_fundingDate_Year'].values,df['com_fundingDate_Month'].values)]
    df['com_fundingDate'] = pd.to_datetime(date)
    filtered_df = df[df["com_fundingDate"].isin(pd.date_range(lower_bound, upper_bound))]  
    return filtered_df

def calculate_coOccur(df, cooccur_with, feedLV):
    feedCol = [_ for _ in df.columns if _.startswith(feedLV)]
    output = {}
    tot_num = 0
    for row in df.iterrows():
        n,row = row
        feeds = [_ for _ in row[feedCol].values if _ != '-']
        feedBool = all(feed in feeds  for feed in cooccur_with)
        mon = row['com_totalMoneyRaised']
        
        if mon != '-': mon = int(mon)
        else: mon = 0
        
        if feedBool:
            for f in feeds:
                if output.get(f) is None:
                    output[f] = [1,mon]
                else:
                    output[f][0] += 1
                    output[f][1] += mon
                    
            tot_num += 1

    for _ in cooccur_with:
         del output[_]
    
    output_df = pd.DataFrame({feedLV:output.keys(),
                             'occurence'      :[a for a,b in output.values()],
                             'fundedAmount'   :[b for a,b in output.values()]})
    output_df = output_df.sort_values(by=['occurence'],ascending=False)
    return output_df, tot_num