#ifndef PLAYER_H
#define PLAYER_H
#include <QVector3D>
#include "gameobject.h"
#include "cmesh.h"

class Player : public GameObject
{
public:

    QVector3D direction; float speed;
    float phi; float theta;
    Player();

    void init();
    void render(GLWidget* glwidget);
    void update();
    CMesh* m_mesh;
    float hp = 100;

};

#endif // PLAYER_H
