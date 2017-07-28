import requests
from bs4 import BeautifulSoup
from database import Curso, Unidade
from database import session

r = requests.get('http://www.pucminas.br/Pos-Graduacao/IEC/modalidades/latusensu/Paginas/Especializa%C3%A7%C3%A3o%20e%20Master.aspx')

soup = BeautifulSoup(r.text, 'html.parser')

'''
unidades = soup.select('h3.puc-wp-encontre-seu-curso-unidade')

for i in unidades:
    u = Unidade()
    u.unidade = i.text
    session.add(u)

session.commit()
'''

cursos = soup.select('a.puc-wp-encontre-seu-curso-link-curso')

for c in cursos:
    print (c.text)

    request_curso = requests.get(c['href'])

    sc = BeautifulSoup(request_curso.text, 'html.parser')



    div = sc.find(id="ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField")
    p = div.select('p')[0].text

    print (p)

    '''
    div = sc.find('div', {'class': 'puc-pl-pos-graduacao-conteudo-area-conhecimento'})
    children = div.findChildren()
    for child in children:
        print (child)
    '''



'''
links = 

for link in links:
    materia = Materia()
    request_para_pagina_curso = requests.get(link['href'])

    
    materia.descricao = soup_curso.select_one('.puc-wp-curso-outras-unidades').text
    materia.area_de_conhecimento = soup_curso.select_one('.puc-pl-pos-graduacao-conteudo').text
    materia.duracao = soup_curso.select_one('#ctl00_PlaceHolderMain_ctl11__ControlWrapper_RichHtmlField').text
'''