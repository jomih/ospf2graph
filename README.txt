#############################################################################################################
#
#Script en Python para mostrar un grafico a partir de la base de datos de OSPF
#
#Para ejecutarlo, hay que invocar el script con -f <fichero_base_datos>
#Se puede marcar la IP de un ACX para que salga coloreado en rojo en el dibujo. Para ello, -m <IP>
#
#Ejemplo:
#  python ./ospf_graph.py -f ospf_database.txt -m 100.127.61.46
#  python ./ospf_graph.py -f ospf_database.txt 
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

Dependencias para instalar graphviz (aunque deberia estar ya cargado gracias a pipenv):
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null ; brew install caskroom/cask/brew-cask 2> /dev/null
brew reinstall graphviz
pip install graphviz
