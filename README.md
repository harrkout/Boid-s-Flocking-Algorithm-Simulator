# Boid Simulator

## Overview

The Boid Simulator is a Python-based 2D simulation that models flocking behavior using a set of simple rules. These rules, inspired by the work of Craig Reynolds, simulate the behavior of a group of boids (bird-like objects), allowing them to align with each other, maintain cohesion, avoid overcrowding, and interact with the environment.

This simulation provides a hands-on look into how local behaviors can give rise to complex group dynamics. In addition to the basic flocking behaviors, the boids can interact with the mouse pointer, and they can also avoid a predator (represented by the mouse).

The project uses the **Pygame** library to create a graphical environment and handle user interaction.



![img](/img.png)



## Features

- **Boid Behaviors**:
  - **Alignment**: Boids adjust their movement to match the average direction (velocity) of nearby boids.
  - **Cohesion**: Boids steer towards the center of mass of nearby boids, encouraging them to stay together as a group.
  - **Separation**: Boids avoid crowding and potential collisions by steering away from other boids.

- **Mouse Interaction**:
  - **Attraction/Repulsion**: Boids can be either attracted to or repelled by the mouse pointer, simulating behaviors like curiosity or avoidance.

- **Predator Behavior**:
  - **Avoidance**: When enabled, boids will try to avoid the mouse pointer, mimicking predator-prey interactions.

- **Metrics Display**:
  - Key metrics such as **average speed** and **cohesion level** of the flock are shown in real-time, allowing users to monitor the flock’s behavior dynamically.

- **Interactive Simulation**:
  - Users can toggle various behaviors in real-time, allowing them to experiment and observe how different settings impact the flock’s movement.

## Interacting with the Simulation

Once the simulation window is open, you'll see a flock of boids moving around. You can interact with the boids and adjust their behavior in real-time by using the following keys:

- **Press 1**: Toggle mouse attraction for the boids. When enabled, boids will move towards the mouse position.
- **Press 2**: Toggle predator behavior. When enabled, boids will avoid the mouse pointer, simulating predator-prey interactions.
- **Press 3**: Toggle the display of metrics. When enabled, the average speed and cohesion of the flock will be displayed on the screen.
- **Press Esc**: Exit the simulation.

## Boid Movement

Boids in the simulation move based on the following behaviors:

- **Alignment**: Boids adjust their movement to align with nearby boids.
- **Cohesion**: Boids steer towards the center of mass of nearby boids, keeping the flock together.
- **Separation**: Boids steer away from others to avoid crowding and collisions.
- **Mouse Attraction/Repulsion**: Boids will either move towards or away from the mouse pointer depending on the setting.
- **Predator Avoidance**: When predator behavior is enabled, boids will avoid the mouse pointer.

## Metrics

When the metrics display is enabled, the simulation will show the average speed and cohesion of the boids in real-time. This allows you to see how the flock is behaving at any given moment.

# Boid Class

The **Boid** class is at the core of the simulation. It manages the creation, movement, and behavior of each boid. Each boid has properties like position, velocity, and acceleration, and several methods that control how it behaves in the flock:

- **edges()**: Ensures that boids wrap around the screen when they move off the edges, keeping the simulation continuous.
- **align()**: Steers the boid towards the average heading of nearby boids, allowing it to align with the flock.
- **cohesion()**: Steers the boid towards the center of mass of nearby boids, keeping the flock together.
- **separation()**: Makes the boid steer away from other boids to avoid collisions and overcrowding.
- **seek_mouse()**: Controls how the boids are attracted to or repelled by the mouse pointer, based on the current setting.
- **avoid_predator()**: When the predator feature is enabled, this method makes the boids avoid the mouse pointer.
- **flock()**: Combines the three main flocking behaviors—alignment, cohesion, and separation—into a single method that governs the boid’s movement.
- **update()**: Updates the boid’s position, velocity, and acceleration based on its current behavior.
- **draw()**: Draws the boid on the screen using Pygame’s drawing methods, displaying it as a triangle.



