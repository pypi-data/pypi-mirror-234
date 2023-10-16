from cast_common.highlight import Highlight
from cast_common.util import format_table
from pandas import DataFrame,concat
from pandas import pivot_table,ExcelWriter,json_normalize
from os.path import abspath



hl = Highlight(hl_user='n.kaplan+WellsFargo@castsoftware.com',
               hl_pswd='mdSi20ty@02',
               hl_instance=1271,
               hl_base_url='https://rpa.casthighlight.com/')

hl._get_third_party_data(max_rows=40)
oss = DataFrame()
for row in Highlight._third_party:
    data = Highlight._third_party[row]
    if data != '':
        try:
            for d in data:
                if 'cve' not in d.keys():
                    d['cve'] = []

            df = json_normalize(data,record_path=['cve',['vulnerabilities']],meta=['componentId','name','version','release', 'languages','lifeSpan', 'origin','licenses', 'lastVersion', 'lastRelease','cve'],record_prefix='_',errors='ignore')
            df['application']=row
            oss = concat([oss,df])
        except KeyError as ke:
            hl.log.warning(f'{row} {ke}')
        except Exception as ex:
            hl.log.warning(f'{row} {ex}')

oss = oss.drop(columns=['cve'])


file_name = abspath(f'E:/work/Decks/Wells Fargo/test.xlsx')

writer = ExcelWriter(file_name, engine='xlsxwriter')
format_table(writer,oss,'summary')
writer.close()


pass