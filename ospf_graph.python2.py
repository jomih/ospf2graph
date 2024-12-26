#!/usr/bin/python
# -*- coding: utf-8 -*-

from graphviz import Source
import sys, getopt


#############################################################################################################
#Script en Python para mostrar un grafico a partir de la base de datos de OSPF
#
#Para ejecutarlo, hay que invocar el script con -f <fichero_base_datos>
#
#El fichero de base de datos debe contener el resultado del comando "show ospf database extensive" de un ACX
#Si se mete la base de datos de OSPF de un PE que participa en varias areas, el resultado es inesperado
#
#Por ahora solo muestra los routers como nodos, y las adyacencias como edge. 
#
#Para futuras versiones:
# - Mostrar metric de los enlaces
# - Traducir IP a nombre
# - Soportar una base de datos con varias areas
#
#############################################################################################################


###############
#
# Functions
#
###############


def getNodeID(id_to_search):
	#pattern = ''.join([id_to_search,'$'])
	pattern = id_to_search
	#print 'buscara', pattern
	for router in routerList:
		if (router.endswith(pattern)):
		#if (router.find(pattern) !=-1):
			#print '  id_to_search encontrado'
			def_varTmp1 = router.split(' ')
			return(def_varTmp1[0].strip())
	return ('null')


###############
#
# Main Function
#
###############

try:
    opts, args = getopt.getopt(sys.argv[1:],"f:m:h")
except getopt.GetoptError:
	sys.exit(2)

checkIP = 0

if (len(sys.argv) < 2):
	print (' Error en los argumentos')
	print (' python ./xxxxx.py -f <fichero_ospf_database>\n')
	print (' El fichero debe contener el resultado de "show ospf database extensive" de un ACX\n')
	sys.exit(2)


for opt, arg in opts:
	if opt in ("-h"): #ayuda
		print ("El script se puede ejecutar con dos parametros:")
		print ("  -f: (obligatorio) indica el fichero de base de datos de OSPF (resultado de \"show ospf database extensive\" en el ACX)")
		print ("  -m: (opcional) IP del ACX que se quiere marcar en el dibujo")
		sys.exit()
	elif opt in ("-f"): #fichero ospf database
		ficheroOspfDb = arg.strip()
	elif opt in ("-m"): #IP de router a marcar en el dibujo
		markedIP = arg.strip()
		checkIP = 1
	else:
		print ("Error")
		sys.exit()

nodeID = 0
graphDb = []
routerList = []

try:
	ospfDatabase = open (ficheroOspfDb, 'r')
except:
	print (' Error en los argumentos')
	print (' Se debe especificar con -f el fichero con la base de datos de Ospf\n')
	sys.exit(2)

graphDb.append('digraph G{')

#caracteristicas globales del dibujo 
graphDb.append('graph [concentrate=true]')

#caracteristicas de las lineas (edge)
graphDb.append('edge [dir=none]')
graphDb.append('edge [color=red]')
graphDb.append('node [shape=box]')

#Posicion de PE1 y PE2 en el dibujo
graphDb.append('{rank=source; 0;}') #PE1
graphDb.append('{rank=sink; 1;}') #PE2


#Primera iteracion: extrae todos los nodos y les asigna un ID
for line in ospfDatabase:
	if (line.startswith('Area ')):
		varTmp1 = line.split()
		areaID = varTmp1[1].strip()

#		text = ''.join(['node [shape=ellipse]'])
#		graphDb.append(text)

		text = ''.join(['Area [label="Area ',str(areaID),'",fillcolor=orange, style=filled, shape=ellipse, width=1, height=1]'])
		#text = ''.join(['Area [label="Area ',str(areaID),'",fillcolor=orange, style=filled, shape=ellipse]'])
		graphDb.append(text)
		continue

	if (line.startswith('Router')):
		varTmp1 = line.split()
		routerID = varTmp1[1].strip()

		if (checkIP):
			if (routerID.endswith(markedIP)):
				text = ''.join([str(nodeID), ' [label="',str(routerID.replace('*','')),'",fillcolor=red, style=filled]'])
				graphDb.append(text)

				text = ''.join([str(nodeID), ' ',routerID])
				routerList.append(text)
				nodeID = nodeID + 1
				continue

		if (routerID.startswith('10.34.')):
			text = ''.join([str(nodeID), ' [label="',str(routerID.replace('*','')),'",fillcolor=grey, style=filled]'])
			graphDb.append(text)
		else:
			text = ''.join([str(nodeID), ' [label="',str(routerID.replace('*','')),'"]'])
			graphDb.append(text)

		text = ''.join([str(nodeID), ' ',routerID])
		routerList.append(text)
		nodeID = nodeID + 1

		continue


currentNodeID = 0

ospfDatabase.close()
ospfDatabase = open (ficheroOspfDb, 'r')

#segunda iteracion: construye las adyacencias (edge)

for line in ospfDatabase:
	if (line.startswith('Router')):
		varTmp1 = line.split()
		routerID = varTmp1[1].strip()

		currentNodeID = getNodeID(routerID)

		continue

	if (line.startswith('  Topology default')):
		#print 'entra en topology'
		while(1):
			line = ospfDatabase.next()
			if (line.startswith('    Type: PointToPoint')):
				varTmp2 = line.split()
				neighborID = varTmp2[4].strip()
				nodeID = getNodeID(neighborID)
				#print 'nodeID es', nodeID
				
				text = ''.join([str(currentNodeID), ' -> ', nodeID])
				graphDb.append(text)
				continue
			if (line.startswith('  Aging timer')):
				break

graphDb.append('}')

#print 'graphDb vale:\n'
temp = '\n'.join(graphDb)
#print temp

s = Source(temp, filename="ospf_graph.gv", format="png")
s.view()