import docker

class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images
    listNomes = []
    listNameFormated = []

    def __init__(self):
        #pass
        self.deleteNones()
        self.addInList()
        self.formatNameImg()
        self.searchName()

    def deleteNones(self):
        print("###### DELETAR NONES #########")
        for image in [images for images in self.imagesDocker.list()
                      if "<none>" in images.attrs["RepoTags"]]:
            print("Repotags: %s + Short_id %s" % (image.attrs["RepoTags"], image.short_id))
            print("###### REMOVENDO NONE ######")
            self.imagesDocker.remove(image, force=True)

    def addInList(self):
        nmRepoTags = []
        for img in self.imagesDocker.list():
            print("Repotags: %s + Short_id %s + Created %d" %(img.attrs["RepoTags"], img.short_id, img.attrs["Created"]))
            if "," in img.attrs["RepoTags"].__str__():
                nmRepoTagsStr = img.attrs["RepoTags"].__str__().split(",")
                for img in nmRepoTagsStr:
                    nmRepoTags.append(img)
                self.listNomes.append(nmRepoTags[0])
                self.listNomes.append(nmRepoTags[1])
            else:
                self.listNomes.append(img.attrs["RepoTags"].__str__())
        print("*****************")


    def formatNameImg(self):
        nomeAdd = []
        for i in range(len(self.listNomes)):
            print(self.listNomes[i])
            nomeSplit = self.listNomes[i].split(":")
            for nm in nomeSplit:
                nomeAdd.append(nm)
            if self.listNomes[i].count(":") > 1:
                self.listNameFormated.append(nomeAdd[0].replace("[u'", "")+nomeAdd[1])
            else:
                self.listNameFormated.append(nomeAdd[0].replace("[u'", "").replace(" u'", ""))
            nomeAdd = []
        return self.listNameFormated

    def searchName(self):
        listData = []
        for i in range(0, len(self.listNameFormated)):
            listImagensDebian = self.imagesDocker.list(self.listNameFormated[i])
            print("listaNameFormated %s" %self.listNameFormated[i])
            print("listImagensDebian %s" %listImagensDebian)
            print("Length listImagensDebian %d" %len(listImagensDebian))
            for img in listImagensDebian:
                listData.append(([img.attrs["Created"]], [img]))
            sorted(listData, key=lambda ld: ld[0], reverse=True)
            self.deleteAll(listData)
            listData = []

    def deleteAll(self, plistData):
        #print("plistData %s" %plistData)
        #print("Length plistData %d" %len(plistData))
        if len(plistData) > 1:
            for i in range(1, len(plistData)):
                dock1 = plistData[0][1]
                dock0 = plistData[0][0]
                print("dock1 %s" %dock1)
                print("dock0 %s" %dock1[0].short_id)
                self.imagesDocker.remove(dock1[0].short_id, force=True)


if __name__ == '__main__':
    deleteImages = DeleteImages()

    for img in deleteImages.imagesDocker.list():
        pass
        #print(img.attrs)
    #deleteImages.addInList()
    #deleteImages.formatNameImg()
    #print(deleteImages.listNameFormated)
    #print(deleteImages.listNomes)