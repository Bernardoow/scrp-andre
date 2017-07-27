import requests
from bs4 import BeautifulSoup



class Materia(object):
    descricao = None
    area_de_conhecimento = None
    duracao = None

    def create_sql(self):
        return "insert into table values ('{}','{}','{}')".format(self.descricao.replace('\n', '').replace('\r','').strip(), self.area_de_conhecimento.strip(), self.duracao.strip())


r = requests.get('http://www.pucminas.br/Pos-Graduacao/IEC/modalidades/latusensu/Paginas/Especializa%C3%A7%C3%A3o%20e%20Master.aspx')


soup = BeautifulSoup(r.text, 'html.parser')


#Obter links para a materia
links = soup.select('a.puc-wp-encontre-seu-curso-link-curso')

for link in links:
    materia = Materia()
    request_para_pagina_curso = requests.get(link['href'])

    soup_curso = BeautifulSoup(request_para_pagina_curso.text, 'html.parser')
    materia.descricao = soup_curso.select_one('.puc-wp-curso-outras-unidades').text
    materia.area_de_conhecimento = soup_curso.select_one('.puc-pl-pos-graduacao-conteudo').text
    materia.duracao = soup_curso.select_one('#ctl00_PlaceHolderMain_ctl11__ControlWrapper_RichHtmlField').text

    print(materia.create_sql())
