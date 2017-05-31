import docker

class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images
    listNomes = []
    listNameFormated = []

    def __init__(self):
        self.deleteNones()
        self.addInList()
        self.formatNameImg()
        self.searchName()

    def deleteNones(self):
        print("###### DELETAR NONES #########")
        for image in [images for images in self.imagesDocker.list()
                      if "<none>:<none>" == images.attrs["RepoTags"]]:
            print("Repotags: %s + Short_id %s" % (image.attrs["RepoTags"], image.short_id))
            print("###### REMOVENDO NONE ######")
            self.imagesDocker.remove(image, force=True)

    def addInList(self):
        for img in self.imagesDocker.list():
            print("Repotags: %s + Short_id %s + Created %d" %(img.attrs["RepoTags"], img.short_id, img.attrs["Created"]))
            self.listNomes.append(img.attrs["RepoTags"].__str__())
        print("*****************")


    def formatNameImg(self):
        nomeAdd = []
        for i in range(len(self.listNomes)):
            nomeSplit = self.listNomes[i].split(":")
            for nm in nomeSplit:
                nomeAdd.append(nm)
            if self.listNomes[i].count(":") > 1:
                self.listNameFormated.append(nomeAdd[0].replace("[u'", "")+nomeAdd[1])
            else:
                self.listNameFormated.append(nomeAdd[0].replace("[u'", ""))
            nomeAdd = []
        return self.listNameFormated

    def searchName(self):
        listData = []
        for i in range(0, len(self.listNameFormated)):
            listImagensDebian = self.imagesDocker.list(self.listNameFormated[i])
            for img in listImagensDebian:
                listData.append(([img.attrs["Created"]], [img]))
            sorted(listData, key=lambda ld: ld[0], reverse=True)
            self.deleteAll(listData)
            listData = []

    def deleteAll(self, plistData):
        if len(plistData) > 1:
            for i in range(1, len(plistData)):
                dock1 = plistData[0][1]
                dock0 = plistData[0][0]
                print(dock1)
                print(dock1[0].short_id)
                #self.imagesDocker.remove(dock1[0].short_id, force=True)


if __name__ == '__main__':
    deleteImages = DeleteImages()
    #print(deleteImages.listNameFormated)
    #print(deleteImages.listNomes)