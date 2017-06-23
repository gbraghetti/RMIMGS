import docker

class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images
    listNomes = []
    listCloneDocker = []

    def __init__(self):
        #pass
        #self.deleteNones()
        self.organizeList()
        self.addInList()
        self.searchAndRemoveName()
        #self.listParaTeste()

    def deleteNones(self):
        print("####deleteNones")
        noneStr = u'<none>:<none>'
        print("###### DELETAR NONES #########")
        for image in [images for images in self.imagesDocker.list()
                      if (images.attrs["RepoTags"] is None and noneStr in images.attrs["RepoTags"])]:
            print("Repotags: %s + Short_id %s" % (image.attrs["RepoTags"], image.short_id))
            print("###### REMOVENDO NONE ######")
            #self.imagesDocker.remove(image, force=True)

    def listParaTeste(self):
        print("####listParaTeste")
        listTeste = []
        noneStr = u'<none>:<none>'
        for images in self.imagesDocker.list():
            if (images.attrs["RepoTags"] is not None and noneStr not in images.attrs["RepoTags"]):
                print("####images.attr[RepoTags]: %s" % images.attrs["RepoTags"])
                print("####images.attr[RepoTags]: %s %s" % (images.attrs["RepoTags"], len(images.attrs["RepoTags"])))
                listTeste.append(images)
        print("####tamanho lista teste: %d" % len(listTeste))
        print("####tamanho images docker: %d" % len(self.imagesDocker.list()))
        return listTeste

    def validarBuscaPorNome(self, list):
        print("####validarBuscaPorNome")
        print("####len list %d" %len(list))
        listOrganizada = []
        noneStr = u'<none>:<none>'
        for images in list:
            if (images.attrs["RepoTags"] is not None and noneStr not in images.attrs["RepoTags"]):
                listOrganizada.append(images)
        print("####len list organizada %d" % len(listOrganizada))
        return listOrganizada

    def organizeList(self):
        print("####organizeList")
        noneStr = u'<none>:<none>'
        for img in [images for images in self.imagesDocker.list()
                    if (images.attrs["RepoTags"] is not None and noneStr not in images.attrs["RepoTags"])]:
            #print("####RepoTags: %s" %str(img.attrs["RepoTags"]))
        # for img in self.listParaTeste():
            if(len(img.attrs["RepoTags"]) > 1):
                #print("####MAIOR %d %s" %(len(img.attrs["RepoTags"]), img.attrs["RepoTags"]))
            #if "," in str(img.attrs["RepoTags"]):
                #auxiliar = str(img.attrs["RepoTags"]).split(",")
                for aux in img.attrs["RepoTags"]:
                    self.listCloneDocker.append(str(aux.strip()))
            else:
                self.listCloneDocker.append(str(img.attrs["RepoTags"]).strip())
        #print(self.listCloneDocker)
        print(len(self.listCloneDocker))

    def addInList(self):
        print("####addInList")
        for name in self.listCloneDocker:
            #print(name)
            if name.count(":") > 1:
                tagPosition = name.rfind(":")
            else:
                tagPosition = name.find(":")
            #print("####tagPosition %s" %tagPosition)
            tagStr = name[tagPosition::]
            nmRepoTagsChange = name.replace(tagStr, "")
            #print(nmRepoTagsChange)
            nmRepoTagsChange = nmRepoTagsChange.replace("[", "").replace("]", "").replace("u'", "")
            #print(nmRepoTagsChange)
            self.listNomes.append(nmRepoTagsChange)
        print(self.listNomes)
        print("*****************")

    def searchAndRemoveName(self):
        print("####searchAndRemoveName")
        print("####len list nomes %s" % len(self.listNomes))
        listData = []
        for i in range(0, len(self.listNomes)):
            #print("####list nomes[i]#### NAO ERA PRA ESTAR VAZIO!!!")
            #print(self.listNomes[i])
            listImagensLinux = self.imagesDocker.list(self.listNomes[i])
            listImagensLinux = (self.validarBuscaPorNome(listImagensLinux))
            #print("####list imagens linux")
            #print(listImagensLinux)
            for img in listImagensLinux:
                #COMENTARIO
                listData.append(([img.attrs["Created"]], [img.attrs["RepoTags"]]))
            sorted(listData, key=lambda ld: ld[0], reverse=True)
            self.deleteAll(listData)
            listData = []

    def deleteAll(self, plistData):
        print("####deleteAll")
        #print("Created %s" %plistData[0])
        #print("Created [0]")
        #print(plistData[0][0])
        print("####plistData")
        print(plistData)
        print("####len %d" %len(plistData))
        if (len(plistData) > 1):
            for i in range(1, len(plistData)):
                print("####list plistData %d" % i)
                dock1 = plistData[i][1]
                print[dock1]
                str(dock1)
                print(dock1.replace("[", "").replace("]", "").replace("u'", ""))
                #self.imagesDocker.remove(str(dock1.attrs["RepoTags"].replace("[", "").replace("]", "").replace("u'", "")))#, force=True)


if __name__ == '__main__':
    deleteImages = DeleteImages()

'''
----------------------------COMENTARIO----------------------------
listData.append(([img.attrs["Created"]], [img])) ESTAVA ASSIM
listData.append(([img.attrs["Created"]], [img.attrs["RepoTags"]])) FICOU ASSIM
foi feito isso para facilitar a exclusao na linha 
self.imagesDocker.remove(str(dock1.replace("[", "").replace("]", "").replace("u'", ""))
pensar na solucao para poder usar o atributo attrs["RepoTags"] da imagem.

'''