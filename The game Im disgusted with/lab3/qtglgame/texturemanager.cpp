#include "texturemanager.h"

std::map<std::string, QOpenGLTexture*> TextureManager::m_textures;

TextureManager::TextureManager()
{

}

void TextureManager::init() {
    m_textures["brick"]=new QOpenGLTexture(QImage("resources/brick.jpg"));
    m_textures["grass"]=new QOpenGLTexture(QImage("resources/grass.jpg"));
    m_textures["wood"]=new QOpenGLTexture(QImage("resources/wood.jpg"));
    m_textures["spinning_cross"]=new QOpenGLTexture(QImage("resources/boomerang-cross.png"));
    m_textures["skydome"] = new QOpenGLTexture(QImage("resources/skydome.png"));
    m_textures["defeat"]=new QOpenGLTexture(QImage("resources/defeat.jpg"));
    m_textures["victory"]=new QOpenGLTexture(QImage("resources/victory.jpg"));
    m_textures["boar_skin"]=new QOpenGLTexture(QImage("resources/boar_skin.jpg"));
}

QOpenGLTexture* TextureManager::getTexture(std::string name) {
    return m_textures[name];
}
