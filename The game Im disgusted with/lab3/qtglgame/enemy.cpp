#include "enemy.h"
#include <cmath>

enemy::enemy()
{
    m_name="enemy";
}

void enemy::init() {
    m_mesh=CMesh::m_meshes["pig"];
}

void enemy::render(GLWidget *glwidget) {
    m_mesh->render(glwidget);
}

void enemy::update() {
    // Wykorzystanie energii.
    position = position + energy;

    // Wytrącanie energii.
    energy = energy / 1.2f;

    //Podążanie za graczem
    direction=player->position-position;
    float d = direction.length();

    direction.setY(0);
    rotation.setY(270-atan2(player->direction.z(), player->direction.x())*180/3.14); //obracanie się do gracza
    direction.normalize();
    position+=direction*0.02;

    if(d < 0.5)
        player->hp -= damage;
}
