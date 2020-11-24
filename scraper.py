
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
    res = requests.get(url, headers=headers, verify=False)

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
    ls = list(map(lambda c: { 'title': c.text, 'p_date' : None, 'src' : c.attrs['href']}, ls_A))
    return ls

def gather_documents_regulations(normativa):
    url = 'https://sib.gob.do/normativas-sib/' + normativa
    soup = get_soup(url)

    THs = soup.select('th')
    for th in THs:
        if any(x in th.text for x in ['Publ', 'Emis']):
            publication_date_index = THs.index(th)

    docs = []
    TRs = soup.select('tr')

    for tr in TRs:
        TDs = tr.select('td')
        if not TDs: continue

        title = TDs[0].text.strip()
        p_date = TDs[publication_date_index].text.strip() if publication_date_index > 0 else None
        src = TDs[-1].a.attrs['href']
        docs.append({
            'title' : title,
            'p_date' : p_date,
            'src' : src
        })

    return docs

def gather_all_documents_regulations():
    regulations = (
        'leyes',
        'reglamentos',
        'cir%C2%ADcu%C2%ADlares_instructivos',
        'manuales-sib',
        'manual-de-requerimiento-de-información',
        'manual-de-supervisión-basada-en-riesgos',
        'documentos-en-consulta-pública'
    )

    ls = []

    for regulation in regulations:
        _ls = gather_documents_regulations(regulation)
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
    