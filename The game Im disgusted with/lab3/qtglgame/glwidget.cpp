#include "glwidget.h"
#include <QMouseEvent>
#include <QOpenGLShaderProgram>
#include <QCoreApplication>
#include <math.h>
#include <iostream>
#include <qstack.h>
#include <QPainter>
#include "cube.h"
#include "bullet.h"
#include "texturemanager.h"
#include "enemy.h"
using namespace std;

GLWidget::GLWidget(QWidget *parent)
    : QOpenGLWidget(parent),
      m_program(nullptr)
{
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
    QCursor c = cursor();
    c.setShape(Qt::CursorShape::BlankCursor);
    setCursor(c);
}

GLWidget::~GLWidget()
{
    /*for(auto it = m_meshes.begin() ; it != m_meshes.end(); it++)
        delete it.value();*/

    cleanup();
}

QSize GLWidget::sizeHint() const
{
    return QSize(1000, 800);
}

void GLWidget::cleanup()
{
    if (m_program == nullptr)
        return;
    makeCurrent();

    delete m_program;
    m_program = nullptr;
    doneCurrent();
}

void GLWidget::addObject(GameObject* obj) {
    obj->init();
    m_gameObjects.push_back(obj);
}



void GLWidget::loadHeightMap(QString filepath, QVector3D center, QVector3D size, QVector2D maxUV, QOpenGLTexture* texture)
{
    QImage img;
    img.load(filepath);

    float boxSizeX = size.x()/img.width();
    float boxSizeZ = size.z()/img.height();

    float offsetX = -boxSizeX * img.width()/2 + center.x();
    float offsetZ = -boxSizeZ * img.height()/2;

    float minY = center.y() - size.y() / 2;
    float maxY = center.y() + size.y() / 2;

    int groupSize = (img.width() - 1) * (img.height() - 1) * 2;

//    for(int i = 0 ; i < img.height() - 1 ; i++)
//    {
//        for(int j = 0 ; j < img.width() - 1 ; j++)
//        {
//            float X1 = offsetX + boxSizeX * i;
//            float X2 = offsetX + boxSizeX * (i+1);
//            float Z1 = offsetZ + boxSizeZ * j;
//            float Z2 = offsetZ + boxSizeZ * (j+1);

//            float Y00 = QColor(img.pixel(j, i)).red() / 255.0f * (maxY - minY) + minY;
//            float Y01 = QColor(img.pixel(j+1, i)).red() / 255.0f * (maxY - minY) + minY;
//            float Y10 = QColor(img.pixel(j, i+1)).red() / 255.0f * (maxY - minY) + minY;
//            float Y11 = QColor(img.pixel(j+1, i+1)).red() / 255.0f * (maxY - minY) + minY;

//            QVector2D texCoord00(maxUV.x() * i / img.width(), maxUV.y() * j / img.height());
//            QVector2D texCoord01(maxUV.x() * (i+1) / img.width(), maxUV.y() * j / img.height());
//            QVector2D texCoord10(maxUV.x() * i / img.width(), maxUV.y() * (j+1) / img.height());
//            QVector2D texCoord11(maxUV.x() * (i+1) / img.width(), maxUV.y() * (j+1) / img.height());

//            addTriangleCollider(QVector3D(X1, Y00, Z1), QVector3D(X1, Y01, Z2), QVector3D(X2, Y11, Z2), groupSize,
//                                texCoord00, texCoord10, texCoord11, texture);

//            addTriangleCollider(QVector3D(X2, Y11, Z2), QVector3D(X2, Y10, Z1), QVector3D(X1, Y00, Z1), groupSize,
//                                texCoord11, texCoord01, texCoord00, texture);
//        }
//    }
}



