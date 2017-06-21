import random

class DockerFake(object):
    repotags = None

    def __init__(self, repotags=None, short_id=None, created=None):
        self.repotags = repotags
        self.short_id = short_id
        self.created = created

    '''
        Fake para meus Dockers
        def __init__(self, repotags, created):
        self.short_id = self.getShort_id()
        self.repotags = repotags
        self.created = created
    '''

    def getShort_id(self):
        return str(random.randrange(100000, 999999))

    def setRepotags(self, repotags):
        self.repotags = repotags

    def getRepotags(self):
        return self.repotags

    def setCreated(self, created):
        self.created = created

    def getCreated(self):
        return self.create

    def __str__(self):
        return "short_id = %s /repotags = %s /created = %s" %(self.short_id, self.repotags, self.created)


import docker


class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images

    def __init__(self):
        # self.deleteNones()
        self.listImages()

    def deleteNones(self):
        for image in [images for images in self.imagesDocker.list()
                      if None or "<none>" in images.attrs["RepoTags"]]:
            print("##### REMOVENDO IMAGEM %s" %image)
            #self.imagesDocker.remove(image)  # , force=True)

    def listImages(self):
        for image in self.imagesDocker.list():
            print("Repotags %s" % image.attrs["RepoTags"])
            print("Short_id %d" % image.short_id)
        print("Numero imagens: %d" % len(self.imagesDocker.list()))


if __name__ == '__main__':
    deleteImages = DeleteImages()

