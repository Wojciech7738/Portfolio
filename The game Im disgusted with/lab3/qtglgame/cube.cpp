#include "cube.h"

Cube::Cube()
{
    m_name="Cube";
}

void Cube::init() {
    m_mesh=CMesh::m_meshes["cube"];
}

void Cube::render(GLWidget *glwidget) {
    m_mesh->render(glwidget);
}

void Cube::update() {
    // Wykorzystanie energii.
    position = position + energy;

    // Wytrącanie energii.
    energy = energy / 1.2f;
}