void GLWidget::initCollisionTriangles() {
   /* addTriangleCollider(
                QVector3D(25,0,-25),
                QVector3D(-25,0,-25),
                QVector3D(25,0,25),
                1,
                QVector2D(1,1),
                QVector2D(0,1),
                QVector2D(1,0),
                TextureManager::getTexture("grass")
                );
    addTriangleCollider(
                QVector3D(-25,0,-25),
                QVector3D(-25,0,25),
                QVector3D(25,0,25),
                1,
                QVector2D(0,1),
                QVector2D(0,0),
                QVector2D(1,0),
                TextureManager::getTexture("grass")
                );*/

//    loadHeightMap("resources/heightmap.png", QVector3D(0.0f,-5.0f,0.0f), QVector3D(200.0f, 20.0f,200.0f),
//                  QVector2D(10,10), TextureManager::getTexture("grass"));
    collisionTrianglesMesh.m_primitive=GL_TRIANGLES;
    collisionTrianglesMesh.initVboAndVao();
    //scena:
    /*addTriangleCollider(QVector3D(30, 0, -30), QVector3D(-30, 0, -30), QVector3D(30, 0, 30), 1, QVector2D(1, 1), QVector2D(0, 1), QVector2D(1, 0), TextureManager::getTexture("grass"));
    addTriangleCollider(QVector3D(-30, 0, -30), QVector3D(-30, 0, 30), QVector3D(30, 0, 30), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("grass"));

    addTriangleCollider(QVector3D(-15, 0, 15), QVector3D(-15, 15, 15), QVector3D(15, 15, 15), 1, QVector2D(1, 0), QVector2D(1, 1), QVector2D(0, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(15, 15, 15), QVector3D(15, 0, 15), QVector3D(-15, 0, 15), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-15, 15, 15), QVector3D(-15, 0, 15), QVector3D(-15, 15, 20), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-15, 0, 15), QVector3D(-15, 0, 20), QVector3D(-15, 15, 20), 1, QVector2D(0, 0), QVector2D(1, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-35, 0, 20), QVector3D(-35, 15, 20), QVector3D(-15, 15, 20), 1, QVector2D(1, 0), QVector2D(1, 1), QVector2D(0, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-15, 15, 20), QVector3D(-15, 0, 20), QVector3D(-35, 0, 20), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-35, 15, 20), QVector3D(-35, 0, 20), QVector3D(-35, 15, -30), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-35, 0, 20), QVector3D(-35, 0, -30), QVector3D(-35, 15, -30), 1, QVector2D(0, 0), QVector2D(1, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(25, 0, -30), QVector3D(25, 15, -30), QVector3D(-35, 15, -30), 1, QVector2D(1, 0), QVector2D(1, 1), QVector2D(0, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(-35, 15, -30), QVector3D(-35, 0, -30), QVector3D(25, 0, -30), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(25, 15, -30), QVector3D(25, 0, -30), QVector3D(25, 15, 25), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(25, 0, -30), QVector3D(25, 0, 25), QVector3D(25, 15, 25), 1, QVector2D(0, 0), QVector2D(1, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(25, 15, 25), QVector3D(25, 0, 25), QVector3D(15, 15, 15), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));
    addTriangleCollider(QVector3D(25, 0, 25), QVector3D(15, 0, 15), QVector3D(15, 15, 15), 1, QVector2D(0, 0), QVector2D(1, 0), QVector2D(1, 1), TextureManager::getTexture("brick"));

    addTriangleCollider(QVector3D(5, 3, -21), QVector3D(-5, 3, -21), QVector3D(5, 3, -13), 1, QVector2D(1, 1), QVector2D(0, 1), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-5, 3, -21), QVector3D(-5, 3, -13), QVector3D(5, 3, -13), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-5, 3, -21), QVector3D(-10, 0, -21), QVector3D(-5, 3, -13), 1, QVector2D(1, 1), QVector2D(0, 1), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-10, 0, -21), QVector3D(-10, 0, -13), QVector3D(-5, 3, -13), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(10, 0, -21), QVector3D(5, 3, -21), QVector3D(10, 0, -13), 1, QVector2D(1, 1), QVector2D(0, 1), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(5, 3, -21), QVector3D(5, 3, -13), QVector3D(10, 0, -13), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(5, 3, -13), QVector3D(-5, 3, -13), QVector3D(5, 0, -13), 1, QVector2D(1, 1), QVector2D(0, 1), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-5, 3, -13), QVector3D(-5, 0, -13), QVector3D(5, 0, -13), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-5, 3, -13), QVector3D(-10, 0, -13), QVector3D(-5, 0, -13), 1, QVector2D(1, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(5, 3, -13), QVector3D(5, 0, -13), QVector3D(10, 0, -13), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-5, 3, -21), QVector3D(5, 3, -21), QVector3D(-5, 0, -21), 1, QVector2D(1, 1), QVector2D(0, 1), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(5, 3, -21), QVector3D(5, 0, -21), QVector3D(-5, 0, -21), 1, QVector2D(0, 1), QVector2D(0, 0), QVector2D(1, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(-5, 3, -21), QVector3D(-5, 0, -21), QVector3D(-10, 0, -21), 1, QVector2D(1, 1), QVector2D(1, 0), QVector2D(0, 0), TextureManager::getTexture("wood"));
    addTriangleCollider(QVector3D(5, 3, -21), QVector3D(10, 0, -21), QVector3D(5, 0, -21), 1, QVector2D(0, 1), QVector2D(1, 0), QVector2D(0, 0), TextureManager::getTexture("wood"));*/
}

void GLWidget::addTriangleCollider(QVector3D v1, QVector3D v2, QVector3D v3, int groupSize,
                                   QVector2D uv1, QVector2D uv2, QVector2D uv3, QOpenGLTexture *texture) {
        Triangle t;
        t.v1=v1;
        t.v2=v2;
        t.v3=v3;
        t.texture=texture;
        t.groupSize=groupSize;
        t.n=QVector3D::crossProduct(v1-v3,v2-v1).normalized();
        t.A=t.n.x();
        t.B=t.n.y();
        t.C=t.n.z();
        t.D=-(t.A*v1.x() + t.B * v1.y() + t.C*v1.z());
        collisionTriangles.push_back(t);
        collisionTrianglesMesh.add(t.v1, t.n, uv1);
        collisionTrianglesMesh.add(t.v2, t.n, uv2);
        collisionTrianglesMesh.add(t.v3, t.n, uv3);
}

void GLWidget::setRectangle(float xPos, float yPos, float width, float height, QVector3D color, QOpenGLTexture *texture) {
    m_program_HUD->setUniformValue(m_rectangleLoc_HUD.xPos, xPos);
    m_program_HUD->setUniformValue(m_rectangleLoc_HUD.yPos, yPos);
    m_program_HUD->setUniformValue(m_rectangleLoc_HUD.width, width);
    m_program_HUD->setUniformValue(m_rectangleLoc_HUD.height, height);
    m_program_HUD->setUniformValue(m_color_HUD, color);

    if (texture!=nullptr) {
        m_program_HUD->setUniformValue(m_hasTexture_HUD, 1);
        texture->bind();
    } else {
        m_program_HUD->setUniformValue(m_hasTexture_HUD, 0);
    }
}

