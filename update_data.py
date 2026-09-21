import json,os,requests
URL='https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil'
PATH='data/history.json'
HEAD={'User-Agent':'Mozilla/5.0 (compatible; Lotofacil-Omega/1.0)','Accept':'application/json','Referer':'https://loterias.caixa.gov.br/'}
def main():
    with open(PATH,encoding='utf8') as f: hist=json.load(f)
    last=hist[-1]['concurso'] if hist else 0
    r=requests.get(URL,headers=HEAD,timeout=30);r.raise_for_status();latest=r.json();target=int(latest['numero'])
    for n in range(last+1,target+1):
        rr=requests.get(f'{URL}/{n}',headers=HEAD,timeout=30);rr.raise_for_status();p=rr.json(); nums=sorted(int(x) for x in p['listaDezenas'])
        if len(nums)==15: hist.append({'concurso':int(p['numero']),'data':p['dataApuracao'],'dezenas':nums})
    hist={x['concurso']:x for x in hist};hist=sorted(hist.values(),key=lambda x:x['concurso'])
    with open(PATH,'w',encoding='utf8') as f:json.dump(hist,f,ensure_ascii=False,separators=(',',':'))
    print(f'Atualizado até concurso {hist[-1]["concurso"]}; total {len(hist)}')
if __name__=='__main__':main()
