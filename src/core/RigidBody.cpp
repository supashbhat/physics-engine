#include "RigidBody.h"

RigidBody::RigidBody(double mass, double restitution) 
    : position(0, 0), velocity(0, 0), acceleration(0, 0),
      mass(mass), restitution(restitution) {
    inverseMass = (mass > 0) ? 1.0 / mass : 0.0;
}

void RigidBody::applyForce(const Vec2& force) {
    acceleration += force * inverseMass;
}

void RigidBody::integrate(double dt) {
    // Euler integration
    velocity += acceleration * dt;
    position += velocity * dt;
    
    // Clear accumulated forces for next frame
    clearAccumulator();
}

void RigidBody::clearAccumulator() {
    acceleration = Vec2(0, 0);
}