void GLWidget::paintHUD() {
    CMesh* rectMesh=CMesh::m_meshes["rect"];
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC0_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    m_program_HUD->bind();
    m_program_HUD->setUniformValue(m_resolutionLoc_HUD, m_resolution);

    //Elementy HUDu
//    setRectangle(20,680,100,100,QVector3D(1,1,0), TextureManager::getTexture("spinning_cross"));
//    rectMesh->render(this);

    if (m_player.hp<=0) {
        setRectangle(m_resolution.x()/4,m_resolution.y()/4,500,100,QVector3D(1,1,0), TextureManager::getTexture("defeat"));
        rectMesh->render(this);
    }

    if (licznik==liczba_spawnow) {
        m_player.speed=0;
        setRectangle(m_resolution.x()/4,m_resolution.y()/4,500,100,QVector3D(1,1,0), TextureManager::getTexture("victory"));
        rectMesh->render(this);
    }

    //HealthBar
    float playerHP=m_player.hp;
    float playerHPmax=100;
    float posX=20;
    float posY=20;
    float width=250;
    float height=20;
    float frame=5;

    setRectangle(posX,posY,width*playerHP/playerHPmax,height,QVector3D(0,1,0),nullptr);
    rectMesh->render(this);
    setRectangle(posX+width*playerHP/playerHPmax,posY,width*(1-playerHP/playerHPmax),height,QVector3D(0,0,0),nullptr);
    rectMesh->render(this);
    setRectangle(posX-frame,posY-frame,width+frame*2,height+frame*2, QVector3D(0, 0.5, 0), nullptr);
    rectMesh->render(this);

    char str[80];
    sprintf(str, "%d", licznik);

    QPainter painter(this);
    painter.setPen(QColor(255.0f, 255.0f, 255.0f, 255.0f));
    painter.setFont(QFont("Helvetica", 26));
    painter.drawText(100, 100, str);
    painter.end();

    QPainter crosshair(this);
    crosshair.setPen(QColor(255.0f, 255.0f, 255.0f, 255.0f));
    crosshair.setFont(QFont("Helvetica", 11));
    crosshair.drawText((m_resolution.x()/2)-8,m_resolution.y()/2, "+");
    crosshair.end();


    if (playerHP<=0) {
        m_player.speed=0;
    }

    glDisable(GL_BLEND);
    m_program_HUD->release();
}

void GLWidget::loadTriangleCollidersFromFile(QString filepath, QOpenGLTexture *texture) {
    QFile file(filepath);
        file.open(QFile::OpenMode::enum_type::ReadOnly);

        std::cout << "Loading " << filepath.toStdString() << " as mesh - " << (file.isOpen() ? "Found!" : "Not Found!") << std::endl;

        QVector<QVector3D> loaded_vertices;
        QVector<QVector3D> loaded_normals;
        QVector<QVector2D> loaded_texCoords;

        QVector<QVector3D> v;
        QVector<QVector3D> n;
        QVector<QVector2D> uv;
        int facesCount = 0;


        bool hasNormals = false;
        bool hasTexCoords = false;

        QTextStream stream(&file);

        while (!stream.atEnd()) {
            QString line = stream.readLine();
            line = line.simplified();

            if (line.length() > 0 && line.at(0) != QChar::fromLatin1('#')) {
                QTextStream lineStream(&line, QIODevice::ReadOnly);
                QString token;
                lineStream >> token;

                if (token == QStringLiteral("v")) {
                    float x, y, z;
                    lineStream >> x >> y >> z;
                    loaded_vertices.append(QVector3D( x, y, z ));
                } else if (token == QStringLiteral("vt")) {
                    float s,t;
                    lineStream >> s >> t;
                    loaded_texCoords.append(QVector2D(s, t));
                    hasTexCoords = true;
                } else if (token == QStringLiteral("vn")) {
                    float x, y, z;
                    lineStream >> x >> y >> z;
                    loaded_normals.append(QVector3D( x, y, z ));
                    hasNormals = true;
                } else if (token == QStringLiteral("f")) {
                    int i = 0;
                    facesCount++;
                    while (!lineStream.atEnd()) {

                        if(i >= 3) continue;
                        QString faceString;
                        lineStream >> faceString;

                        QStringList indices = faceString.split(QChar::fromLatin1('/'));

                        v.append(loaded_vertices.at(indices.at(0).toInt() - 1));

                        if(hasTexCoords)
                            uv.append(loaded_texCoords.at(indices.at(1).toInt() - 1));

                        if(hasNormals)
                            n.append(loaded_normals.at(indices.at(2).toInt() - 1));

                        i++;
                    }
                }
            }
        }

        for(int i = 0 ; i < facesCount ; i++)
        {
            QVector3D face_v[3];
            QVector2D face_uv[3];

            face_v[0] = v[i * 3 + 0];
            face_v[1] = v[i * 3 + 1];
            face_v[2] = v[i * 3 + 2];

            if(hasTexCoords)
            {
                face_uv[0] = uv[i * 3 + 0];
                face_uv[1] = uv[i * 3 + 1];
                face_uv[2] = uv[i * 3 + 2];
            }

            addTriangleCollider(2.3*face_v[0], 2.3*face_v[1], 2.3*face_v[2], facesCount, face_uv[0], face_uv[1], face_uv[2], TextureManager::getTexture("grass"));
        }

}




