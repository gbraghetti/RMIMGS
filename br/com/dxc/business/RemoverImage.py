import docker
#from br.com.dxc.teste.DockerFake import DockerFake
from br.com.dxc.teste.Teste import Teste

# import pdb; pdb.set_trace() --> modo interativo de DEBUG


# client = docker.DockerClient(base_url="tcp://192.168.99.100:2376")

'''
Imagens reais alocadas no Vagrant

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
imagesDocker = client.images
'''

teste = Teste()

def deleteNones():
    print("###### deletar nones #########")
    for image in teste.list():
    #for image in imagesDocker.list():
        if '<none>:<none>' in image.attrs["RepoTags"]:
            #DockerFake.remove(image.short_id, force=True)
            Teste.remove(image.short_id, force=True)
            print(image.attrs["RepoTags"])


listNomes = []
def addInList():
    for img in teste.list():
    #for img in imagesDocker.list():
        listNomes.append(img.attrs["RepoTags"].__str__())
    print("*****************")

listNameFormated = []
def formatNameImg():
    nomeAdd = []
    for i in range(len(listNomes)):
        nomeSplit = listNomes[i].split(":")
        for nm in nomeSplit:
            nomeAdd.append(nm)
            listNameFormated.append(nomeAdd[0].replace("[u'", ""))
            break
        nomeAdd = []
    return listNameFormated


listData = []
def searchName(listFormatNameImg):
    for i in range(len(listFormatNameImg)):
        listImagensDebian = teste.list(listFormatNameImg[i])
        #listImagensDebian = imagesDocker.list(listFormatNameImg[i])
        for img in listImagensDebian:
            print("######## IMAGENS")
            print(img)
            listData.append(([img.attrs["Created"]], [img]))
        listData.sort(reverse=True)
        #print("Permanecera: ")
        #print(listData[0])
        #deleteAll(listData)

def deleteAll(plistData):
    if len(plistData) > 1:
        for i in range(1, len(plistData)):
            print("Removendo %d %s" % (i, plistData[i]))


########
#addInList()
#print(listNomes)
#print(formatNameImg())
#searchName(formatNameImg())
#print(imagesDocker.list("amov/nginx"))
#print("######## ALL")

'''def listaImagesDocker():
    for img in imagesDocker.list():
        print(img.attrs["Created"])
        '''


