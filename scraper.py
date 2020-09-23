
import requests
import bs4
import time


def get_soup(url):
    ''' Get soup from url '''

    # fake headers to cheat the page xd
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    # perform request
    res = requests.get(url, headers=headers)

    # let's continue if the request was accepted
    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        return soup

def gather_documents_1():
    url = 'https://sib.gob.do/centro-de-documentos?tid_1=5&keys='
    soup = get_soup(url)

    # get all <a> tags
    ls_A = soup.select(".region-content a")
    # convert all elements into a dict
    ls = list(map(lambda c: { 'title': c.text, 'src' : c.attrs['href']}, ls_A))
    return ls

def gather_documents_regulations(normativa, link_index):
    url = 'https://sib.gob.do/normativas-sib/' + normativa
    soup = get_soup(url)

    docs = []
    TRs = soup.select('tr')

    for tr in TRs:
        TDs = tr.select('td')
        if not TDs: continue

        title = TDs[0].text.strip()
        src = TDs[link_index].a.attrs['href']
        docs.append({
            'title' : title,
            'src' : src
        })

    return docs

def gather_all_documents_regulations():
    regulations = (
        ('leyes', 4),
        ('reglamentos', 5),
        ('cir%C2%ADcu%C2%ADlares_instructivos', 5),
        ('manuales-sib', 4),
        ('manual-de-requerimiento-de-información', 4),
        ('manual-de-supervisión-basada-en-riesgos', 4),
        ('documentos-en-consulta-pública', 5),
    )

    ls = []

    for regulation in regulations:
        _ls = gather_documents_regulations(*regulation)
        ls.extend(_ls)
        # avoid ddos xd
        time.sleep(1)

    return ls

def gather_all_documents():
    ls = []

    _ls = gather_all_documents_regulations()
    ls.extend(_ls)
    
    _ls = gather_documents_1()
    ls.extend(_ls)

    return ls
    