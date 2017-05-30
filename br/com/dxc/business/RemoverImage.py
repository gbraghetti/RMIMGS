import docker
from br.com.dxc.teste.DockerFake import DockerFake
from br.com.dxc.teste.Teste import Teste

# import pdb; pdb.set_trace() --> modo interativo de DEBUG


# client = docker.DockerClient(base_url="tcp://192.168.99.100:2376")

'''
Imagens reais alocadas no Vagrant

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
imagesDocker = client.images.list()
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
        #listNomes.append(img.attrs["RepoTags"].__str__())
        listNomes.append(img.repotags.replace(" ", ""))
    print("*****************")

listNameFormated = []
def formatNameImg():
    nomeAdd = []
    for i in range(len(listNomes)):
        nomeSplit = listNomes[i].split(":")
        for nm in nomeSplit:
            nomeAdd.append(nm)
        if listNomes[i].count(":") > 1:
            listNameFormated.append(nomeAdd[0].replace("[u'", "")+nomeAdd[1])
        else:
            listNameFormated.append(nomeAdd[0].replace("[u'", ""))
        nomeAdd = []
    return listNameFormated



def searchName():
    listData = []
    listImgCreated = []
    print("#entrou")
    for i in range(0, len(listNameFormated)):
        listImagensDebian = teste.list(listNameFormated[i])
        #listImagensDebian = imagesDocker.list(listFormatNameImg[i])
        for img in listImagensDebian:
            #print(img)
            #listData.append(([img.attrs["Created"]], [img]))
            listData.append(([img.created], [img]))
            listImgCreated.append(img.created)
        sorted(listData, key=lambda ld: ld[0], reverse=True)
        deleteAll(listData)
        listData = []

def deleteAll(plistData):
    dock = DockerFake()
    if len(plistData) > 1:
        for i in range(1, len(plistData)):
            print(i)
            dock = plistData[0][1]
            print(dock)
            print(dock[0].short_id)
            #teste.remove(plistData[i].short)





'''def listaImagesDocker():
    for img in imagesDocker.list():
        print(img.attrs["Created"])
        '''

def listaNomes():
    for img in listNomes:
        print(img)

def listaNameFormated():
    for img in listNameFormated:
        print(img)

addInList()
formatNameImg()
searchName()


