#!/usr/bin/env python3

import requests, re, os
from lxml import html

print('Ingrese nombre de la banda:')
bus=str(input())

url='https://www.metal-archives.com/search/ajax-band-search/?field=name&query='+bus+'&sEcho=1&iColumns=3&sColumns=&iDisplayStart=0&iDisplayLength=20'

headers={
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.51 Safari/537.36"
        }

r=requests.get(url,headers=headers)
busqueda=r.json()

if(len(busqueda['aaData'])>0):
    print('Se encontró '+str(len(busqueda['aaData']))+' resultados\n')
    lista=[]
    for i in range(0,len(busqueda['aaData'])):
        link=re.findall(r'<a href="(.*)">',busqueda['aaData'][i][0])[0]
        band=re.findall(r'">(.*)</a>',busqueda['aaData'][i][0])[0]
        genero=busqueda['aaData'][i][1]
        pais=busqueda['aaData'][i][2]
        lista.append([band,genero,pais,link])

    print("{:<3} {:<25} {:<40} {:<10}".format('#','Banda','Género','País'))
    for i in range(0,len(lista)):
        print("{:<3} {:<25} {:<40} {:<10}".format(i+1,lista[i][0],lista[i][1],lista[i][2]))

    print('\nIngrese número: ')
    while(True):
        try:
            num=int(input())
            if(num>0 and num<=len(lista)):
                break
            else:
                print('El número ingresado no existe en la lista')
                print('Ingrese número: ')
                continue
        except:
            print('Debe ingresar un número válido')
            print('Ingrese número: ')
    
    url=lista[num-1][3]
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        doc=html.fromstring(r.content)
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

    else:
        print('Error al mostrar información. Por favor vuelva a intentar.')


else:
    print('No se encontró resultado')