void GLWidget::initializeGL()
{
    initializeOpenGLFunctions();
    glClearColor(0.1f, 0.2f, 0.3f, 1);
    glFrontFace(GL_CCW);
    glCullFace(GL_BACK);

    m_program = new QOpenGLShaderProgram;
    m_program->addShaderFromSourceFile(QOpenGLShader::Vertex, "resources/shader.vs");
    m_program->addShaderFromSourceFile(QOpenGLShader::Fragment, "resources/shader.fs");
    m_program->bindAttributeLocation("vertex", 0);
    m_program->bindAttributeLocation("normal", 1);
    m_program->link();

    m_program->bind();
    m_projMatrixLoc = m_program->uniformLocation("projMatrix");
    m_viewMatrixLoc = m_program->uniformLocation("viewMatrix");
    m_modelMatrixLoc = m_program->uniformLocation("modelMatrix");
    m_hasTextureLoc = m_program->uniformLocation("hasTexture");
    m_cameraPositionLoc=m_program->uniformLocation("cameraPosition");

    m_materialLoc.ambient=m_program->uniformLocation("material.ambient");
    m_materialLoc.specular=m_program->uniformLocation("material.specular");
    m_materialLoc.diffuse=m_program->uniformLocation("material.diffuse");
    m_materialLoc.shiness=m_program->uniformLocation("material.shiness");

    for (int i=0;i<MAX_LIGHTS;i++) {
        m_lightLoc[i].position=m_program->uniformLocation(QString().asprintf("light[%d].position", i));
        m_lightLoc[i].ambient=m_program->uniformLocation(QString().asprintf("light[%d].ambient", i));
        m_lightLoc[i].diffuse=m_program->uniformLocation(QString().asprintf("light[%d].diffuse", i));
        m_lightLoc[i].specular=m_program->uniformLocation(QString().asprintf("light[%d].specular", i));
        m_lightLoc[i].isActive=m_program->uniformLocation(QString().asprintf("light[%d].isActive", i));
        m_lightLoc[i].attenuation=m_program->uniformLocation(QString().asprintf("light[%d].attenuation", i));
    }
    loadTriangleCollidersFromFile("resources/collider.obj", TextureManager::getTexture("grass"));


    m_program->release();

    m_program_HUD=new QOpenGLShaderProgram;
    m_program_HUD->addShaderFromSourceFile(QOpenGLShader::Vertex, "resources/shader_HUD.vs");
    m_program_HUD->addShaderFromSourceFile(QOpenGLShader::Fragment, "resources/shader_HUD.fs");
    m_program_HUD->bindAttributeLocation("vertex", 0);
    m_program_HUD->bindAttributeLocation("normal", 1);
    m_program_HUD->bindAttributeLocation("uvCoord", 2);
    m_program_HUD->link();

    m_program_HUD->bind();
    m_resolutionLoc_HUD=m_program_HUD->uniformLocation("resolution");
    m_color_HUD=m_program_HUD->uniformLocation("color");
    m_hasTexture_HUD=m_program_HUD->uniformLocation("hasTexture");
    m_rectangleLoc_HUD.xPos=m_program_HUD->uniformLocation("rect.xPos");
    m_rectangleLoc_HUD.yPos=m_program_HUD->uniformLocation("rect.yPos");
    m_rectangleLoc_HUD.width=m_program_HUD->uniformLocation("rect.width");
    m_rectangleLoc_HUD.height=m_program_HUD->uniformLocation("rect.height");
    m_program_HUD->release();
	
    lastUpdateTime = 0;
    timer.start();

    CMesh::loadAllMeshes();
    TextureManager::init();
    initCollisionTriangles();
    addObject(&m_player);

//    for(int i = 0 ; i < 5 ; i++) {
//        for(int j = 0 ; j < 7 ; j++) {
//            // Wskaźnik do Cube'a z tworzeniem obiektu.
//            // MUSI BYĆ WSKAŹNIK !!!
//            Cube* cube = new Cube();

//            // Ustawienie pozycji Cube'a
//            cube->position.setX(j * 1 - 3);
//            cube->position.setY(0);
//            cube->position.setZ(i * 1 - 6);

//            // Kolor Cube'a. Zwykły gradient.
//            cube->material.diffuse.setX(i * 0.2f);
//            cube->material.diffuse.setY(0.5f);
//            cube->material.diffuse.setZ(j * 0.1f);

//            // Wielkość Cube'a.
//            // Ustawienie w jednej linijce zamiast osobno dla X, Y i Z.
//            cube->scale = QVector3D(0.3f, 0.3f, 0.3f);

//            // Dodanie obiektu do sceny.
//            cube->m_radius = 0.5 * sqrt(3 * cube->scale.x() * cube->scale.x());
//            cube->m_texture = TextureManager::getTexture("brick");
//            addObject(cube);
//        }
//    }

    /*enemy* enimen = new enemy();
    enimen->player=&m_player;

    // Ustawienie pozycji Cube'a
    enimen->position.setX(0);
    enimen->position.setY(0);
    enimen->position.setZ(-3);

    // Kolor Cube'a. Zwykły gradient.
    enimen->material.diffuse.setX(0.2f);
    enimen->material.diffuse.setY(0.5f);
    enimen->material.diffuse.setZ(0.1f);

    // Wielkość Cube'a.
    // Ustawienie w jednej linijce zamiast osobno dla X, Y i Z.
    enimen->scale = QVector3D(0.3f, 0.3f, 0.3f);

    // Dodanie obiektu do sceny. przeciwnik
    enimen->m_radius = 0.5 * sqrt(3 * enimen->scale.x() * enimen->scale.x());
    enimen->m_texture = TextureManager::getTexture("boar_skin");
    addObject(enimen);*/
}

