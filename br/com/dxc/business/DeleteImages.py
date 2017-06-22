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

    def deleteNones(self):
        print("###### DELETAR NONES #########")
        for image in [images for images in self.imagesDocker.list()
                      if "u'<none>:<none>'" == images.attrs["RepoTags"].__str__()]:
            print("Repotags: %s + Short_id %s" % (image.attrs["RepoTags"], image.short_id))
            print("###### REMOVENDO NONE ######")
            #self.imagesDocker.remove(image, force=True)

    def listParaTeste(self):
        listTeste = []
        noneStr = "u'<none>:<none>'"

        for images in self.imagesDocker.list():
            if images.attrs["RepoTags"] is not None or noneStr not in images.attrs["RepoTags"].__str__().strip():
                print("####images.attr[RepoTags]: %s" % images.attrs["RepoTags"])
                listTeste.append(images)

        return listTeste


    def organizeList(self):
        noneStr = "u'<none>:<none>'"
        for img in [images for images in self.imagesDocker.list()
                    if images.attrs["RepoTags"] is not None or noneStr not in images.attrs["RepoTags"].__str__().strip()]:
            #print("####noneStr: %s" %noneStr)
            print("####RepoTags: %s" %img.attrs["RepoTags"].__str__())
        # for img in self.listParaTeste():
            if "," in img.attrs["RepoTags"].__str__():
                auxiliar = img.attrs["RepoTags"].__str__().split(",")
                for aux in auxiliar:
                    self.listCloneDocker.append(aux.strip())
            else:
                self.listCloneDocker.append(img.attrs["RepoTags"].__str__().strip())
        print(self.listCloneDocker)

    def addInList(self):
        for name in self.listCloneDocker:
            print(name)
            if name.count(":") > 1:
                tagPosition = name.rfind(":")
            else:
                tagPosition = name.find(":")
            print("####tagPosition %s" %tagPosition)
            tagStr = name[tagPosition::]
            nmRepoTagsChange = name.replace(tagStr, "")
            print(nmRepoTagsChange)
            nmRepoTagsChange = nmRepoTagsChange.replace("[", "").replace("]", "").replace("u'", "")
            print(nmRepoTagsChange)
            self.listNomes.append(nmRepoTagsChange)
        print("*****************")

    def searchAndRemoveName(self):
        print("####len list nomes %s" % len(self.listNomes))
        listData = []
        for i in range(0, len(self.listNomes)):
            listImagensLinux = self.imagesDocker.list(self.listNomes[i])
            print("####list nomes[i]")
            print(self.listNomes[i])
            print("####list imagens linux")
            print(listImagensLinux)
            for img in listImagensLinux:
                listData.append(([img.attrs["Created"]], [img]))
            sorted(listData, key=lambda ld: ld[0], reverse=True)
            self.deleteAll(listData)
            listData = []

    def deleteAll(plistData):
        if len(plistData) > 1:
            for i in range(1, len(plistData)):
                dock1 = plistData[0][1]
                dock0 = plistData[0][0]
                print("dock1 %s" % dock1)
                print("dock0 %s" % dock1[0].short_id)
                # self.imagesDocker.remove(dock1[0].attrs["RepoTags"].__str__().replace("[", "").replace("]", "").replace("u'", ""))#, force=True)


if __name__ == '__main__':
    deleteImages = DeleteImages()
