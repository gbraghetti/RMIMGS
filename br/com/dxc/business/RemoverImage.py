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

def deleteNones2():
    print("###### DELETAR NONES #########")
    for image in teste.list():

    #for image in imagesDocker.list():
        print("Repotags: %s + Short_id %s" %(image.repotags, image.short_id))
        #teste.remove("46807d3de55c")
        if ("<none>:<none>".replace(" ","") == image.repotags.replace(" ", "")):
            print(image.repotags.replace(" ", ""))
        #if '<none>:<none>' in image.attrs["RepoTags"]:
            #DockerFake.remove(image.short_id, force=True)
            print("###### REMOVENDO NONE ######")
            teste.remove(image.short_id)
            #print(image.attrs["RepoTags"])



def deleteNones():
    print("###### DELETAR NONES #########")
    for image in [images for images in teste.list()
                  if "<none>".replace(" ", "") in images.repotags.replace(" ", "")]:
        print("Repotags: %s + Short_id %s" % (image.repotags, image.short_id))
        print(image.repotags.replace(" ", ""))
        print("###### REMOVENDO NONE ######")
        teste.listaDockerImgs.remove(image)
    print(len(teste.listaDockerImgs))

listNomes = []
def addInList():
    for img in teste.list():
    #for img in imagesDocker.list():
        #listNomes.append(img.attrs["RepoTags"].__str__())
        listNomes.append(img.repotags.replace(" ", ""))
    print("*****************")
    print("listnomes %d" %len(listNomes))

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
    print("listnameformated %d" % len(listNameFormated))
    return listNameFormated



def searchName():
    listData = []
    for i in range(0, len(listNameFormated)):
        listImagensDebian = teste.list(listNameFormated[i])
        for img in listImagensDebian:
            listData.append(([img.created], [img]))
        sorted(listData, key=lambda ld: ld[0], reverse=True)
        deleteAll(listData)
        listData = []

def deleteAll(plistData):
    dock = DockerFake()
    if len(plistData) > 1:
        for i in range(1, len(plistData)):
            dock = plistData[0][1]
            teste.remove(dock[0].short_id)



def listaNomes():
    for img in listNomes:
        print(img)

def listaNameFormated():
    for img in listNameFormated:
        print(img)

print("###### LISTA INICIAL #######")
print("")
teste.consultarLista()
print("")
print("###### FIM LISTA INICIAL ######")
deleteNones()
addInList()
formatNameImg()
searchName()


print("###### LISTA FINAL #######")
print("")
teste.consultarLista()
print("")
print("###### FIM LISTA FINAL ######")