void GLWidget::setLights() {
    for (int i=0;i<MAX_LIGHTS;i++) {
        m_program->setUniformValue(m_lightLoc[i].position, m_lights[i].position);
        m_program->setUniformValue(m_lightLoc[i].ambient, m_lights[i].ambient);
        m_program->setUniformValue(m_lightLoc[i].diffuse, m_lights[i].diffuse);
        m_program->setUniformValue(m_lightLoc[i].specular, m_lights[i].specular);
        m_program->setUniformValue(m_lightLoc[i].isActive, m_lights[i].isActive);
        m_program->setUniformValue(m_lightLoc[i].attenuation, m_lights[i].attenuation);
    }
}


void GLWidget::updateGL() {
    //robotArmAngle = robotArmAngle + 1;
    przeladowanie--;

    float jump_count=28.8f;
    QCursor::setPos(mapToGlobal(QPoint(width()/2, height()/2)));
if (liczba_spawnow2 != 0) {
    if(czas_spawn == 0)
    {
        czas_spawn = 30;
        liczba_spawnow2--;
        enemy*e = new enemy;
        e->player=&m_player;
        e->damage=liczba_spawnow-(liczba_spawnow2-1);
        e->position.setX(0);
        e->position.setY(-6.83);
        e->position.setZ(rand()%5);
        e->material.diffuse.setX(0.2f);
        e->material.diffuse.setY(0.5f);
        e->material.diffuse.setZ(0.1f);
        e->scale = QVector3D(0.3f, 0.3f, 0.3f);
        e->m_radius = 0.5 * sqrt(3 * e->scale.x() * e->scale.x());
        e->m_texture = TextureManager::getTexture("boar_skin");
        addObject(e);
    }
    else {
        czas_spawn--;
    }
}


    //Movement control:
    //Forward
    if (m_keyState[Qt::Key_W]) {
        m_player.energy.setX(m_player.energy.x() + m_player.direction.x() * m_player.speed);
        m_player.energy.setZ(m_player.energy.z() + m_player.direction.z() * m_player.speed);
    }

    //Left
    if (m_keyState[Qt::Key_A]) {
        m_player.energy.setX(m_player.energy.x() + m_player.direction.z() * m_player.speed);
        m_player.energy.setZ(m_player.energy.z() - m_player.direction.x() * m_player.speed);
    }

    //Right
    if (m_keyState[Qt::Key_D]) {
        m_player.energy.setX(m_player.energy.x() - m_player.direction.z() * m_player.speed);
        m_player.energy.setZ(m_player.energy.z() + m_player.direction.x() * m_player.speed);
    }

    //Backward
    if (m_keyState[Qt::Key_S]) {
        m_player.energy.setX(m_player.energy.x() - m_player.direction.x() * m_player.speed);
        m_player.energy.setZ(m_player.energy.z() - m_player.direction.z() * m_player.speed);
    }

    //Jump
    if (m_keyState[Qt::Key_Space] && m_player.isOnGround) {
        m_player.isOnGround=false;
        m_player.energy.setY(m_player.energy.y() + jump_count * m_player.speed);
    }

    //Down
    if (m_keyState[Qt::Key_F]) {
        m_player.energy.setY(m_player.energy.y() - jump_count * m_player.speed);
    }

    //Update dla wszytskich obiektów nieulegających interakcji z graczem
    for(int i = 0 ; i < m_gameObjects.size(); i++) {
        GameObject* obj = m_gameObjects[i];
        obj->previousPosition=obj->position;

        // Porównujemy każdy obiekt z każdym
        for(int j = 0 ; j < m_gameObjects.size() ; j++) {
            if (i == j) // Nie porównujemy obiektów samych ze sobą
                continue;

            GameObject* obj2 = m_gameObjects[j];

            // Liczymy wektor od pozycji jednego obiektu do drugiego
            QVector3D v = obj->position - obj2->position;

            // Długość tego wektora to odległość między środkami obiektów
            float d = v.length();

            // Porównujemy z sumą promieni
            if(d < (obj->m_radius + obj2->m_radius)) {
                std::string name1=obj->m_name;
                std::string name2=obj2->m_name;
                GameObject* o1=obj;
                GameObject* o2=obj2;
                if (strcmp(name1.c_str(), name2.c_str())>0) {
                    o1=obj2;
                    o2=obj;
                    v=-v;
                }
                if (!o1->m_name.compare("Player") && !o2->m_name.compare("bullet")) {
                    o2->isAlive=false;
                    m_player.hp-=5;
                } else if(!o1->m_name.compare("bullet") && !o2->m_name.compare("cube")) {
                    o1->isAlive=false;
                    o2->isAlive=false;
                } else if (!o1->m_name.compare("bullet") && !o2->m_name.compare("enemy")) {
                    o1->isAlive=false;
                    o2->object_hp-=20;
                    if (o2->object_hp<=0) o2->isAlive=false;
                } else {

                    o1->position=o1->position+v*(d/2);      //Poprawa kolizji
                    o2->position=o2->position-v*(d/2);
                    v.normalize();
                    float energySum = obj->energy.length() + obj2->energy.length();
                    obj->energy = v * energySum / 2;
                    obj2->energy = -v * energySum / 2;
                }
                // Reakcja na kolizję!
            }
        }
        obj->energy.setY(obj->energy.y() - 0.06f); //Grawitacja
        obj->update();
    }

    for (unsigned int i = 0; i < m_gameObjects.size(); i++)
    {
        GameObject* obj = m_gameObjects[i];
        for (int j = 0; j < collisionTriangles.size(); j++)
        {
            Triangle tr = collisionTriangles[j];
            float currDist = tr.A * obj->position.x() + tr.B * obj->position.y() + tr.C * obj->position.z() + tr.D;
            float prevDist = tr.A * obj->previousPosition.x() + tr.B * obj->previousPosition.y() + tr.C * obj->previousPosition.z() + tr.D;
            if ((currDist * prevDist < 0) || abs(currDist) < obj->m_radius) {
    // Rzut pozycji obiektu na plaszczyzne
            QVector3D p = obj->position - tr.n * currDist;
    // Przesuniecie punktu do srodka trojkata o dlugosc promienia kolidera
            QVector3D r = (tr.v1 + tr.v2 + tr.v3) * (1.0f / 3.0f) - p;
            r = r.normalized();
            p = p + r * obj->m_radius;
            // Obliczenle v, w, u - wspolrzednych barycentrycznych
            QVector3D v0 = tr.v2 - tr.v1, v1 = tr.v3 - tr.v1, v2 = p - tr.v1;
            float d00	=	QVector3D::dotProduct(v0,	v0);
            float d01	=	QVector3D::dotProduct(v0,	v1);
            float d11	=	QVector3D::dotProduct(v1,	v1);
            float d20 = QVector3D::dotProduct(v2, v0);
            float d21 = QVector3D::dotProduct(v2, v1);
            float denom = d00 * d11 - d01 * d01;
            float v = (d11 * d20 - d01 * d21) / denom;
            float w = (d00 * d21 - d01 * d20) / denom;
            float u = 1.0f - v - w;
            // Sprawdzenie czy punkt jest w srodku trojkata
            if (v >= 0 && w >= 0 && (v + w) <= 1)
            {
                float d = obj->m_radius - currDist;
                obj->position = obj->position + tr.n * d;
                obj->energy = obj->energy - tr.n * QVector3D::dotProduct(tr.n, obj->energy) * 2;
                obj->isOnGround=true;
            }
        }
    }
}

    //Sprawdzenie, czy obiekt jest żywy.
    for(int i = 0 ; i < m_gameObjects.size(); ) {
        GameObject* obj = m_gameObjects[i];
        if(obj->isAlive == false) {

            if(obj->m_name.compare("enemy") == 0)
            {
                licznik++;
            }

            m_gameObjects.erase(m_gameObjects.begin() + i);
            delete obj;
        } else
            i++;
    }
}




