from django.http import HttpResponse
from django.shortcuts import render
import sys
sys.path.append('..')
from indexrequest.query import Query

query = Query('../indexrequest/index')

def search_form(request):
    return render(request, 'main.html')

def search(request):
    res = None
    if 'q' in request.GET and request.GET['q']:
        res = query.standard_search(request.GET['q'])
        context = {
            'query': request.GET['q'],
            'resCount': len(res),
            'results': res
        }
        return render(request, 'result.html', context)
    else:
        return render(request, 'main.html')


def extract(request, q):
    if q and len(query.standard_search(q)) > 0:
        res = query.regex_extract(q)
        adjs, poss, ages, times = list(), list(), list(), list()
        wdN = 0
        for r in res:
            for ir in r['adjs']:
                adjs.append(ir)
            for ir in r['poss']:
                poss.append(ir[0])
            for ir in r['ages']:
                ages.append(ir)
            for ir in r['times']:
                times.append(ir)
            wdN += r['wdN']
        if len(adjs) > 10:
            adjs = adjs[:10]
        if len(poss) > 10:
            poss = poss[:10]
        if len(ages) > 10:
            ages = ages[:10]
        if len(times) > 10:
            times = times[:10]
        context = {
            'query': q,
            'adjs': adjs,
            'poss': poss,
            'ages': ages,
            'times': times,
            'wdN': wdN
        }
        return render(request, 'extract.html', context)
    else:
        return render(request, 'result.html')