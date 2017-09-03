#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from database import Unidade, Curso, AreaConhecimento, Objetivo, Programa
from database import Base, engine, session

def init_browser():
	driver = "/Users/dedeco/Apps/chromedriver"
	os.environ["webdriver.chrome.driver"] = driver
	b = webdriver.Chrome(driver)	
	return b

def captura(url):

	b = init_browser()

	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	links = soup.select('a.puc-wp-encontre-seu-curso-link-curso')
	unidades = soup.select('h3.puc-wp-encontre-seu-curso-unidade')

	for i in unidades:
		u = Unidade()
		u.unidade = i.text
		session.add(u)
		session.flush()
	
	for l in links:
		
		link = l['href']

		b.get(l['href'])
		b.implicitly_wait(2)
		sp_curso = BeautifulSoup(b.page_source, 'html.parser')

		curso = sp_curso.select_one('h2.puc-pl-titulo-pg').text.strip()

		ac = sp_curso.select_one('.puc-pl-pos-graduacao-conteudo-area-conhecimento ul') 

		conhecimentos = []
		for litag in ac.find_all('li'):
			conhecimentos.append(litag.text)

		div = sp_curso.find(id="ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField")
		texto = ''

		ptags = div.find_all("p")
		for tag in ptags:
			if len(tag.text) > 20:
				texto += '\r' + tag.text

		spantags = div.find_all("span")
		for tag in spantags:
			if len(tag.text) > 20:
				texto += '\r' + tag.text

		divs = div.find_all("div")
		for tag in divs:
			if len(tag.text) > 20:
				texto += "\r" + tag.text

		m = re.search('(.*)\\s*(?=Área)', texto)
		descricao = m.group(0)

		c = Curso()
		c.nome_curso = curso
		c.descricao = descricao
		c.texto = texto
		c.link = link
		c.unidade_id = 1

		session.add(c)
		session.flush()

		ultags = div.find_all("ul")

		obj = []
		for litag in ultags[0].find_all('li'):
			obj.append(litag.text)

		for i in obj:
			o = Objetivo()
			o.objetivo = i
			o.curso_id = c.id
			session.add(o)

		programa = []
		try:
			for litag in ultags[1].find_all('li'):
				programa.append(litag.text)
		except IndexError:
			pass

		for i in programa:
			p = Programa()
			p.programa = i
			p.curso_id = c.id
			session.add(p)

		session.commit()

	b.quit()

if __name__ == "__main__":
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
	url = "http://www.pucminas.br/Pos-Graduacao/IEC/modalidades/latusensu/Paginas/Especializa%C3%A7%C3%A3o%20e%20Master.aspx"
	captura(url)

