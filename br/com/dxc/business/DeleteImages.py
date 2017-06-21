import docker

class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images
    listNomes = []
    listCloneDocker = []

    def __init__(self):
        pass
        #self.deleteNones()
        #self.addInList()
        #self.formatNameImg()
        #self.searchName()

    def deleteNones(self):
        print("###### DELETAR NONES #########")
        for image in [images for images in self.imagesDocker.list()
                      if "u'<none>:<none>'" == images.attrs["RepoTags"].__str__()]:
            print("Repotags: %s + Short_id %s" % (image.attrs["RepoTags"], image.short_id))
            print("###### REMOVENDO NONE ######")
            #self.imagesDocker.remove(image, force=True)

    def organizeList(self):
        for img in self.imagesDocker.list():
            if "," in img.attrs["RepoTags"].__str__():
                auxiliar = img.attrs["RepoTags"].__str__().split(",")
                for aux in auxiliar:
                    self.listCloneDocker.append(aux.strip())
            else:
                self.listCloneDocker.append(img.attrs["RepoTags"].__str__().strip())

    def addInList(self):
        for name in self.listCloneDocker:
            print(name)
            print(name[::-1])
            strAttrs = name[::-1]
            print(strAttrs)
            nmRepoTagsStr = strAttrs.split(":")

            print(nmRepoTagsStr[0])
            print(nmRepoTagsStr[0][::-1])
            nmRepoTagsStr = nmRepoTagsStr[1][::-1].replace("[", "").replace("]", "").replace("u'", "")
            print(nmRepoTagsStr)
            self.listNomes.append(nmRepoTagsStr)
        print("*****************")

    def searchName(self):
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

    for img in deleteImages.imagesDocker.list():
        print(img.attrs)