/*void GLWidget::paintGL()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);

    QStack<QMatrix4x4> worldMatrixStack;

    m_program->bind();

    m_program->setUniformValue(m_lightLoc.position, QVector3D(0.0f, 0.0f, 15.0f));
    m_program->setUniformValue(m_lightLoc.ambient, QVector3D(0.1f, 0.1f, 0.1f));
    m_program->setUniformValue(m_lightLoc.diffuse, QVector3D(0.9f, 0.9f, 0.9f));




    //FPP camera
    m_camera.setToIdentity(); m_world.setToIdentity();
    m_camera.lookAt(m_player.position, m_player.position + m_player.direction, QVector3D(0, 1, 0) );
    //TPP camera: m_camera.lookAt(m_player.position - m_camDistance * m_player.direction, m_player.position,QVector3D(0, 1, 0) );


    // Bunny
    worldMatrixStack.push(m_world);
        m_world.translate(0.7f, 0.0f, 0.2f);
        m_world.scale(QVector3D(0.1f, 0.1f, 0.1f));
        setTransforms();
        m_program->setUniformValue(m_modelColorLoc,QVector3D(1.0f, 1.0, 1.0));
    m_world = worldMatrixStack.pop();

    // Robot
    worldMatrixStack.push(m_world);

        m_world.translate(m_player.position);
        float phii = atan2(m_player.direction.z(), m_player.direction.x());
        m_world.rotate(-phii * 180.0f / M_PI + 90, 0, 1, 0);

    // Robot's Head
        worldMatrixStack.push(m_world);
            m_world.translate(0.0f, 0.20f, 0.0f);
            m_world.scale(QVector3D(0.1f, 0.1f, 0.1f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(0.0f, 1.0, 0.0));

        m_world = worldMatrixStack.pop();

    // Robot's Body
        worldMatrixStack.push(m_world);
            m_world.translate(0.0f, 0.0f, 0.0f);
            m_world.scale(QVector3D(0.25f, 0.3f, 0.15f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(0.0f, 0.0, 1.0));

        m_world = worldMatrixStack.pop();

    // Robot's Left Arm
        worldMatrixStack.push(m_world);
            m_world.translate(0.12f, 0.05f, 0.0f);
            //m_world.rotate(-15.0f, 0, 0, 1);
            //m_world.rotate(30*sin(robotArmAngle), 0, 0, 1);
            m_world.translate(0.08f, 0.0f, 0.0f);
            m_world.scale(QVector3D(0.16f, 0.05f, 0.05f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(1.0f, 0.0, 0.0));

        m_world = worldMatrixStack.pop();

    // Robot's Right Arm
        worldMatrixStack.push(m_world);
            m_world.translate(-0.2f, 0.05f, 0.0f);
            m_world.rotate(15.0f, 0, 0, 1);
            m_world.scale(QVector3D(0.16f, 0.05f, 0.05f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(1.0f, 0.0, 0.0));

        m_world = worldMatrixStack.pop();

    // Robot's Left Leg
        worldMatrixStack.push(m_world);
            m_world.translate(-0.1f, -0.2f, 0.0f);
            m_world.rotate(-15.0f, 0, 0, 1);
            m_world.scale(QVector3D(0.05f, 0.16f, 0.05f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(1.0f, 0.0, 0.0));

        m_world = worldMatrixStack.pop();

    // Robot's Right Arm
        worldMatrixStack.push(m_world);
            m_world.translate(0.1f, -0.2f, 0.0f);
            m_world.rotate(15.0f, 0, 0, 1);
            m_world.scale(QVector3D(0.05f, 0.16f, 0.05f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(1.0f, 0.0, 0.0));

        m_world = worldMatrixStack.pop();

    m_world = worldMatrixStack.pop();

    // Circle of spheres and cubes
    for(int i = 0 ; i < 15 ; i++)
    {
        QVector3D innerPosition;
        QVector3D outerPosition;

        float r1 = 1;
        float r2 = 2;
        float theta1 = float(i) / 15 * 2 * float(M_PI);
        float theta2 = float(i+0.5f) / 15 * 2 * float(M_PI);

        innerPosition.setX(r1 * cos(theta1));
        innerPosition.setY(0);
        innerPosition.setZ(r1 * sin(theta1));

        outerPosition.setX(r2 * cos(theta2));
        outerPosition.setY(0);
        outerPosition.setZ(r2 * sin(theta2));

        worldMatrixStack.push(m_world);
            m_world.translate(innerPosition);
            m_world.scale(QVector3D(0.2f, 0.2f, 0.2f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(cos(theta1) * 0.5f + 0.5f, sin(theta1) * 0.5f + 0.5f, 0.0));

        m_world = worldMatrixStack.pop();

        worldMatrixStack.push(m_world);
            m_world.translate(outerPosition);
            m_world.scale(QVector3D(0.2f, 0.2f, 0.2f));
            setTransforms();
            m_program->setUniformValue(m_modelColorLoc, QVector3D(0.02f, cos(theta1) * 0.5f + 0.5f, sin(theta1) * 0.5f + 0.5f));

        m_world = worldMatrixStack.pop();
    }

    m_program->release();

    float timerTime = timer.elapsed() * 0.001f;         //new
    float deltaTime = timerTime - lastUpdateTime;
    if(deltaTime >= (1.0f / 60.0f)) {
    updateGL();
    lastUpdateTime = timerTime; }

    if(m_keyState[Qt::Key_Z]) m_camDistance += 0.005f;
    if(m_keyState[Qt::Key_X]) m_camDistance -= 0.005f;



    update();

}*/
float player_height=0.3f;
void GLWidget::paintGL() {

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST);    glEnable(GL_CULL_FACE);
    QStack<QMatrix4x4> worldMatrixStack;

    m_lights[0].position=QVector3D(-3.0f, 1.0f, -4.0f);
    m_lights[0].ambient=QVector3D(0.1f, 0.1f, 0.1f);
    m_lights[0].diffuse=QVector3D(1.0f, 0.3f, 0.3f);
    m_lights[0].specular=QVector3D(0.1f, 0.1f, 0.1f);
    m_lights[0].isActive=true;
    m_lights[0].attenuation=0.5f;

    m_lights[1].position=QVector3D(3.0f, 1.0f, -4.0f);
    m_lights[1].ambient=QVector3D(0.1f, 0.1f, 0.1f);
    m_lights[1].diffuse=QVector3D(0.3f, 1.0f, 0.3f);
    m_lights[1].specular=QVector3D(0.1f, 0.1f, 0.1f);
    m_lights[1].isActive=true;
    m_lights[1].attenuation=0.5f;

    m_program->bind();
    m_program->setUniformValue(m_cameraPositionLoc, m_player.position-m_camDistance*m_player.direction);

    setLights();

    m_world.setToIdentity();
    m_camera.setToIdentity();
    //m_camera.lookAt(m_player.position - m_camDistance * m_player.direction, m_player.position, QVector3D(0, 1, 0) );
    //FPP:
    m_camera.lookAt(m_player.position+QVector3D(0,player_height+0.1,0), m_player.position + m_player.direction + QVector3D(0,player_height+0.1,0), QVector3D(0, 1, 0) );

    for(int i = 0 ; i < m_gameObjects.size(); i++) {
        GameObject* obj = m_gameObjects[i];

        m_program->setUniformValue(m_materialLoc.ambient, obj->material.ambient);
        m_program->setUniformValue(m_materialLoc.diffuse, obj->material.diffuse);
        m_program->setUniformValue(m_materialLoc.specular, obj->material.specular);
        m_program->setUniformValue(m_materialLoc.shiness, obj->material.shiness);

        if (obj->m_texture!=nullptr) {
            m_program->setUniformValue(m_hasTextureLoc,1);
            obj->m_texture->bind();
        } else {
            m_program->setUniformValue(m_hasTextureLoc,0);
        }
        worldMatrixStack.push(m_world);
        m_world.translate(obj->position);
        m_world.rotate(obj->rotation.x(), 1, 0, 0);
        m_world.rotate(obj->rotation.y(), 0, 1, 0);
        m_world.rotate(obj->rotation.z(), 0, 0, 1);
        m_world.scale(obj->scale);
        setTransforms();	obj->render(this);	m_world = worldMatrixStack.pop();
    }

    for (int i=0;i<collisionTriangles.size(); /*nic*/) {
        Triangle triangle=collisionTriangles[i];

        m_program->setUniformValue(m_materialLoc.ambient, QVector3D(1.0f,1.0f,1.0f));
        m_program->setUniformValue(m_materialLoc.diffuse, QVector3D(1.0f,1.0f,1.0f));
        m_program->setUniformValue(m_materialLoc.specular, QVector3D(1.0f,1.0f,1.0f));
        m_program->setUniformValue(m_materialLoc.shiness, 1.0f);

        if (triangle.texture!=nullptr) {
            m_program->setUniformValue(m_hasTextureLoc,1);
            triangle.texture->bind();
        } else {
            m_program->setUniformValue(m_hasTextureLoc,0);
        }

        worldMatrixStack.push(m_world);
        m_world.translate(QVector3D(0,0,0));
        m_world.rotate(0, 1, 0, 0);
        m_world.rotate(0, 0, 1, 0);
        m_world.rotate(0, 0, 0, 1);
        m_world.scale(QVector3D(1,1,1));
        setTransforms();
        collisionTrianglesMesh.render(this, i*3, triangle.groupSize *3);
        m_world=worldMatrixStack.pop();

        i+=triangle.groupSize;
    }


    CMesh* skydomeMesh = CMesh::m_meshes["skydome"];

    m_lights[0].ambient = QVector3D(1.0f, 1.0f, 1.0f);
    m_lights[0].attenuation = 0.0f;
    setLights();
    m_program->setUniformValue(m_materialLoc.ambient, QVector3D(1.0f, 1.0f, 1.0f));
    m_program->setUniformValue(m_materialLoc.diffuse, QVector3D(0.0f, 0.0f, 0.0f));
    m_program->setUniformValue(m_materialLoc.specular, QVector3D(0.0f, 0.0f, 0.0f));
    m_program->setUniformValue(m_materialLoc.shiness, 0.0f);

    m_program->setUniformValue(m_hasTextureLoc, 1);
    TextureManager::getTexture("skydome")->bind();

    worldMatrixStack.push(m_world);
        m_world.translate(m_player.position);
        m_world.rotate(0, 1, 0, 0);
        m_world.rotate(timer.elapsed() * 0.001f, 0, 1, 0);
        m_world.rotate(0, 0, 0, 1);
        m_world.scale(20.0f);
        setTransforms();
        skydomeMesh->render(this);
    m_world = worldMatrixStack.pop();




    m_program->release();

    float timerTime = timer.elapsed() * 0.001f;
    float deltaTime = timerTime - lastUpdateTime;
    if(deltaTime >= (1.0f / FPS)) {
        updateGL();	lastUpdateTime = timerTime;
    }
    paintHUD();
    update();
}


