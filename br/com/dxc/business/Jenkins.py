#!/bin/bash

./ usr / bin / virtualenvwrapper.sh
export
http_proxy = proxy.houston.hpecorp.net:8080
export
https_proxy = proxy.houston.hpecorp.net:8080
virtualenv =$(workon | grep
delete_nones)
if ["$virtualenv" == ""]; then
mkvirtualenv
delete_nones
fi

pip
install - -upgrade
pip
pip
install
docker

touch
programa.py

deleteNones =
'class DeleteImages(object):' +
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

echo $deleteNones > programa.py

python
programa.py
