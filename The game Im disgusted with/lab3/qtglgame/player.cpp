#include "player.h"
#include <QElapsedTimer>
#include <cmath>

Player::Player()
{
    position = QVector3D(0, -6.83, 0);
    direction = QVector3D(0, 0, -1);
    speed = 0.01f;


}

void Player::init() {
    //m_mesh.generateMeshFromObjFile("resources/bunny.obj");
    m_mesh=CMesh::m_meshes["Shotgun"];

    scale = QVector3D(0.07f, 0.07f, 0.07f);
    m_radius = 0.05f;
    m_name = "Player";
}

void Player::render(GLWidget* glwidget) {
    m_mesh->render(glwidget);
}

void Player::update() {
    rotation.setY(180-atan2(direction.z(), direction.x()) * 180 / 3.14f);
    //rotation.setZ(180-atan2(direction.z(), direction.x()) * 180);
    // Wykorzystanie energii.
    position = position + energy;

    // Wytrącanie energii.
    energy = energy / 1.2f;
}
