#pragma once
#include "Vec2.h"

struct RigidBody {
    Vec2 position;
    Vec2 velocity;
    Vec2 acceleration;  // accumulated forces
    double mass;
    double inverseMass;
    double restitution;  // coefficient of restitution (bounciness)
    
    RigidBody(double mass = 1.0, double restitution = 0.5);
    
    void applyForce(const Vec2& force);
    void integrate(double dt);
    void clearAccumulator();
};
