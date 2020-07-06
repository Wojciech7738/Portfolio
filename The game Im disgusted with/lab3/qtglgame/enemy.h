#ifndef ENEMY_H
#define ENEMY_H
#include "gameobject.h"
#include "cmesh.h"
#include "player.h"

class enemy : public GameObject
{ public:
    enemy();
    QVector3D direction;
    void init();
    void render(GLWidget* glwidget);
    void update();
    CMesh* m_mesh;
    Player *player;
    float phi; float theta;
    float damage;
};

#endif // ENEMY_H
