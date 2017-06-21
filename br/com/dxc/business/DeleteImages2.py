import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
imagesDocker = client.images

def teste():
    for img in imagesDocker.list():
        print(img.attrs["RepoTags"])
        print(img.attrs["RepoTags"].__str__()[::-1])
        strAttrs = img.attrs["RepoTags"].__str__()[::-1]
        print(strAttrs)
        nmRepoTagsStr = strAttrs.split(":")

        print(nmRepoTagsStr[0])
        print(nmRepoTagsStr[1][::-1])
        print(nmRepoTagsStr[1][::-1].replace("'", "").replace("[", "").replace("]", ""))

        # imagesDocker.remove("oraclelinux:7.1")

listCloneDocker = []
def organizeList():
    for img in imagesDocker.list():
        if "," in img.attrs["RepoTags"].__str__():
            auxiliar = img.attrs["RepoTags"].__str__().split(",")
            for aux in auxiliar:
                listCloneDocker.append(aux.strip())
        else:
            listCloneDocker.append(img.attrs["RepoTags"].__str__().strip())

listNomes = []
def addInList():
    for name in listCloneDocker:
        print(name)
        print(name[::-1])
        strAttrs = name[::-1]
        print(strAttrs)
        nmRepoTagsStr = strAttrs.split(":")

        print(nmRepoTagsStr[0])
        print(nmRepoTagsStr[0][::-1])
        nmRepoTagsStr = nmRepoTagsStr[1][::-1].replace("[", "").replace("]", "").replace("u'", "")
        print(nmRepoTagsStr)
        listNomes.append(nmRepoTagsStr)

def searchName():
    print("####len list nomes %s" %len(listNomes))
    listData = []
    for i in range(0, len(listNomes)):
        listImagensLinux = imagesDocker.list(listNomes[i])
        print("####list nomes[i]")
        print(listNomes[i])
        print("####list imagens linux")
        print(listImagensLinux)
        for img in listImagensLinux:
            listData.append(([img.attrs["Created"]], [img]))
        sorted(listData, key=lambda ld: ld[0], reverse=True)
        deleteAll(listData)
        listData = []

def deleteAll(plistData):
    if len(plistData) > 1:
        for i in range(1, len(plistData)):
            dock1 = plistData[0][1]
            dock0 = plistData[0][0]
            print("dock1 %s" %dock1)
            print("dock0 %s" %dock1[0].short_id)
            #self.imagesDocker.remove(dock1[0].attrs["RepoTags"].__str__().replace("[", "").replace("]", "").replace("u'", ""))#, force=True)

organizeList()
addInList();
searchName();

print(imagesDocker.list("enois"))
