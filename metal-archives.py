#!/usr/bin/env python3

import requests, re, os
from lxml import html

print('Ingrese nombre de la banda:')
bus=str(input())
pag=1
start=0

url='https://www.metal-archives.com/search/ajax-band-search/?field=name&query='+bus+'&sEcho='+str(pag)+'&iColumns=3&sColumns=&iDisplayStart='+str(start)+'&iDisplayLength=200&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2'

headers={
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.51 Safari/537.36"
        }

r=requests.get(url,headers=headers)
busqueda=r.json()
tam=int(busqueda['iTotalRecords'])
aux=0

if(tam>0):
    print('Se encontró '+str(tam)+' resultados\n')
    lista=[]
    for i in range(0,tam):
        if i%200==0 and i//200>0:
            pag+=1
            start+=200
            url='https://www.metal-archives.com/search/ajax-band-search/?field=name&query='+bus+'&sEcho='+str(pag)+'&iColumns=3&sColumns=&iDisplayStart='+str(start)+'&iDisplayLength=200&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2'
            r=requests.get(url,headers=headers)
            busqueda=r.json()
            aux=0
        link=re.findall(r'<a href="(.*)">',busqueda['aaData'][aux][0])[0]
        band=re.findall(r'">(.*)</a>',busqueda['aaData'][aux][0])[0]
        genero=busqueda['aaData'][aux][1]
        pais=busqueda['aaData'][aux][2]
        id=re.findall('^.+/(\\d*)$',link)[0]
        lista.append([band,genero,pais,link,id])
        aux+=1

    print("{:<3} {:<25} {:<40} {:<10}".format('#','Banda','Género','País'))
    for i in range(0,tam):
        print("{:<3} {:<25} {:<40} {:<10}".format(i+1,lista[i][0],lista[i][1],lista[i][2]))

    print('\nIngrese número: ')
    while(True):
        try:
            num=int(input())
            if(num>0 and num<=tam):
                break
            else:
                print('El número ingresado no existe en la lista')
                print('Ingrese número: ')
                continue
        except:
            print('Debe ingresar un número válido')
            print('Ingrese número: ')
    
    url=lista[num-1][3]
    disc_url='https://www.metal-archives.com/band/discography/id/'+str(lista[num-1][4])+'/tab/all'
    r=requests.get(url,headers=headers)
    rd=requests.get(disc_url,headers=headers)
    if r.status_code==200:
        doc=html.fromstring(r.content)
        disc_doc=html.fromstring(rd.content)
        os.system('cls||clear')
        print(doc.xpath('//h1//text()')[0]+'\n')
        print(doc.xpath("//div[@id='band_stats']/dl[1]/dt[1]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[1]//a/text()")[0])
        print(doc.xpath("//div[@id='band_stats']/dl[1]/dt[2]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[1]/dd[2]/text()")[0])
        print(doc.xpath("//div[@id='band_stats']/dl[1]/dt[3]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[1]/dd[3]/text()")[0])
        print(doc.xpath("//div[@id='band_stats']/dl[1]/dt[4]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[1]/dd[4]/text()")[0])
        print()
        print(doc.xpath("//div[@id='band_stats']/dl[2]/dt[1]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[2]/dd[1]/text()")[0])
        print(doc.xpath("//div[@id='band_stats']/dl[2]/dt[2]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[2]/dd[2]/text()")[0])
        print(doc.xpath("//div[@id='band_stats']/dl[2]/dt[3]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[2]//a/text()")[0])
        print()
        print(doc.xpath("//div[@id='band_stats']/dl[3]/dt[1]/text()")[0]+' '+doc.xpath("//div[@id='band_stats']/dl[3]/dd[1]")[0].text_content())
        print()
        print('Discografía:')
        print('---------------------------------------------------------')
        discs=disc_doc.xpath("//tbody/tr")
        aux=1
        for disc in discs:
            print(disc.xpath('(//td[1]/a/text())['+str(aux)+']')[0])
            print(disc.xpath('(//td[2]/text())['+str(aux)+']')[0])
            print(disc.xpath('(//td[3]/text())['+str(aux)+']')[0])
            if aux==len(discs):
                break
            print()
            aux+=1
        print('---------------------------------------------------------')
    else:
        print('Error al mostrar información. Por favor vuelva a intentar.')


else:
    print('No se encontró resultado')
