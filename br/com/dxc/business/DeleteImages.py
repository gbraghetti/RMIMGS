###########
#Os comentarios estao sem acento, por causa do encoding que estava dando problema na hora do desenvolvimento.
###########

import docker

class DeleteImages(object):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    imagesDocker = client.images
    listNomes = []
    listCloneDocker = []

    def __init__(self):
        self.deleteNameAndTagIsNone()
        self.deleteTagIsNone()
        self.addInList()
        self.searchAndRemoveName()

    def deleteNameAndTagIsNone(self):
        '''
            O metodo deleteNameAndTagIsNone, tem a funcao de deletar as imagens que contem o nome e a tag como none (<none>:<none>).
            Ele verifica nas images em questao quais sao aqueles que contem u'<none>:<none> como nome e apos isso tenta deleta-las.
            Foi visto que o motivo pelo qual ela nao consegue deleta-la e "conflict: unable to delete cf9295ace4da (must be forced) - image is referenced in multiple repositories"
                na qual precisa ser forcada com "force=True" no momento da exclusao.
        '''
        noneStr = u'<none>:<none>'
        for image in [images for images in self.imagesDocker.list()
                      if (noneStr in images.attrs["RepoTags"])]:
            try:
                print("TENTANDO REMOVER")
                self.imagesDocker.remove(image.attrs["Id"])  # , force=True)
                print("REMOVIDO %s" %image.attrs["RepoTags"])
            except Exception as e:
                print("FALHOU REMOVER, MOTIVO: %s" %e)
                continue


    def deleteTagIsNone(self):
        '''
            O metodo deleteNameAndTagIsNone, tem a funcao de deletar as images que estao como None em suas tags, o que acaba causando um None em seu atributo RepoTags.
            Foi visto que o motivo pelo qual ela não consegue deleta-la é "conflict: unable to delete cf9295ace4da (must be forced) - image is referenced in multiple repositories"
                nao qual precisa ser forcada com "force=True" no momento da exclusao.
        '''
        for image in [images for images in self.imagesDocker.list()
                      if (images.attrs["RepoTags"] is None)]:
            try:
                print("TENTANDO REMOVER")
                self.imagesDocker.remove(image.attrs["Id"])  # , force=True)
                print("REMOVIDO %s" %image.attrs["RepoTags"])
            except Exception as e:
                print("FALHOU REMOVER, MOTIVO: %s" %e)

    def validarBuscaPorNome(self, list):
        '''
            O metodo validarBuscaPorNome, tem a funcao de receber uma lista q foi gerada pela listagem por nomes e ira verificar se existe alguma situacao None nas imagens.
            Caso tenha, ira remove-las e retornar uma lista com apenas nomes validos.

        :param list: lista com todas as imagens para aquele nome

        :return: a lista organizada
        '''
        listOrganizada = []
        noneStr = u'<none>:<none>'
        for images in list:
            if (images.attrs["RepoTags"] is not None and noneStr not in images.attrs["RepoTags"]):
                listOrganizada.append(images)
        return listOrganizada

    def organizeList(self):
        '''
            O metodo organizeList, tem a funcao de verificar se eixste alguma situacao None nas imagens e por nome de imagem, verificar se a imagem possui mais de uma imagem
                em seu RepoTags.
            Caso tenha, ira fazer um loop dentro dessas imagens e adicionar em uma lista clone das imagens dockers em questao.
        '''
        noneStr = u'<none>:<none>'
        for img in [images for images in self.imagesDocker.list()
                    if (images.attrs["RepoTags"] is not None and noneStr not in images.attrs["RepoTags"])]:
            if(len(img.attrs["RepoTags"]) > 1):
                for aux in img.attrs["RepoTags"]:
                    self.listCloneDocker.append(str(aux.strip()))
            else:
                self.listCloneDocker.append(str(img.attrs["RepoTags"]).strip())

    def addInList(self):
        '''
            O metodo addInList, tem a funcao de separar as tags dos nomes das imagens.
            Apos chamar o organizeList, ele ir contar se no nome da imagem tenha mais de uma ocorrencia de dois pontos (:), caso tenha
                ira chamar o metodo rfind para uma string e procurar a ultima posicao dos dois pontos e adicionar a variavel tagPosition.
            Caso tenha apenas um dois pontos (:), ira procurar a primeira ocorrencia dele e adicionar a variavel tagPosition.
            Apos isso a variavel tagStr ira receber a posicao dos dois pontos e retornar a tag do nome da imagem.
            Apos isso a variavel nmRepoTagsChange ira substituir a tag no nome da imagem por vazio "".
            E se precisar dar um replace nos caracteres necessarios.
                e adicionar a uma lista de nomes formatados para o passo seguinte.
        '''

        self.organizeList()
        for name in self.listCloneDocker:
            if name.count(":") > 1:
                tagPosition = name.rfind(":")
            else:
                tagPosition = name.find(":")
            tagStr = name[tagPosition::]
            nmRepoTagsChange = name.replace(tagStr, "")
            nmRepoTagsChange = nmRepoTagsChange.replace("[", "").replace("]", "").replace("u'", "")
            self.listNomes.append(nmRepoTagsChange)

    def searchAndRemoveName(self):
        '''
            O metodo searchAndRemoveName, tem a funcao de buscar por nome na lista de imagens no jenkins e retornar uma lista com as imagens referentes à aqueles nomes.
            E para cada imagem, será adicionada numa lista de arrays o atributo Created, referente a data da criação da imagem e a imagem em sim.
            Apos ter adicionado todos as imagens nessa lista de arrays, isso sera feito uma ordenacao reversa pelo atributo Created, para que deixe o maior atributor Created
                como primeiro da lista.
            Apos isso ira chamar o metodo deleteAll, passando essa lista e depois limpando a lista de arrays.

        '''
        listData = []
        for i in range(0, len(self.listNomes)):
            listImagensLinux = self.imagesDocker.list(self.listNomes[i])
            listImagensLinux = (self.validarBuscaPorNome(listImagensLinux))
            for img in listImagensLinux:
                listData.append(([img.attrs["Created"]], [img]))
            sorted(listData, key=lambda ld: ld[0], reverse=True)
            self.deleteAll(listData)
            listData = []

    def deleteAll(self, plistData):
        '''
            O metodo deleteAll, tem a funcao de deletar todas as imagens mais antigas do jenkins por cada nome.
            Se o tamanho da lista for maior que 1, ele continuará o fluxo para remover todas as imagens, menos a primeira,
                pois a primeira é a imagem mais atual existente no jenkins.
            Caso o fluxo continue, sera pega a imagem dentro da lista atrelada ao atributo created, transformar o nome dela em string (garantir que seja uma string)
                e removê-lo por nome.
            Caso ocorra algum erro, será exibida a mensagem e o fluxo continuará.

        :param plistData: lista ordenada reversa
        '''
        if (len(plistData) > 1):
            for i in range(1, len(plistData)):
                dock1 = plistData[i][1]
                strRepoTags = str(dock1[0].attrs["RepoTags"]).replace("[", "").replace("]", "").replace("u'", "").replace("'", "")
                try:
                    print("TENTANDO REMOVER")
                    self.imagesDocker.remove(strRepoTags)#, force=True)
                    print("REMOVIDO %s" %str(dock1[0].attrs["RepoTags"]))
                except Exception as e:
                    print("FALHOU REMOVER, MOTIVO: %s" % e)
                    continue



if __name__ == '__main__':
    deleteImages = DeleteImages()