void GLWidget::setTransforms(void)
{
    m_program->setUniformValue(m_projMatrixLoc, m_proj);
    m_program->setUniformValue(m_viewMatrixLoc, m_camera);
    m_program->setUniformValue(m_modelMatrixLoc, m_world);
}

void GLWidget::resizeGL(int w, int h)
{
    m_proj.setToIdentity();
    m_proj.perspective(60.0f, GLfloat(w) / h, 0.01f, 100.0f);
    m_resolution=QVector2D(w,h);
}

void GLWidget::mousePressEvent(QMouseEvent *event)
{
    m_lastPos = event->pos();
    if (m_player.hp>0 || licznik==liczba_spawnow) {
    //Strzelanie pociskami
    if (event->buttons() & Qt::LeftButton) {
        if (przeladowanie<0) {
        Bullet* bullet = new Bullet();
        bullet->direction=m_player.direction;
        bullet->position = m_player.position + QVector3D(0,player_height,0);
        bullet->scale = QVector3D(0.1f, 0.1f, 0.1f);
        bullet->m_radius = 0.1f;
        bullet->energy = 3 * m_player.direction;
        addObject(bullet);
        przeladowanie=10;
        }
    }
    }
}

void GLWidget::mouseMoveEvent(QMouseEvent *event)
{
    if (m_player.hp>0) {
        int dx = event->x() - width()/2;
        int dy = event->y() -  height()/2;
        m_player.phi=atan2(m_player.direction.z(), m_player.direction.x());
        m_player.theta=acos(m_player.direction.y());
        m_player.phi = m_player.phi + dx * 0.01;
        m_player.theta = m_player.theta + dy * 0.01;

        if(m_player.theta < 0.01) m_player.theta = 0.01;
        if(m_player.theta > M_PI) m_player.theta = M_PI;

        m_player.direction.setX( sin(m_player.theta) * cos(m_player.phi));
        m_player.direction.setY( cos(m_player.theta));
        m_player.direction.setZ( sin(m_player.theta) * sin(m_player.phi));

        if (event->buttons() & Qt::LeftButton) {
            //setXRotation(m_camXRot + 0.5f * dy);
            // setYRotation(m_camYRot + 0.5f * dx);
        } else if (event->buttons() & Qt::RightButton) {
            // setXRotation(m_camXRot + 0.5f * dy);
            // setZRotation(m_camZRot + 0.5f * dx);
        }
        m_lastPos = event->pos();
    }
}

void GLWidget::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_Escape)
        exit(0);
    else
        QWidget::keyPressEvent(e);

    if(e->key() >= 0 && e->key() <= 255)
        m_keyState[e->key()] = true;

    if (e->key() == Qt::Key_Escape) exit(0);
       /* else if (e->key() == Qt::Key_Space) {
        Bullet* bullet = new Bullet();
        bullet->position = m_player.position + m_player.direction * 0.7f;
        bullet->position.setY(0);
        bullet->scale = QVector3D(0.5f, 0.5f, 0.5f);
        bullet->m_radius = 0.5f;
        bullet->energy = 3 * m_player.direction;
        bullet->energy.setY(0);
        addObject(bullet);
    } else
        QWidget::keyPressEvent(e);*/
}

void GLWidget::keyReleaseEvent(QKeyEvent *e)
{
    if(e->key() >= 0 && e->key() <= 255)
        m_keyState[e->key()] = false;
}
