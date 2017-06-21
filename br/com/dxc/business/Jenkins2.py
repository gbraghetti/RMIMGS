import docker

class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images


def __init__(self):
    self.deleteNones()


def deleteNones(self):
    for image in [images for images in self.imagesDocker.list()
                  if "<none>" in images.attrs["RepoTags"]]:
        self.imagesDocker.remove(image, force=True)

if __name__ == '__main__':
    deleteImages = DeleteImages()
