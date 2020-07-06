#ifndef GLWIDGET_H
#define GLWIDGET_H

#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QMatrix4x4>
#include <QKeyEvent>
#include <QMap>
#include <QElapsedTimer>
#include <cmesh.h>
#include <player.h>
#include <vector>

QT_FORWARD_DECLARE_CLASS(QOpenGLShaderProgram)

class GLWidget : public QOpenGLWidget, protected QOpenGLFunctions
{
    Q_OBJECT

public:
    GLWidget(QWidget *parent = nullptr);
    ~GLWidget();

    QSize sizeHint() const override;

    friend CMesh;

public slots:
    void cleanup();

protected:
    void initializeGL() override;
    void updateGL();
    void paintGL() override;
    void resizeGL(int width, int height) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;
    void keyReleaseEvent(QKeyEvent *event) override;

    void Update();
    void setTransforms(void);
    std::vector<GameObject*> m_gameObjects;
    void addObject(GameObject* obj);
    void paintHUD();
    void loadTriangleCollidersFromFile(QString filepath, QOpenGLTexture* texture);
    void loadHeightMap(QString filepath, QVector3D center, QVector3D size, QVector2D maxUV=QVector2D(0,0), QOpenGLTexture* texture=nullptr);

private:

    struct LightLocStruct
    {
        int position;
        int ambient;
        int diffuse;
        int specular;
        int isActive;
        int attenuation;
    };

    struct Light {
        QVector3D ambient;
        QVector3D position;
        QVector3D diffuse;
        QVector3D specular;
        bool isActive=false;
        float attenuation;
    };

    struct MaterialLocStruct {
        int ambient;
        int diffuse;
        int specular;
        int shiness;
    };

    struct RectangleLocStruct {
        int xPos;
        int yPos;
        int width;
        int height;
    };

    struct Triangle {
        QVector3D v1,v2,v3;
        QOpenGLTexture* texture;
        QVector3D n;
        float A,B,C,D;
        int groupSize;
    };

    static const int MAX_LIGHTS = 5;
    Light m_lights[MAX_LIGHTS];
    void setLights();

    std::vector<Triangle> collisionTriangles;
    CMesh collisionTrianglesMesh;
    void initCollisionTriangles();
    void addTriangleCollider(QVector3D v1,QVector3D v2,QVector3D v3,int groupSize,
                             QVector2D uv1=QVector2D(0,0),QVector2D uv2=QVector2D(0,0),
                             QVector2D uv3=QVector2D(0,0),QOpenGLTexture* texture=nullptr);


    QPoint m_lastPos;
    QOpenGLShaderProgram *m_program;
    int m_projMatrixLoc;
    int m_viewMatrixLoc;
    int m_modelMatrixLoc;
    int m_hasTextureLoc;
    int m_cameraPositionLoc;
    LightLocStruct m_lightLoc[MAX_LIGHTS];
    MaterialLocStruct m_materialLoc;

    QElapsedTimer timer;
    float lastUpdateTime;
    float FPS = 60;

    QOpenGLShaderProgram *m_program_HUD;
    int m_resolutionLoc_HUD;
    int m_color_HUD;
    int m_hasTexture_HUD;
    RectangleLocStruct m_rectangleLoc_HUD;
    void setRectangle(float xPos, float yPos, float width, float height, QVector3D color, QOpenGLTexture *texture);
    QVector2D m_resolution;

    QMatrix4x4 m_proj;
    QMatrix4x4 m_camera;
    QMatrix4x4 m_world;



    bool m_keyState[256];

    float m_camDistance = 1.5f;

    Player m_player;

    int licznik = 0;
    int czas_spawn=30;
    int przeladowanie=0;
    int liczba_spawnow=5;
    int liczba_spawnow2=5;  //wpisać to samo
};

#endif

